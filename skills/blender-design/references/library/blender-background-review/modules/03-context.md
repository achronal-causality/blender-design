# 03. Context, operators and evaluation

## Purpose and prerequisites

Separate direct datablock access, UI-style operator execution and evaluated geometry. Read [ownership](02-data.md). References: [Context](https://docs.blender.org/api/5.2/bpy.types.Context.html), [Depsgraph](https://docs.blender.org/api/5.2/bpy.types.Depsgraph.html), [Object](https://docs.blender.org/api/5.2/bpy.types.Object.html).

## Mental model and invariants

`bpy.data` addresses stored data. `bpy.context` describes the active operating context: scene, view layer, active object, mode and, when available, window/area/region. An operator (`bpy.ops...`) models an application operation and can depend on these context members. Direct RNA assignment usually has fewer selection/UI preconditions; it is not universally context-free, and it may only tag work for later evaluation.

The dependency graph maps original editable IDs to evaluated state after modifiers, parenting, constraints and other dependencies. Original mesh data answers “what was authored?” Evaluated data answers “what geometry is currently produced by this graph?” A graph has an evaluation mode, scene and view layer. A background process is not automatically a render-mode graph. [C07 - C09](../CLAIMS.md#c07).

## API contracts

### Direct operations versus operators

Use direct API for mesh creation, coordinates, object transforms, collection links, modifier settings and node construction. Use operators where the reviewed public workflow provides an application operation: save/open, render, OBJ export or deliberately applying a modifier. BMesh operators are a different API (`bmesh.ops`), accepting an explicit BMesh and not a UI context.

`bpy.ops.object.modifier_apply('EXEC_DEFAULT', modifier=name, ...)` dispatches immediately through the execute callback. `INVOKE_DEFAULT` asks the application to invoke an operation, potentially opening UI or starting modal behavior. `RUNNING_MODAL` is not job completion. Operator results are sets of status identifiers such as `{'FINISHED'}` or `{'CANCELLED'}`. Reports with error severity can become a Python `RuntimeError` even after some mutations. No general rollback is promised.

`operator.poll()` checks eligibility in the **current** context and returns a boolean; it does not validate every parameter or future geometry. Call it in the same override in which execution will happen. A successful poll is not an output guarantee. The pinned callable accepts execution mode and undo control as positional arguments, with operation properties as keywords. The legacy first-positional override dictionary is not the reference interface in 5.2.

### Set an actual context

`bpy.context.view_layer.objects.active = obj` sets the active object of that ViewLayer. `obj.select_set(True, view_layer=...)` changes selection; selection and active state are separate. The Object must belong to the relevant ViewLayer. `bpy.context.active_object` itself is read-only. Mode is application state; setting an Object property is not equivalent to entering Edit Mode.

```python
# UNEXECUTED: apply one modifier on a known local, single-user mesh Object.
import bpy

if obj.mode != 'OBJECT' or obj.data.users != 1:
    raise RuntimeError('Expected Object Mode and independent mesh data')
with bpy.context.temp_override(object=obj, active_object=obj,
                               selected_objects=[obj],
                               selected_editable_objects=[obj]):
    if not bpy.ops.object.modifier_apply.poll():
        raise RuntimeError('Modifier apply context rejected')
    result = bpy.ops.object.modifier_apply('EXEC_DEFAULT', modifier=modifier_name)
if result != {'FINISHED'} or obj.modifiers.get(modifier_name) is not None:
    raise RuntimeError('Modifier was not conclusively applied')
```

`temp_override` temporarily replaces supplied context members and restores valid prior members on exit. It does not create a real window or editor region. If supplying `window`, `screen`, `area`, or `region`, their membership must be consistent. If file loading or another operator destroys the old context, restoration cannot recreate it. It is a context manager, not a scene transaction. The example requires the object already in the active scene/view layer; an override is not a replacement for collection membership. Selection changes outside an override require explicit restoration if the job promises to preserve them.

`Context.temp_override`'s returned manager exposes `logging_set` for context-access logging; use it for diagnosis rather than guessing UI requirements. UI operators requiring a viewport cannot be made reliable headlessly by assigning a fabricated `area`. [Historical context reports](../EXPERIENCE.md#r6101), [C07](../CLAIMS.md#c07).

### Obtain current evaluated geometry

`Context.evaluated_depsgraph_get()` ensures an evaluated graph for the current scene/view layer in ordinary writable execution. `ViewLayer.update()` updates tagged data in that layer. `Depsgraph.update()` explicitly updates and can invalidate evaluated references; it rejects an update requested during evaluation. These are boundaries, not harmless getters when retaining evaluated wrappers.

`ID.evaluated_get(depsgraph)` (inherited as `Object.evaluated_get`) **does not ensure evaluation**. It returns the last corresponding evaluated ID; source delegates to graph lookup. Always establish a fresh evaluation boundary after edits before reading the result. [C08](../CLAIMS.md#c08).

```python
# UNEXECUTED: copy evaluated mesh coordinates into Python-owned world-space tuples.
import bpy

dg = bpy.context.evaluated_depsgraph_get()
evaluated = obj.evaluated_get(dg)
mesh = evaluated.to_mesh(preserve_all_data_layers=True, depsgraph=dg)
try:
    if mesh is None:
        raise RuntimeError('Expected convertible mesh geometry')
    world = evaluated.matrix_world.copy()
    points_world = [tuple(world @ v.co) for v in mesh.vertices]
    face_count = len(mesh.polygons)
finally:
    evaluated.to_mesh_clear()
```

`Object.to_mesh(preserve_all_data_layers=False, depsgraph=None)` returns a temporary Mesh for supported object types. The returned coordinates are object-local; multiply by the evaluated object's world matrix for world-space positions. Requesting all data layers requires a dependency graph. The result belongs to the Object's temporary conversion storage; a second `to_mesh` clears the previous result. Pair each acquisition with `to_mesh_clear()` on **the same Object**, and do not update/load/delete the owner during that lifetime.

This example extracts the mesh component. It does not prove it includes all un-realized Geometry Nodes instances. If mesh inspection is the goal, explicitly Realize Instances in the graph or separately inspect the dependency graph's instance iterator. [Node module](06-nodes.md).

`bpy.data.meshes.new_from_object(evaluated, preserve_all_data_layers=True, depsgraph=dg)` creates a persistent Main Mesh suitable for linking to an original Object. The implementation converts geometry, remaps ID references, moves storage into Main and removes anonymous attributes. This differs from the temporary `to_mesh` result, which must not be attached as an original object's data. Conversion can produce an empty mesh in certain failure/empty cases; inspect counts and expected attributes rather than accepting a non-null handle. [C09](../CLAIMS.md#c09).

### Inspection contracts

- `Depsgraph.object_instances` iterates evaluated placements. Entries and evaluated wrappers are transient; copy `matrix_world`, names/keys and numeric values during iteration. A single Object can have many instance placements.
- `Object.bound_box` supplies object-space bounding-box corners; unavailable data can use sentinel values. Transform corners for a world-axis-aligned bound, or calculate bounds directly from evaluated points when exact mesh bounds are required.
- `Object.dimensions` is not a world-axis-aligned bounding box; see [transforms](05-transforms.md).
- `Object.ray_cast(origin, direction, ..., depsgraph=...)` operates in object space. `Scene.ray_cast(depsgraph, origin, direction, ...)` uses world space. Treat a missing original face index as possible after topology changes; original polygon index is not a universal evaluated-face identity.
- `Scene.frame_set(frame, subframe=...)` performs the scene update associated with a frame change. Assigning `frame_current` is not an equivalent synchronization recipe. Animation authoring is excluded, but imported files may contain drivers or frame-dependent data.
- Modifier `show_viewport` and `show_render`, subdivision `levels` and `render_levels`, and ViewLayer exclusions can produce different viewport/evaluated inspection and render geometry. Choose and record the intended comparison mode.

## Implementation traces

`ops.py:1 - 65` exposes native callables. `bpy_operator_function.cc:115 - 435` parses arguments, checks writable context, polls, converts parameters, updates the active view layer and turns error reports into exceptions. `bpy_operator_wrap.cc:29 - 120` concerns registration/deferred properties, not the entire built-in execution path. `bpy_rna_context.cc:180 - 520` checks real UI membership and restoration.

`rna_ID.cc:757 - 782` is lookup only. `rna_context.cc:226 - 243` → `context.cc:1752 - 1762` → `scene.cc:2749 - 2835` provides the evaluation boundary. `rna_object_api.cc:426 - 451` → `object.cc:5601 - 5622` → `mesh_convert.cc:860 - 1055` establishes conversion ownership/cleanup. `rna_depsgraph.cc:285 - 321` rejects recursive update. `object_modifier.cc:1257 - 1345,1991 - 2078` checks mode/users, may mutate multiple objects, and does not make the status alone a complete success predicate. [Pinned links](../SOURCE_TRACES.md).

## Failure modes and diagnosis

| Failure | Diagnosis and correction |
|---|---|
| `poll() failed, context is incorrect` | Wrong mode/active data/UI requirement; prefer a direct-data equivalent or establish documented real context |
| Positional `TypeError`; historical search text `1-2 args execution context is supported` | Old override-dictionary recipe; use `temp_override`. The quoted text is a legacy diagnostic, not the pinned native callable's promised error wording |
| `Dependency graph update requested during evaluation` | Reentrant evaluation; move edits/inspection outside callbacks/evaluation |
| Geometry unchanged after assignment | Original data read, no refresh, wrong graph/view layer, disabled modifier, or instances not realized |
| Mesh disappears after another conversion | Prior temporary mesh invalidated by repeated `to_mesh` |
| Apply reports finished but modifier remains | Partial/no application path; verify the target stack and resulting geometry |
| Camera conversion unexpectedly raises | Unsupported conversion target; pinned RNA is stricter than illustrative docs |

## Evidence and open questions

D/S distinguish lookup from refresh and temporary from persistent meshes. R's stale-light report is unresolved and contradicted by other users; it is not proof that background evaluation is broken. I recommends fresh graph acquisition and copied inspection values. [T04 - T05](../FUTURE_TESTS.md) check context failure, evaluated topology, instances and lifetime. Exact visibility-dependent evaluation and subdivided-mesh materialization remain concrete runtime questions.
