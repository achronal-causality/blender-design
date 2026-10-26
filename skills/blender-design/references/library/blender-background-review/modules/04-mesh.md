# 04. Mesh construction and BMesh

## Purpose and prerequisites

Choose a representation, construct valid topology and write it back without stale references. Read [data](02-data.md) and [evaluation](03-context.md). Primary references: [Mesh](https://docs.blender.org/api/5.2/bpy.types.Mesh.html), [BMesh](https://docs.blender.org/api/5.2/bmesh.html), [BMesh types](https://docs.blender.org/api/5.2/bmesh.types.html), [operators](https://docs.blender.org/api/5.2/bmesh.ops.html), [utilities](https://docs.blender.org/api/5.2/bmesh.utils.html), [geometry queries](https://docs.blender.org/api/5.2/bmesh.geometry.html).

## Mental model and invariants

A Mesh stores compact arrays: vertices contain positions, edges contain pairs of vertex indices, polygons identify contiguous ranges of **loops**, and loops represent face corners with vertex/edge indices. A MeshLoop is not an edge loop used in modeling selection. Corner-domain UVs, colors and split normals allow a shared geometric vertex to have different values on different faces.

BMesh stores editable connectivity through `BMVert`, `BMEdge`, `BMFace` and `BMLoop` objects. It supports efficient local topology edits without repeatedly rebuilding all Mesh arrays. A BMesh can be an independently allocated editing workspace or the live Edit Mode representation owned by Blender. Those ownership cases have different completion and cleanup contracts. [C10](../CLAIMS.md#c10).

Correct topology requires valid indices, non-repeated face vertices, consistent edge/corner relationships and meaningful geometry. Valid storage does not prove a watertight, self-intersection-free or physically manufacturable solid. Shading normals do not repair topology. Selection invariants are separate from geometry validity.

## API contracts

### Direct Mesh construction

`Mesh.from_pydata(vertices, edges, faces, shade_flat=True)` fills a Mesh from coordinate sequences, edge index pairs and polygon index sequences. Coordinates are in the object's local geometry space; Blender does not attach a physical unit certificate. An empty `edges` sequence lets Blender derive edges from faces. Explicit edges can also represent loose wire geometry. Face winding determines orientation. This method is not a general input validator.

```python
# UNEXECUTED: one open quad, not a closed solid.
import bpy

mesh = bpy.data.meshes.new('Quad')
mesh.from_pydata([(0, 0, 0), (2, 0, 0), (2, 1, 0), (0, 1, 0)],
                 [], [(0, 1, 2, 3)], shade_flat=True)
if mesh.validate(verbose=True):
    raise ValueError('Constructor emitted topology requiring repair')
mesh.update(calc_edges=True)
```

`validate(verbose=False, clean_customdata=True)` may **mutate** invalid geometry; its Python return is `True` when data was corrected. In 5.2 `clean_customdata` is retained but no longer has the earlier effect. Treat a repair in a deterministic constructor as evidence that inputs or construction are wrong, rather than silently accepting repaired output. `validate_material_indices()` similarly corrects invalid face material indices and returns whether it changed them. `Mesh.update(calc_edges=False, calc_edges_loose=False)` updates mesh-related state, can calculate edges, and tags dependent geometry; it is not interchangeable with a full evaluated dependency graph refresh. [C11](../CLAIMS.md#c11).

`Mesh.clear_geometry()` clears mesh geometry while retaining some non-geometric datablock state; pinned source also frees animation data. It is not a reversible “clear vertices only” operation and is unnecessary for a candidate Mesh built separately. `calc_loop_triangles()` computes derived tessellation for polygon inspection; it does not permanently replace polygon topology with triangles.

### Attributes and normals

`mesh.attributes.new(name, type, domain)` returns an Attribute owned by the Mesh. Domain controls element count: `POINT` → vertices, `EDGE` → edges, `FACE` → polygons, `CORNER` → loops. Data type controls the property's value representation, e.g. `FLOAT` uses `.value`, `FLOAT_VECTOR` uses `.vector`, and colors have their own color properties. `AttributeGroupMesh` supplies collection operations; required built-in attributes cannot be treated as arbitrary removable data.

```python
# UNEXECUTED: scalar metadata on the four vertices of the preceding quad.
attr = mesh.attributes.new(name='support_weight', type='FLOAT', domain='POINT')
attr.data.foreach_set('value', [1.0, 1.0, 0.0, 0.0])
```

`foreach_set(property, sequence)` bulk-writes a flattened basic numeric sequence. A vector attribute with N elements needs 3N numbers. `foreach_get` fills an existing correctly sized mutable sequence/buffer. These are transfer operations, not vectorized topology validation; NumPy is optional, not required. Preserve attribute names, types and domains as part of the model contract. A name collision or type/domain mismatch is a revision conflict, not permission to overwrite arbitrary data.

Use `mesh.color_attributes` for modern color layers; historical `vertex_colors` is legacy. A `.` prefix may hide an attribute from normal UI lists. Named and anonymous attributes have different persistence and propagation semantics; anonymous Geometry Nodes attributes can be lost when converting evaluated geometry to a persistent Main Mesh.

`MeshVertex.normal`, vertex/face normal collections and corner normals expose different smoothing interpretations. `sharp_face` and `sharp_edge` influence shading splits; flat/smooth shading changes normals, not geometric curvature. `Mesh.normals_split_custom_set` assigns corner normals; `normals_split_custom_set_from_vertices` supplies vertex-based custom normals. Their arrays must match the expected topology. A zero vector has documented special behavior for retaining automatic normals; use explicit normalized directions where intentional. Negative-determinant transforms can reverse orientation; `Mesh.flip_normals()` changes winding and is not a universal custom-normal repair. `calc_tangents(uvmap=...)` needs UV data; tangents are outside the neutral inspection recipe. [C12](../CLAIMS.md#c12).

### Owned BMesh lifecycle

```python
# UNEXECUTED: isolated BMesh edit of an existing original Mesh.
import bmesh

bm = bmesh.new(use_operators=True)
try:
    bm.from_mesh(mesh)
    bm.verts.ensure_lookup_table()
    bm.verts[0].co.z += 0.1
    bm.normal_update()
    bm.to_mesh(mesh)
finally:
    bm.free()
mesh.update()
```

`bmesh.new(use_operators=True)` allocates caller-owned data. Disabling operators saves associated storage but makes `bmesh.ops` calls invalid. `from_mesh(mesh, face_normals=True, vertex_normals=True, ...)` **adds** mesh data to a BMesh; repeated calls are not reset semantics. Existing custom-data layers affect how later imports map attributes. `to_mesh(mesh)` writes back to an existing Mesh and rejects writing through this route while that Mesh is in Edit Mode. `free()` releases owned BMesh memory and invalidates element wrappers. A failure before write-back leaves the original Mesh unchanged by the local BMesh edit; a failure after write-back does not roll it back.

`ensure_lookup_table()` enables/rebuilds indexed sequence access after additions/removals. `index_update()` updates each element's `.index` field. They solve different problems. Neither makes indices durable semantic identifiers, and sorting a BMesh sequence need not update indices. Use element references only within the current topology lifetime and re-identify regions geometrically or through owned attributes after structural changes.

### BMesh operations

`bmesh.ops` functions take one positional `bm` and named operation parameters. Many return a dictionary of output slots containing mixed geometry types, not a new Mesh. Invalid keywords raise `TypeError`; a BMesh without operator storage raises `ValueError`. Native operation errors may become exceptions after mutation, with no rollback.

```python
# UNEXECUTED: fragment for a deliberately chosen face region in an owned BMesh.
result = bmesh.ops.extrude_face_region(bm, geom=region_faces)
new_verts = [item for item in result['geom'] if isinstance(item, bmesh.types.BMVert)]
bmesh.ops.translate(bm, verts=new_verts, vec=(0.0, 0.0, height))
bm.normal_update()
```

`region_faces` must be a current list of BMFace elements from `bm`; `height` is a scalar in local coordinates. `extrude_face_region` duplicates/constructs connected geometry and can delete/flip original elements depending on options and adjacency. It does **not** supply the subsequent displacement. Filter the returned `geom` rather than translating all vertices and moving the base too. `translate` adds the given vector to the selected BMVert positions. Retained references to removed original faces may be invalid.

For `bmesh.ops.bevel`, explicitly supply `geom`, `offset`, `segments`, `profile`, `affect='EDGES'` or `'VERTICES'`, and `clamp_overlap`. API defaults differ from a UI Bevel modifier. The wrapper tags eligible manifold edges and calls `BM_mesh_bevel`; the kernel clamps segments to at least one and returns early for nonpositive offset. A positive offset does not imply every supplied edge was beveled. Profile 0.5 is the conventional rounded cross-section, while other profiles alter the shape. [C13](../CLAIMS.md#c13).

`bmesh.utils` offers local split/join helpers returning elements or `None` under documented conditions; destructive helpers invalidate old connectivity. `bmesh.geometry.intersect_face_point(face, point)` is a face query, not a mesh Boolean or global inside-solid test. `BMesh.calc_volume(signed=...)` depends on orientation and a meaningful closed surface; numerical output does not certify manifoldness.

### Edit Mode distinction and selection

`bmesh.from_edit_mesh(mesh)` borrows the live Edit Mode BMesh. Finish with `bmesh.update_edit_mesh(mesh, loop_triangles=True, destructive=True)` when topology changed; choose `destructive=False` only for edits without element creation/removal. It updates the Edit Mode representation and optional tessellation. **Do not free the borrowed BMesh.** The pinned implementation protects Blender-owned memory while invalidating a freed wrapper; the old “dead BMesh until re-entering mode” report is historical, not a current guarantee. [R105715](../EXPERIENCE.md#r105715).

Selecting a face implies its boundary edges/vertices should be selected; deselecting a vertex should not leave selected incident faces. `select_set` performs downward selection updates; `select_flush_mode()` reconciles selection with `bm.select_mode`. Hidden geometry should not remain selected. These are caller-maintained invariants for scripts; arbitrary direct flag edits can violate them. Background constructors usually avoid selection entirely.

## Implementation traces

`rna_mesh.cc:400 - 474,1686 - 1786` maps positions, selection attributes and lazy normal access. `rna_mesh_api.cc:198 - 258` implements update/clear/validate, with the inverted internal validity result exposed as “changed.” `mesh_validate.cc:852 - 951` sequences topology and attribute checks and repairs.

`bmesh_py_api.cc:38 - 161` creates/borrows BMeshes; `bmesh_py_types.cc:1319 - 1408,1513 - 1592` establishes ownership and write-back. `bmesh_py_ops_call.cc:760 - 870` validates slots, executes, converts errors and releases operator storage. `bmo_extrude.cc:319 - 465` establishes original-region and duplicate handling; `bmo_bevel.cc:1 - 96` → `bmesh_bevel.cc:8239 - 8322` establishes eligibility and parameter normalization. Remaining geometric kernel internals are not claimed audited. [Pinned ranges](../SOURCE_TRACES.md).

## Failure modes and diagnosis

| Diagnostic/symptom | Likely distinction |
|---|---|
| `BMesh data of type BMesh has been removed` | Freed BMesh or stale elements |
| `outdated internal index table` | Rebuild lookup table after topology edit |
| `bmesh created with 'use_operators=False'` | Operator storage omitted |
| `Mesh is in editmode` / write-back rejection | Wrong ownership route |
| `validate` returns true | Data was repaired, not simply “valid” |
| Smooth render hides faceting or holes | Normals/materials do not prove geometric smoothness/closure |
| Bevel/extrusion appears to do nothing | Offset/displacement missing, ineligible geometry, clamp or wrong output selection |

## Evidence and open questions

D/S support representation and cleanup contracts. R144340 records a historical normals/modifier freeze on a different version/platform; its attachment and native stack are not a current-build reproduction. I requires validation before accepting construction and independent geometric checks appropriate to intent. [T07](../FUTURE_TESTS.md) investigates invalid topology, normals and modifier order; it is not manufacturing certification.
