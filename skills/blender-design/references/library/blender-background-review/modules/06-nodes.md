# 06. Python-created node graphs

## Purpose and prerequisites

Build editable Geometry Nodes and material graphs through Python, and distinguish their construction from evaluation. Read [data](02-data.md), [evaluation](03-context.md), [mesh](04-mesh.md) and [transforms](05-transforms.md). References: [NodeTree](https://docs.blender.org/api/5.2/bpy.types.NodeTree.html), [Node](https://docs.blender.org/api/5.2/bpy.types.Node.html), [NodeTreeInterface](https://docs.blender.org/api/5.2/bpy.types.NodeTreeInterface.html), [5.2 migration](https://developer.blender.org/docs/release_notes/5.2/python_api/).

## Mental model and invariants

A node tree is an editable program. Nodes have typed sockets; links connect an output to an input. Creating nodes and links modifies that program, not its evaluated output. Geometry Nodes evaluation produces a GeometrySet containing components such as Mesh, curves and instances. A field is an expression evaluated over a particular geometry/domain, not a Python array you can read from its socket.

Keep three layers separate:

1. **Group interface:** exposed input/output declarations, including socket identifiers, types and defaults.
2. **Node sockets and links:** the internal program, including Group Input/Output nodes that expose interface sockets inside the tree.
3. **Modifier inputs:** per-modifier values assigned to a shared node group's interface. In 5.2 these use generated typed RNA under `modifier.properties.inputs`.

Two modifiers sharing a NodeTree share program edits while retaining their own input configuration. Destroying/recreating interface sockets changes identifiers and can break those configurations. [C17 - C19](../CLAIMS.md#c17).

## API contracts

### Construction and interface

`bpy.data.node_groups.new(name, 'GeometryNodeTree')` creates a geometry node group ID. A Material's `node_tree` is a shader tree owned by that Material; it is not created by assigning a free-standing geometry group to a material. `tree.nodes.new(bl_idname)` creates a node of the registered class, e.g. `GeometryNodeMeshCube`, not a UI label such as “Cube” or a legacy `.type` enum. The node type must be allowed in the tree; failure is reported.

`GeometryNodeTree.is_modifier` marks the group's intended modifier usage; the example sets it to `True`. It is metadata on the concrete geometry tree type, not a call that evaluates the graph, installs it on an Object or guarantees valid output. [Complete concrete type reference](../../../../../../docs/research-catalog.md#file-215dd57d3071b380).

`tree.interface.new_socket(name, description='', in_out='INPUT'|'OUTPUT', socket_type=..., parent=None)` returns an interface socket. `socket_type` uses a registered socket type such as `NodeSocketFloat` or `NodeSocketGeometry`; a placeholder enum in generated HTML is not the complete set. Its `identifier` is the key used to connect interface and per-modifier configuration. `items_tree` includes panels as well as sockets: filter by `item_type` and direction before assuming an item is an input. Removing/moving items changes interface structure; preserve identifiers when revising a public parameter.

`tree.nodes.new('NodeGroupInput')` and `'NodeGroupOutput'` create boundary nodes. Their sockets update from the interface. The Geometry Nodes modifier requires an active Group Output and its **first output interface socket must be Geometry**. Empty, wrong-type or unevaluable graphs can clear geometry and report an error, rather than raising a convenient construction-time exception.

### Links and values

`NodeLinks.new(input, output, verify_limits=True, handle_dynamic_sockets=False)` returns a NodeLink or can fail for invalid sockets. The Python parameter names are counterintuitive relative to the familiar output→input diagram; use explicit keywords `input=destination_socket, output=source_socket`. The pinned implementation recognizes and swaps direction where needed. Both sockets must belong to the same tree; identical directions report an error. A link existing is not proof of type compatibility at evaluation.

With `verify_limits=True`, creating a link can remove existing links at sockets whose limits are exceeded; it also removes duplicate links into a multi-input socket. It is not append-only. `handle_dynamic_sockets` permits node-specific insertion handling; leave it false for this bounded static palette. A node's `inputs`/`outputs` collections return sockets, while `.default_value` sets an **unlinked** input or value-output parameter. A linked input's default is not the driving value. `NodeSocket.links` traverses tree links and is documented O(number of links), so repeated per-socket inspection can be expensive.

Names are presentation labels and can repeat. Math inputs may all display “Value” while identifiers are `Value`, `Value_001`, `Value_002`; Vector Math similarly uses `Vector_001`. Noise's displayed Factor has identifier `Fac`. Mesh Line's endpoint mode relabels `Offset` as End Location without changing the underlying socket. Prefer identifier lookup with explicit uniqueness checks. Mode changes can alter availability or structure; reacquire sockets after changing modes.

```python
# UNEXECUTED: helper for the pinned palette; fails instead of guessing.
def socket_by_id(sockets, identifier):
    matches = [s for s in sockets if s.identifier == identifier]
    if len(matches) != 1:
        raise RuntimeError(f'Expected one socket {identifier!r}, got {len(matches)}')
    return matches[0]
```

### Blender 5.2 migration

```python
# UNEXECUTED: one exposed Float input, after constructing `tree`.
parameter = tree.interface.new_socket(name='Spacing', in_out='INPUT',
                                      socket_type='NodeSocketFloat')
parameter.default_value = 1.25
modifier = obj.modifiers.new('Procedure', 'NODES')
modifier.node_group = tree
input_properties = getattr(modifier.properties.inputs, parameter.identifier)
input_properties.value = 1.5
```

The interface default is the group's default; the modifier value is the instance's setting. `getattr` accesses the generated RNA attribute by the identifier actually returned, not a guessed `Socket_2`. Float/vector/color/int inputs can support a `.type` choice between a literal `VALUE` and `ATTRIBUTE`, with `.attribute_name` selecting a named attribute field where allowed. The exact available choices depend on the interface's socket and structure type. Inspect/reacquire the generated properties after interface edits.

Older recipes such as `modifier['Socket_2'] = value` are not the 5.2 typed-input contract. They may set unrelated custom metadata without supplying the input consumed by evaluation. The source builds the `inputs` property group from interface identifiers and reads its typed `value` or attribute field. A compatibility-note intermediate example differs from this final structure; the pinned implementation resolves the conflict. [C18](../CLAIMS.md#c18).

`structure_type` describes whether an interface accepts single values, fields or other supported structures. Historical `force_non_field` advice and old group `.inputs.new(...)` patterns must not be copied blindly. Transform Geometry's Mode is an input socket in this pinned declaration; don't assume the old node property exists. Keep exact type/socket identifiers in the job's expected schema and fail on drift.

### Bounded Geometry Nodes palette

| Node identifier | Inputs/outputs and execution semantics |
|---|---|
| `NodeGroupInput`, `NodeGroupOutput` | Internal access to declared interface; active output connectivity determines what the modifier returns |
| `GeometryNodeMeshLine` | Count/Resolution, Start Location, Offset → Mesh. Offset mode creates regularly spaced vertices and edges, no faces. Endpoint resolution can leave a remainder; total-count mode with one point uses zero displacement |
| `GeometryNodeMeshCube` | Size vector and Vertices X/Y/Z → Mesh, anonymous UV Map. Default two vertices per axis makes a boundary mesh; this is not volumetric material filling |
| `GeometryNodeTransform` | Geometry, Mode, Translation/Rotation/Scale or Transform matrix → Geometry. Changes components/instance transforms in geometry space; mode controls used sockets |
| `GeometryNodeInputPosition` | Position field from the geometry context in which a downstream consumer evaluates it |
| `GeometryNodeSetPosition` | Geometry, Selection, Position, Offset → Geometry. New positions are Position + Offset evaluated from the input context; instance positions affect origins, not their internal points |
| `GeometryNodeInstanceOnPoints` | Points, Selection, Instance, Pick Instance, Instance Index, Rotation, Scale → Instances. Uses points/mesh vertices/curve points; rotations and scales can be fields. Does not produce one Main Object per instance |
| `GeometryNodeRealizeInstances` | Geometry, Selection, Realize All, Depth → Geometry. Selected instance references expand into geometry; Realize All overrides depth, depth zero does not realize. More memory/topology can result |
| `GeometryNodeJoinGeometry` | Multi-input Geometry → Geometry. Concatenates compatible components; does not weld coincident vertices or perform a Boolean union |
| `ShaderNodeMath` | Float values and `.operation` → Value. Operation selects arguments/labels and domain behavior; explicit arithmetic, no generic Python exception contract for invalid mathematical inputs |
| `ShaderNodeVectorMath` | Vector operands/Scale and `.operation` → Vector and/or Value. Use the output appropriate to the operation; dot product is scalar, vector scale uses a scalar input |

**Construction example:** [instances.py](../examples/instances.py) creates a mesh line, instances a cube at each point, then explicitly realizes geometry before the Group Output. The expected repeated shapes follow the graph design; no vertex count or rendered result has been observed. The example names every node, connects by identifier and leaves a modifier/group as editable output. Removing Realize Instances changes what a mesh-only inspector can see even if the render still shows instances.

A field is evaluated where consumed: reusing Position before and after Set Position can produce different values. Anonymous attributes have graph-managed lifetimes; named attributes are the appropriate boundary when an external inspector needs a stable name/domain contract. Realization propagates attributes according to type/domain rules, and conflicts can prefer geometry's values over instance values. “Realized” does not mean “welded,” “closed” or “one Object per copy.”

### Bounded shader palette

| Node identifier | Meaning and parameters to make explicit |
|---|---|
| `ShaderNodeOutputMaterial` | Surface shader, Volume, Displacement, Thickness; active output and engine target matter. Neutral inspection uses only Surface |
| `ShaderNodeBsdfPrincipled` | Base Color, Metallic, Roughness, IOR, Alpha and layered weights. Set a neutral opaque material; leave Normal and Displacement unconnected for geometric inspection |
| `ShaderNodeRGB`, `ShaderNodeValue` | Constant Color or scalar output via `.outputs[...].default_value`; RGB may be labeled Color in the UI |
| `ShaderNodeTexCoord` | Generated/Normal/UV/Object/Camera/Window/Reflection coordinates. Choose a coordinate system deliberately; missing UVs are not the same as Object coordinates |
| `ShaderNodeMapping` | Vector with Location/Rotation/Scale, `.vector_type`. POINT transforms positions, VECTOR omits translation, NORMAL uses the appropriate normal transform, TEXTURE reverses the apparent mapping convention |
| `ShaderNodeTexNoise` | `.noise_dimensions`, `.noise_type`, normalize; Vector/W, Scale, Detail, Roughness, Lacunarity, Offset/Gain where available, Distortion → Factor/Color. Procedural numeric noise, not diffusion generation |

Increasing noise Detail changes octave complexity, not mesh topology. A texture connected only to Base Color cannot create geometry. Noise sampled on regular integer grids can show degenerate or repeating values; coordinate choice is part of the procedural definition. Shader graph construction shares Node/NodeSocket/NodeLink rules but runs in a shader evaluation context, not the Geometry Nodes field domain.

## Implementation traces

`rna_nodetree.cc:1259 - 1325,1425 - 1532` validates node types/tree membership and handles link limits. `rna_node_tree_interface.cc:729 - 774` resolves supported socket types and updates invariants. `rna_modifier.cc:1875 - 1983` exposes the node group and generated properties. `geometry_nodes_srna.cc:75 - 127,200 - 227` builds the per-interface input structure; `node_socket.cc:1512 - 1546` supplies Float `value` and evaluation flags; `geometry_nodes_execute.cc:126 - 232,554 - 656` reads inputs and executes the lazy graph. `MOD_nodes.cc:1760 - 1905` checks output shape and returns empty mesh components when necessary. [Node declaration/execution ranges](../SOURCE_TRACES.md) cover every palette type without claiming the entire shader or realization kernel was audited.

## Failure modes and diagnosis

| Symptom | Check |
|---|---|
| `Node type ... undefined` | `bl_idname`, registered type and tree compatibility |
| `Same input/output direction of sockets` | Wrong endpoints; socket label is not direction |
| `Node group's first output must be a geometry` | Interface ordering, not merely an internal Geometry link |
| `Cannot evaluate node group` / empty result | Invalid tree, cycle or missing output; inspect geometry counts and graph diagnostics |
| Input assignment has no effect | Legacy ID property, wrong identifier, linked socket default, shared tree versus per-modifier input confusion |
| Socket disappeared or changed type | Node mode/interface migration; reacquire and validate schema |
| Render shows copies, `to_mesh` seems empty | Instances versus mesh component; realize or inspect instances separately |
| Joined parts still have seams | Join Geometry concatenates; it does not weld or Boolean |

## Evidence and open questions

D/S establish typed input paths, graph preconditions and the execution boundary. R160212 concerns forward compatibility with older Blender, not failure to construct nodes in this baseline. I recommends explicit schema checks and realization at static inspection/export boundaries. [T05, T09 and T10](../FUTURE_TESTS.md) cover instances, attribute retention, OBJ losses and migration. The runtime moment at which every generated input property refreshes after interface mutation remains a test question; do not cache nested RNA wrappers across that mutation.
