# 10. Operational recipes and unresolved questions

## Purpose and prerequisites

Translate a concrete task into the smallest reviewed sequence. Start with [execution](01-execution.md), [ownership](02-data.md) and [evaluation](03-context.md). This module deliberately points to detailed contracts rather than duplicating all parameters.

## Mental model and invariants

Every recipe has an authored representation, an evaluation boundary, an inspection requirement and an output boundary. A successful API call is not interchangeable with achieving the intended shape. Recipe code is **unexecuted**; examples illustrate contracts and expected control flow. [Examples map](../examples/README.md).

## API contracts and task recipes

| Task | Sequence and prerequisites | Acceptance and principal failure |
|---|---|---|
| Create mesh | Allocate original Mesh → `from_pydata` → `validate` → link Object into owned Collection | Repairs must be explained; inspect topology/bounds, not only object existence. [Mesh](04-mesh.md) |
| Edit topology | Owned `bmesh.new` → `from_mesh` → explicit BMesh operation → `normal_update` → `to_mesh` → `free` | Object Mode; do not append multiple inputs unintentionally or reuse freed elements |
| Share geometry | `obj.copy()` then link | Confirm shared `.data` is intentional; copied ownership keys need revision |
| Independent copy | Object copy + Mesh copy, optionally material/group copies | Independence is layered, not recursive by default. [Data](02-data.md) |
| Make curve object | `curves.new('CURVE')` → explicit dimensions/resolution/bevel → spline points → Object link | Allocate N−1 extra points; verify rational weights and evaluated tessellation |
| Add modifier | `obj.modifiers.new` → explicit settings and order → evaluate | Input eligibility, visibility and report/no-op paths. [Transforms](05-transforms.md) |
| Make instance graph | Interface → nodes → identifier-checked links → typed modifier inputs → evaluate | Graph output must be Geometry; distinguish instances from mesh and decide realization. [Nodes](06-nodes.md) |
| Revise dimensions | Decide intrinsic versus transformed dimensions → change parameters or scale → refresh → inspect bounds | Stale cached dimensions and zero axes; don't substitute outside extent for local size |
| Inspect evaluated geometry | `evaluated_depsgraph_get` → `evaluated_get` → `to_mesh` → copy values → `to_mesh_clear` | No update/removal while borrowing; realize instances if needed. [Context](03-context.md) |
| Render inspection | Neutral material/world/light/camera → explicit Cycles CPU/color/output settings → synchronous render | Fresh PNG, correct projection/visibility; image does not prove topology. [Render](07-render.md) |
| Save editable output | Final settings/owned IDs → `save_as_mainfile` → artifact checks → later reopen | External resources and unused IDs. [Persistence](08-persistence.md) |
| Export static geometry | Bound collection → explicit evaluation/axes/scale → `wm.obj_export` → inspect OBJ/MTL | Empty warning-only success and information loss |
| Reopen and revise | New process → load own `.blend` → reacquire → validate keys/schema → staged revision → new output | No stale wrappers or silent rebuild destroying manual edits. [Revision](09-revision.md) |
| Recover after failure | Preserve attempt/logs → classify exception/status/native/timeout → repair cause → new process/root | Never accept stale files or silently pool failed attempts |

## Annotated examples

- [mesh_patterns.py](../examples/mesh_patterns.py): direct construction, BMesh extrusion, shared versus independent data, curve and modifier setup. Read comments as preconditions, not results.
- [instances.py](../examples/instances.py): bounded instance graph and typed exposed spacing input. Its explicit Realize Instances creates an inspectable mesh boundary.
- [inspection.py](../examples/inspection.py): new neutral Material/World and camera/light Objects; illustrative framing, not a universal camera fitter.
- [persistence.py](../examples/persistence.py): save/render/export operations and minimal artifact receipt, with caller-owned fresh directory.
- [host_job.py](../examples/host_job.py): external caller process lifecycle; no Blender import.

The examples are separate functions, not an installed framework or autonomous production pipeline. A future agent must choose the part parameters, scene ownership and expected observations, then assemble a test-specific entry script. Nothing here is evidence that any example executed successfully.

## Implementation traces

The recipe boundaries follow [source traces](../SOURCE_TRACES.md) and [claim ledger](../CLAIMS.md): startup → Main ownership → operator/context or direct RNA → dependency graph → temporary/persistent geometry → save/render/export reporting. Kernel internals not necessary for those observable boundaries remain outside the investigation. Individual modifier and node implementations were inspected at recorded functions, not counted as whole-file reviews.

## Failure modes and diagnosis

Use the [failure index](../FAILURE_INDEX.md) before trying another route. In particular, do not respond to a context error by introducing a UI bridge, an import error by installing standalone `bpy`, or poor render feedback by downloading a finished model. Those change this study's interface or capability question. Find the violated precondition within the selected route first.

## Evidence and open questions

| Question | Evidence boundary | Later resolution |
|---|---|---|
| Exact exit codes for script exceptions and `SystemExit` on the installed build | Source establishes separate paths; runtime not executed | T01 |
| Does partial mutation survive a caught exception and get saved? | API calls mutate before reports; no general rollback | T02 |
| Does repeated execution preserve unique parts and intended sharing? | Ownership policy inferred from ID semantics | T03 |
| Which bounded operator preconditions are sufficient without UI? | Poll/source reviewed, sample override unexecuted | T04 |
| Are lazy subdivision and instances materialized as intended by the inspector? | Source distinguishes graph evaluation, delayed tessellation and components | T05 |
| Do all desired custom properties, node input values and resources survive reopen? | Save format and ownership documented; no round trip performed | T06 |
| How do degenerate topology, normal settings and order affect specific shapes? | Validation/eligibility mechanisms inspected, shape-specific behavior unmeasured | T07 |
| Do all relevant render/export failures produce both useful status and no accepted stale artifact? | Warning-only/no-output path confirmed; installed behavior untested | T08 |
| What does the intended OBJ receiver retain and interpret? | Exporter behavior documented; receiver absent | T09 |
| Do old node-input recipes fail loudly or create inert custom properties? | Typed input consumption source-confirmed; legacy assignment runtime untested | T10 |

No unresolved item is silently promoted into a verified capability. These questions are sufficiently specific to design later tests without rereading the conversation. [Future tests](../FUTURE_TESTS.md) give expected observations and failure criteria.
