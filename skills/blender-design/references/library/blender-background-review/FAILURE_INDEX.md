# Failure index

Search literal diagnostic text with `rg -F`, or search a symptom. Strings containing `...` are patterns, not exact complete messages. A symptom does not identify a unique cause. **D/S** entries describe documentation or inspected implementation; **R** entries are historical reports; **I** entries are recommended diagnosis. No entry is an observed capability-test result on this installation.

## Exceptions and diagnostic text

| Search text | Interpretation and first check | Evidence / route |
|---|---|---|
| `ModuleNotFoundError: No module named 'bpy'` | Check which executable launched Python; bundled standalone Python alone does not initialize Blender | [Execution](modules/01-execution.md), D/S/I |
| `ImportError`, incompatible architecture, wrong Python version | Inspect helper path, native package ABI/ARM64 and environment integration; do not install into Blender during this research | [Environment](modules/01-execution.md#environment-and-dependencies), [R72807](EXPERIENCE.md#r72807) |
| `ReferenceError`, `StructRNA ... has been removed` | A Python wrapper outlived its datablock; reacquire after removal, reset or file load | [Ownership](modules/02-data.md), D/S |
| `BMesh data ... has been removed`, invalid `BMVert` / `BMFace` | Freed/invalid wrapper or removed topology element; distinguish owner and element lifetimes | [BMesh](modules/04-mesh.md), [R105715](EXPERIENCE.md#r105715) |
| `poll() failed, context is incorrect` | Operator eligibility failed; check actual scene/view layer, active/editable data, mode and UI requirement | [Context](modules/03-context.md), [R6101](EXPERIENCE.md#r6101) |
| `TypeError` with positional override dictionary | Legacy invocation shape; use `Context.temp_override` and the pinned operator signature | [Context](modules/03-context.md), D/S |
| `1-2 args execution context is supported` | **Historical diagnostic only.** Useful for finding older override recipes, not promised current wording | [Context](modules/03-context.md), R/I |
| `Dependency graph update requested during evaluation` | Reentrant update; keep mutation/evaluation outside an already running evaluation callback | [Evaluation](modules/03-context.md), S |
| `Node type ... undefined` | Registered `bl_idname` and tree compatibility, not UI label or translated name | [Node construction](modules/06-nodes.md#construction-and-interface), D/S |
| `Same input/output direction of sockets` | Reversed or same-direction link endpoints; both must belong to the same tree | [Links](modules/06-nodes.md#links-and-values), S |
| `Node group's first output must be a geometry` | First exposed output interface socket has wrong type/order | [Nodes](modules/06-nodes.md), S |
| `Cannot evaluate node group` | Construction succeeded but executable graph was unavailable; inspect output/links and resulting components | [Nodes](modules/06-nodes.md), S |
| `OBJ Export: No information to write` | Export scope yielded no exportable objects; warning can coexist with `FINISHED` and no OBJ file | [Persistence](modules/08-persistence.md), [C25](CLAIMS.md#c25), S |
| `PermissionError`, `FileNotFoundError`, `OSError` | Filesystem operation failed; inspect absolute path, parent directory, permissions and partial files | [Execution](modules/01-execution.md), [recovery](modules/09-revision.md), D/I |
| `SystemExit`, `TimeoutExpired`, nonzero `returncode` | Separate explicit Python exit, host timeout and process failure; retain each observation | [Execution](modules/01-execution.md#exit-and-completion), D/S/I |
| `SIGPIPE`, hang after `Blender quit`, JACK messages | Historical shutdown/pipe/audio reports; preserve logs rather than applying a historical workaround as a current diagnosis | [R129657](EXPERIENCE.md#r129657), [R99755](EXPERIENCE.md#r99755) |
| `ArchWarn: ARCH_CACHE_LINE_SIZE != Arch_ObtainCacheLineSize()` | Observed in identity diagnostic with zero exit; cause unresolved, no rendering conclusion | [Baseline](BASELINE.md#observed-identity), observed diagnostic |

Example-defined errors such as `Ambiguous owned part: body`, `Blender baseline drift`, `Expected one socket`, `Missing or empty output`, and `Output digest mismatch` are **proposed application diagnostics**. Their presence in source is not evidence that Blender emitted them. [Examples](examples/README.md).

## Symptoms without a reliable exception

| Symptom / search terms | What to distinguish | Route |
|---|---|---|
| Duplicate object; `.001` suffix | Fresh allocation versus idempotent revision; display names versus semantic keys | [Revision](modules/09-revision.md) |
| Editing one object changes another | Shared Mesh/Material/NodeTree, separate Object transforms | [Data](modules/02-data.md) |
| Object exists but is absent from scene/render | Main allocation versus collection linking, view-layer exclusion, visibility and camera framing | [Data](modules/02-data.md), [render](modules/07-render.md) |
| Geometry unchanged; dimensions wrong after assignment | Deferred evaluation, cached dimensions, wrong graph mode, disabled modifier or original data inspection | [Context](modules/03-context.md), [transforms](modules/05-transforms.md) |
| Empty mesh despite visible instances | Instances versus mesh component; explicit realization or instance iteration required | [Nodes](modules/06-nodes.md) |
| Mesh vanishes after second conversion | Temporary `to_mesh` result replaced/cleared or evaluated owner invalidated | [Evaluation](modules/03-context.md) |
| Modifier returns no visible change; apply finished but stack remains | Eligibility/empty input/diagnostics and application path; status is not resulting geometry | [Modifiers](modules/05-transforms.md), [C16](CLAIMS.md#c16) |
| Cracks, flipped shading, invisible faces, distorted bevel | Topology/winding, split normals, negative/nonuniform scale, modifier order and material/lighting | [Mesh](modules/04-mesh.md), [transforms](modules/05-transforms.md), [render](modules/07-render.md) |
| Node value assignment has no effect | Linked socket default, legacy ID property, wrong identifier, shared tree versus modifier input | [5.2 migration](modules/06-nodes.md#blender-52-migration) |
| Black, clipped, cropped, washed-out or noisy PNG | Camera/light/world, render visibility, exposure/view transform, border, denoising and resolution | [Render](modules/07-render.md) |
| Render finished; missing PNG; stale output accepted | `write_still`, output path, report/status, exclusive attempt root and matching receipt | [Recovery](modules/09-revision.md), [T08](FUTURE_TESTS.md#t08-renderexport-failure-and-stale-output) |
| Reopened scene loses resources or edits | External paths, zero-user data, unsaved mutation or different input file | [Persistence](modules/08-persistence.md) |
| OBJ shape/material/orientation differs | Evaluation mode, axes/scale, triangulation and unsupported editable/material data | [Persistence](modules/08-persistence.md), [T09](FUTURE_TESTS.md#t09-static-export-information-loss) |

## Diagnosis order

Preserve the first failing attempt. Check identity and command → traceback/reports/return status → live ownership/context/evaluation → expected geometry → fresh output bytes → later reopen or visual semantics. Do not purge evidence or rerun into the same output location to make an ambiguous result appear successful. [Recovery contract](modules/09-revision.md).
