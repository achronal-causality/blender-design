# 08. Saving, reopening and export

## Purpose and prerequisites

Preserve editable procedural work and understand a bounded static export. Read [data](02-data.md), [evaluation](03-context.md), [nodes](06-nodes.md) and [rendering](07-render.md). References: [save/open operator entries](https://docs.blender.org/api/5.2/bpy.ops.wm.html), [OBJ manual](https://docs.blender.org/manual/en/5.2/files/import_export/obj.html).

## Mental model and invariants

A `.blend` file stores Blender datablocks and their relationships: authored mesh/curve data, modifiers, node graphs, materials, cameras, collections, scene settings and supported custom properties. It does not automatically store the Python process's locals, imported modules, external source scripts, arbitrary Python objects or every external file. Evaluated data is usually reconstructed from authored data/settings when needed. Preserve script and parameters alongside `.blend` if rebuildability matters.

OBJ is an interchange snapshot of selected geometry and a limited material description. It is not an editable procedural scene format and does not preserve the construction program. Save `.blend` before treating OBJ as a derived output. [C23 - C25](../CLAIMS.md#c23).

## API contracts

### Save and reopen

```python
# UNEXECUTED: absolute target inside a fresh job directory.
result = bpy.ops.wm.save_as_mainfile('EXEC_DEFAULT',
    filepath='/absolute/new-job/scene.blend',
    check_existing=False, compress=False, relative_remap=True, copy=False)
if result != {'FINISHED'}:
    raise RuntimeError(f'Save failed: {result}')
```

`filepath` is the destination `.blend`. `check_existing` participates in overwrite checking, especially interactive invocation; it is not a safe filesystem no-overwrite primitive for scripts. The caller must guarantee a fresh destination. `compress=False` produces an uncompressed file for the bounded recipe; compression preserves editability but changes bytes and container detection. `relative_remap=True` rebases relative resources to maintain their targets when saving elsewhere. `copy=False` makes this the current file; `copy=True` writes a copy while retaining the current file's path and restoring backed-up resource paths.

Saving can flush pending editor data, pack resources if autopack is enabled, invoke application callbacks, rotate save-version backups and write a temporary file. It is not side-effect-free and not a transaction over all referenced external resources. Configure final scene settings **before** saving if the saved file should contain them. A later render changing settings does not retroactively update the saved file.

`bpy.ops.wm.open_mainfile(filepath=..., load_ui=False, use_scripts=False)` loads data, with UI loading and automatic script execution disabled for this bounded revision recipe. It replaces Main and invalidates prior Object/Mesh/Collection wrappers. Reacquire everything through the new `bpy.data` and current context. These options do not make arbitrary untrusted `.blend` files a secure parser sandbox. The intended inputs are task-owned files.

`bpy.ops.wm.read_factory_settings(use_empty=True)` resets application data and can supply an empty scene baseline. It must run **before** acquiring references or adding task data. It resets more than a collection of objects; do not use it as a convenient cleanup inside a revision job. The reviewed examples only define it as an optional fresh-build step, never execute it during research.

### What survives and what remains external

| Item | Persistence requirement |
|---|---|
| Object/Mesh/Curve and modifier/node settings | Original IDs must be retained and saved; inspect after reopen |
| Otherwise unused assets | A real user or deliberate fake user is needed where applicable |
| Numeric/custom parameter metadata | Use supported serializable ID properties; store schema/version explicitly |
| Python script and modules | Keep sidecar source files, or deliberately create Text datablocks; a script executed from disk is not automatically embedded |
| Image textures/fonts/linked libraries | May remain external; packing supports some resource types, not a universal self-contained guarantee |
| Rendered PNG / OBJ / MTL | Separate files with their own paths and verification |
| Temporary/evaluated mesh or BMesh | Must deliberately convert/write into retained original data to persist |
| Process globals, handlers and imports | Not reconstructed merely by opening `.blend` |

`bpy.data.file_path_map()` gives ID-to-path information for resource auditing. `BlendData.file_path_foreach` offers path traversal/callback behavior, including metadata in 5.2; returning a replacement path is a mutation, so do not use it casually as a read-only audit. `bpy.path.abspath(..., library=...)` resolves a linked datablock's relative path with the correct library base. An empty or unsaved root, changed directory layout, differing case sensitivity and Unicode encoding can all matter.

Packing an image does not preserve the code that generated it, and a packed resource does not establish that every external dependency is packed. A useful reopen test checks expected IDs, parameter markers, node interfaces, modifier order and resolved resources, then compares evaluated summaries. A file's existence or size alone proves none of these.

### Blender's save failure behavior

Pinned `BLO_write_file_impl` writes to `filepath + '@'`, closes the stream, performs backup history and renames over the destination. On write failure it reports and removes the temporary output; on backup or rename failure an `@` file may remain. Error text distinguishes `Version backup failed (file saved with @)` from `Cannot change old file (file saved with @)`. This protects some failure paths but is not a claim of durable multi-file atomicity, crash-proof storage or transactional rollback of prior in-memory path remapping.

Do not rename a saved candidate `.blend` to another directory without considering its relative resource paths. Prefer a fresh job directory with stable final filenames and a completion receipt written only after checks; promotion can update an external pointer rather than moving the resource root. [Recovery module](09-revision.md).

### Static OBJ export

```python
# UNEXECUTED: `collection_name` identifies a verified job-owned collection.
result = bpy.ops.wm.obj_export('EXEC_DEFAULT',
    filepath='/absolute/new-job/geometry.obj',
    collection=collection_name, export_selected_objects=False,
    export_animation=False, apply_modifiers=True, apply_transform=True,
    export_eval_mode='DAG_EVAL_RENDER',
    forward_axis='NEGATIVE_Z', up_axis='Y', global_scale=1.0,
    export_uv=True, export_normals=True, export_materials=True,
    export_triangulated_mesh=False, export_curves_as_nurbs=False)
if result != {'FINISHED'}:
    raise RuntimeError(f'OBJ export failed: {result}')
```

`bpy.ops.wm.obj_export` is the built-in exporter; old `bpy.ops.export_scene.obj` examples refer to another interface. `collection` bounds the export by named Collection; validate ownership/name uniqueness first. `export_selected_objects=False` means selection is not an additional filter. `export_animation=False` bounds this to one static frame. `apply_modifiers=True` selects evaluated geometry; `export_eval_mode` chooses viewport or render evaluation explicitly. `apply_transform=True` incorporates Object placement. Turning it off can discard world placement in an OBJ that has no Blender parent/transform hierarchy.

`forward_axis='NEGATIVE_Z'`, `up_axis='Y'` converts Blender's +Y-forward/+Z-up convention to the selected receiver convention; `global_scale` multiplies exported coordinates. This does not add reliable physical units to OBJ. Document the intended axis and unit agreement with the receiver. Normals use an inverse-transpose transform; reflected geometry needs winding/handedness handling. A receiver can still interpret conventions differently.

`export_uv` includes supported active UV data; `export_normals` includes shading normals; neither exports every custom attribute. `export_triangulated_mesh=True` triangulates an export copy, not the original editable mesh. `export_curves_as_nurbs=False` converts curves to static geometry rather than preserving a NURBS curve representation. `export_materials` writes an MTL approximation; a procedural Noise/Mapping/Principled graph is not automatically baked or faithfully represented. Associated texture paths and MTL presence require separate verification. Object/material group options affect naming/grouping, not restoration of Blender's hierarchy. Optional vertex colors and PBR extensions depend on receiver support and are not portable guarantees.

### Information loss

OBJ loses modifiers, Geometry Nodes programs, per-instance procedural inputs, parent relationships, camera/world/light setup, editable curve controls when converted, constraints, most named attributes and Blender-specific material behavior. Static instance expansion may preserve visible placements while losing instancing semantics. Joining geometry is not welding it. MTL's limited material model and receiver interpretation can change appearance even when geometry is correct.

The native exporter uses evaluated material lookup, addressing the historical Geometry Nodes material-assignment problem for OBJ's route. The broader [R96721](../EXPERIENCE.md#r96721) remains open for other formats; its status is not evidence that current OBJ still has the same bug. Conversely, the fix does not make MTL equivalent to a shader graph.

## Implementation traces

`wm_files.cc:3965 - 4090` → `2190 - 2248` → `writefile.cc:1889 - 2086` establishes save dispatch, paths, temporary write/backup/rename and status. `wm_files.cc:1430 - 1466` shows Main replacement/reset. `io_obj.cc:89 - 138` returns success unless error reports exist; `obj_exporter.cc:280 - 422` can return early with **warning** “No information to write.” Consequently `FINISHED` can coexist with no output file. `obj_export_mesh.cc:38 - 176` selects evaluated/pre-modifier geometry, handles copies, reads evaluated materials and applies coordinate/normal transforms. [Pinned links](../SOURCE_TRACES.md).

## Failure modes and diagnosis

| Symptom | Interpretation |
|---|---|
| Saved file loses a datablock | Unused/unretained ID, wrong save timing, or unsupported transient data |
| Reopened script reference fails | Main was replaced; reacquire, do not reuse old wrappers |
| `.blend@` remains | Inspect save report for write/backup/rename stage; preserve evidence before retry |
| OBJ finished but missing | Empty filtered export can be a warning-only path |
| OBJ moved/rotated/scaled incorrectly | Axis convention, global scale or `apply_transform` mismatch |
| OBJ material differs | MTL approximation, missing external texture, slot mapping or receiver support |
| Newer `.blend` crashes/changes in older Blender | File format/forward compatibility is not semantic equivalence; stay on pinned baseline |

## Evidence and open questions

D/S substantiate save and export control flow. R includes forward-compatibility and material export cases; no reproduction attachments were run. I requires saved-scene plus output receipts and a bounded OBJ loss checklist. [T06, T08 - T10](../FUTURE_TESTS.md) specify reopen, missing resources, write failures, export and migration checks. File format compatibility does not warrant opening this output with arbitrary earlier Blender versions.
