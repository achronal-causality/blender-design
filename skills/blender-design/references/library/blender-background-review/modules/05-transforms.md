# 05. Transforms, curves and modifiers

## Purpose and prerequisites

Control coordinate space and the order of geometric changes. Read [ownership](02-data.md), [evaluation](03-context.md), and [mesh](04-mesh.md). References: [mathutils](https://docs.blender.org/api/5.2/mathutils.html), [Curve](https://docs.blender.org/api/5.2/bpy.types.Curve.html), [Modifier](https://docs.blender.org/api/5.2/bpy.types.Modifier.html).

## Mental model and invariants

Mesh and curve coordinates are stored in object-local space. The Object's transform places that data in a parent/world hierarchy. Modifiers operate on geometry in an ordered stack and normally leave the original editable data intact. A visible size can therefore change through vertex edits, Object scale, parent scale or modifier evaluation. These are different revision operations with different downstream effects.

For ordinary affine geometry, use column-vector semantics: `world_point = matrix_world @ local_point`; composition `T @ R @ S` scales, rotates, then translates the point. A normal transforms with the inverse transpose of the linear 3×3 part and is renormalized. Translation does not act on a direction. Negative determinant transforms reverse handedness. Singular transforms cannot be safely inverted. [C14](../CLAIMS.md#c14).

## API contracts

### Transform representations

`mathutils.Vector` is a numeric vector; `Matrix` represents linear/affine transforms; `Euler` represents ordered rotations in radians; `Quaternion` represents rotation using `(w, x, y, z)`. `Matrix @ Vector` and `Matrix @ Matrix` perform their geometric products. `Matrix.inverted()` rejects singular matrices; `inverted_safe()` can substitute a fallback and should not be used to conceal zero-scale input. `copy()` detaches an RNA-backed value from its owner. `decompose()` returns location, quaternion rotation and scale, but arbitrary shear is not preserved by a simple location/rotation/scale round trip.

`Object.location`, `rotation_euler`, `rotation_quaternion`, `rotation_mode`, `scale`, delta transforms and parent relationships contribute to placement. Choose the rotation representation before assignment. Transform locks primarily govern interactive editing and do not make Python assignments immutable. `matrix_basis` includes location/rotation/scale and delta transforms relative to parent; `matrix_parent_inverse` accounts for parenting offset; `matrix_world` is world placement. For ordinary object parenting without constraints, the useful relation is parent world × parent inverse × basis. Bone/vertex parenting and constraints require different reasoning and are excluded.

```python
# UNEXECUTED: preserve world placement while parenting ordinary unconstrained objects.
from mathutils import Matrix

world = child.matrix_world.copy()
child.parent = parent
child.matrix_parent_inverse = Matrix.Identity(4)
child.matrix_world = world
```

`Matrix.Identity(4)` is a 4×4 identity transform. This recipe relies on Blender decomposing the assigned placement; nonuniform parent scale combined with rotation can induce shear that a simple transform representation cannot preserve exactly. Compare evaluated world geometry after such a change. Do not claim “parenting always preserves shape” from plausible matrix algebra.

### Revise dimensions

`Object.dimensions` describes bounding-box size along the object's axes with scaling, not the dimensions of an axis-aligned world-space box. Its setter adjusts Object scale using cached evaluated bounds. Assigning dimensions repeatedly without updating can use stale bounds, and a zero-size axis cannot be expanded by scaling it. [C15](../CLAIMS.md#c15).

```python
# UNEXECUTED: isolated one-step dimensions revision, not intrinsic mesh redesign.
bpy.context.view_layer.update()
obj.dimensions = (2.0, 1.0, 0.5)
bpy.context.view_layer.update()
```

This changes scale; it does not rewrite a parameterized bevel width or guarantee constant world-space wall thickness. For procedural revision, prefer changing intrinsic dimensions in the constructor and rebuilding owned geometry. For exact world bounds, inspect evaluated vertices transformed into world space and compute coordinate minima/maxima. Record whether a requested dimension is local size, world size, centerline span or outside extent after modifiers.

### Curves

The selected API uses legacy `Curve`, created through `bpy.data.curves.new(name, type='CURVE')`, not the separate hair `Curves` datablock. `curve.splines.new(type)` creates a Spline with one point. `spline.points.add(count)` adds points to POLY/NURBS; `bezier_points.add(count)` is for BEZIER. To obtain N total points, add N−1. Allocation may invalidate old point wrappers, so allocate first, then fill.

```python
# UNEXECUTED: 3D polyline with a circular bevel, linked by the caller.
curve = bpy.data.curves.new('Path', type='CURVE')
curve.dimensions = '3D'
curve.resolution_u = 12
curve.render_resolution_u = 12
curve.bevel_depth = 0.05
curve.bevel_resolution = 3
curve.use_fill_caps = True
spline = curve.splines.new('POLY')
coords = [(0, 0, 0), (1, 0, 0.5), (1.5, 1, 0.5)]
spline.points.add(len(coords) - 1)
for point, xyz in zip(spline.points, coords):
    point.co = (*xyz, 1.0)
```

`SplinePoint.co` has four components `(x,y,z,w)`; the fourth is the rational weight for NURBS, set explicitly to 1 for this polyline. Bézier points use a 3D `.co` plus left/right handles and handle types such as `AUTO`, `VECTOR`, `ALIGNED`, `FREE`. Handles control interpolation, not additional Object transforms. NURBS order and endpoint/cyclic settings alter continuity and knot behavior. `use_cyclic_u` closes a spline; it is not the same as capping an open beveled tube.

`resolution_u` controls interpolation along the spline where applicable; render resolution zero means use the regular resolution. `bevel_resolution` controls profile tessellation; `bevel_depth` controls profile size; `extrude` supplies additional curve extrusion. They are local geometry parameters, so Object scale changes world-space thickness. Sharp POLY corners, self-intersections and tight curvature can produce intersections or undesirable caps. `dimensions='2D'`, fill mode and winding/tessellation affect planar filled shapes. A 2D fill algorithm is not a general robust solid-modeling kernel. Convert only the evaluated result when mesh inspection or static export is required, keeping the Curve ID editable in `.blend`.

### Modifier stack contracts

`Object.modifiers.new(name, type)` returns an owned Modifier appended to the stack. Modify its RNA properties directly; `remove(modifier)` deletes it, `move(from_index, to_index)` changes order. `show_viewport`, `show_render`, Edit Mode display and cage settings affect different evaluation/display routes. The type strings below identify classic modifier implementations; names are user-facing and may be uniquified.

| Modifier | Parameters requiring an explicit decision | Geometry and failure semantics |
|---|---|---|
| `ARRAY` / ArrayModifier | `fit_type='FIXED_COUNT'`, `count`, `use_relative_offset`, `relative_offset_displace`, `use_constant_offset`, `constant_offset_displace`, merge/caps | Count includes original. Relative offset depends on incoming mesh bounds; constant offset is local. Object offset composes transforms. Tiny fit-length displacement or excessive output can fall back to count 1 with an error |
| `BEVEL` / BevelModifier | `width`, `offset_type`, `segments`, `profile`, `affect`, `limit_method`, `angle_limit`, `use_clamp_overlap` | Width interpretation depends on offset mode. Angle is radians. Only eligible geometry is affected; clamping can reduce the requested width; normal hardening changes shading |
| `BOOLEAN` / BooleanModifier | `operation`, `operand_type`, `object`/`collection`, `solver`, self/hole tolerances where applicable | Operand evaluated geometry and relative transforms matter. `EXACT`, `FLOAT`, `MANIFOLD` have different assumptions. Missing operands/errors can return unchanged geometry; “Exact” is not proof of valid input or watertight output |
| `MIRROR` / MirrorModifier | `use_axis`, `mirror_object`, `use_clip`, merge threshold and bisect flags | Mirrors about local origin or another Object's coordinate frame; enabled axes compose. Merge acts near a threshold. Clipping is not a general Boolean union |
| `SOLIDIFY` / SolidifyModifier | `thickness`, `offset`, `solidify_mode`, rim options, even offset and clamp | Adds shells/rims using local-space distances. Simple mode cannot usefully handle edges shared by more than two faces. Complex mode still contains numeric limits and is not exact wall-thickness certification |
| `SUBSURF` / SubsurfModifier | `subdivision_type`, `levels`, `render_levels`, UV/boundary settings | CATMULL_CLARK smooths; SIMPLE subdivides. Topology grows rapidly. Viewport/render levels differ. Pinned source can defer final tessellation in background/render |
| `NODES` / NodesModifier | `node_group`, typed interface inputs, visibility | Executes a Geometry Nodes tree; graph validity and actual output component must be checked separately |

```python
# UNEXECUTED: object must already have suitable original mesh data.
bevel = obj.modifiers.new('EdgeRound', 'BEVEL')
bevel.width = 0.03
bevel.segments = 3
bevel.limit_method = 'ANGLE'
bevel.angle_limit = 0.5235987755982988  # 30 degrees in radians.
bevel.use_clamp_overlap = True
```

This produces an editable modifier configuration; it does not establish that the mesh was beveled. Evaluate and inspect. A Solidify-before-Bevel stack can round newly created rim edges, whereas Bevel-before-Solidify operates on the original sheet first. Array relative spacing depends on the geometry arriving at that point in the stack. Boolean before versus after bevel changes both topology and eligible edges. Stack order must be part of the model's reproducibility record.

Applying a modifier destructively changes original data and normally removes that modifier. It requires Object Mode and single-user data (or an explicitly chosen single-user conversion). Applying a non-first modifier is not equivalent to baking the entire visible stack in order; the source reports this explicitly. Prefer leaving the stack editable or obtaining a separate evaluated snapshot. [C16](../CLAIMS.md#c16).

## Implementation traces

`object.cc:3763 - 3807` uses cached bounds to derive scale; `rna_curve.cc:684 - 748` creates splines and adds the correct point type; `curve.cc:885 - 912` reallocates point storage. Classic Array `MOD_array.cc:450 - 551` derives offsets from incoming bounds and bounds copy counts. `MOD_bevel.cc:111 - 261` builds BMesh eligibility and calls the bevel kernel. `MOD_boolean.cc:159 - 218,527 - 612` distinguishes errors and evaluated operands. `MOD_mirror.cc:67 - 125` → `mesh_mirror.cc:118 - 200` establishes coordinate conversion and intermediate cleanup. `MOD_solidify.cc:56 - 68` dispatches two different algorithms; inspected callee ranges cover shell parameters and nonmanifold guards. `MOD_subsurf.cc:192 - 278` establishes deferred tessellation. [Pinned links](../SOURCE_TRACES.md).

## Failure modes and diagnosis

- **Wrong thickness after scaling:** distinguish local modifier parameter from world-space dimension.
- **Parented object shears or jumps:** check parent inverse, constraints, singular/nonuniform scale and decomposition limits.
- **Dimensions assignment seems ignored:** zero-size axis or stale evaluated bounds; inspect geometry, not just the property you wrote.
- **Curve has an extra point at origin:** added N instead of N−1, or failed to populate the initial point.
- **Array reports one copy:** zero/tiny offset, excessive copy count, missing curve cache or unsupported fit setup.
- **Boolean leaves original unchanged:** missing operand, unsuitable collection or reported solver failure; unchanged geometry is not necessarily successful difference.
- **Render has more faces than inspection:** different subdivision/render settings or delayed materialization.

## Evidence and open questions

D/S support coordinate, ordering and conversion distinctions. I recommends parameter rebuilding and independent evaluated measurements. The exact bounds of Boolean robustness, corner self-intersection of curves and Solidify thickness accuracy are intentionally not claimed. Fit Curve uses evaluated curve cache and a world-scale factor in pinned source; nonuniform scaling deserves a later test rather than extrapolating a simple “length” label. [T05 and T07](../FUTURE_TESTS.md).
