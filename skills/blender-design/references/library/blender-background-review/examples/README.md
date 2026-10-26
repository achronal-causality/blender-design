# Annotated examples: unexecuted

**All example code is unexecuted.** Validation parses syntax without importing `bpy`, `bmesh`, `mathutils` or these files. These functions describe intended patterns and failure boundaries; they are not a demonstrated capability or a tested production library.

## Read by question

| File/function | Parameters and return | Preconditions, mutation and failure |
|---|---|---|
| [mesh_patterns.py](mesh_patterns.py) `box_mesh(size)` | Three full local extents → original Mesh ID | Positive finite inputs; creates Main data, rejects repaired topology, cleans its own zero-user candidate on ordinary failure |
| `new_collection(scene, name)` | Scene and display name → Collection ID | Fresh build; links into master collection; repeated calls create more collections |
| `replace_body(collection, size)` | Owned Collection and dimensions → `(Object, previous Mesh or None)` | Unique semantic key, independent owned editable geometry; stages replacement but retains old data for caller's acceptance/recovery |
| `extrude_top(mesh, height)` | Original Mesh and positive local displacement → no return value | Object Mode; chooses upward faces with example-specific normal threshold; owned BMesh; writes back and frees; post-write failure does not restore old data |
| `copy_object(..., independent_geometry)` | Existing Object, Collection, new part key, boolean → Object | Deliberately shares/copies mesh; referenced materials remain shared; not a recursive dependency clone |
| `curve_object(collection)` | Owned Collection → Curve Object | Fresh-build only, one initial point plus two added, explicit 4D coordinates; profile/cap correctness unverified |
| `add_bevel(obj)` | Mesh Object → BevelModifier | Rejects duplicate name, explicit width/segments/angle; does not prove eligible edges changed |
| [instances.py](instances.py) `instance_graph(obj, count, spacing)` | Original mesh Object, count 2 - 100, positive spacing → `(modifier, tree)` | Builds new geometry group; preserves a modifier graph; exposes typed spacing, explicitly realizes. The count bound is an example parameter guard, not a research/example-count limit |
| [inspection.py](inspection.py) `configure(...)` | Scene, Collection, fresh Mesh Object, absolute PNG path → camera/light/material/world IDs | Changes assigned material slots and scene inspection settings; fixed illustrative view near origin; no render call |
| `aim(obj, target)` | Unparented Object, world target → no return | `Vector.to_track_quat('-Z','Y')` aligns local −Z toward target with +Y up; zero direction rejected; pole/roll behavior needs intentional framing |
| [persistence.py](persistence.py) `mesh_summary(obj)` | Geometry Object → Python dictionary of counts/world bounds | Fresh evaluation; assumes nonempty realized mesh component; copies numbers and frees temporary mesh |
| `save_render_export(...)` | Fresh output root, collection name, Object, provenance → script receipt | Saves `.blend`, requests PNG and OBJ/MTL; minimal transport checks only. Later host/reopen/visual acceptance remains required |
| [host_job.py](host_job.py) `run_job(...)` | Trusted job entry script, new root, timeout → verified-byte receipt | External process, exclusive directory, fixed Blender, logs, timeout, receipt and digest checks; does not import Blender |

No function automatically creates scenes merely by importing its file. A future job entry script must first check `bpy.app.version == (5, 2, 2)` and the build hash before calling any mutating function. Recheck the executable externally as well. For a fresh job, choose a factory/empty startup before retaining references; for a revision job, load the input and reacquire all data. Do not mix these modes.

## How to assemble a later job

The host receives a trusted Python entry script, not a conversation prompt evaluated with `exec`. That script parses its `--output-dir` option using the argument-tail pattern in [execution](../modules/01-execution.md), verifies identity first, chooses an owned scene/collection, calls selected construction functions, inspects expected geometry, configures rendering and calls the persistence function. It supplies source/parameter/input digests as `provenance`.

The persistence example hard-codes the inspection recipe's 768×768 PNG expectation. If a future test chooses another resolution, change its expectation deliberately. It summarizes a viewport graph, while OBJ is requested in render mode; set corresponding modifier levels equal or explicitly compare the difference. The code does not silently reconcile those modes. The material example applies to ordinary Mesh data; a Geometry Nodes primitive can supply different evaluated materials and needs its own material-assignment decision.

Do not blindly call all example functions: a curve and a box answer different construction questions; independent and shared copies answer opposite ownership questions; instance realization deliberately selects an output boundary. A repeated call to a fresh-build helper is not an idempotent revision API.

## Standard-library interfaces used

| Interface | Meaning in these examples |
|---|---|
| `math.isfinite`, `math.radians` | Reject NaN/infinity and convert degrees to the radians required by Blender rotation/angle properties |
| `pathlib.Path` | Filesystem path object; `resolve` normalizes to absolute, `is_absolute/is_dir/is_file/exists` inspect, `mkdir(exist_ok=False)` rejects reuse, `open('x')` creates a new file exclusively |
| `Path.read_bytes/read_text/write_text`, `stat().st_size` | Read/write data or inspect size; these operations can raise filesystem exceptions and are not scene-validity checks |
| `hashlib.sha256(...).hexdigest()` | Digest bytes to identify a captured/output file; does not certify content correctness |
| `json.dump/dumps/load(s)` | Serialize/parse a plain JSON receipt; only JSON-compatible values are allowed, not RNA wrappers |
| `struct.unpack('>II', bytes)` | Decode two unsigned 32-bit big-endian integers from PNG's IHDR width/height fields; does not decode pixels or validate all chunks |
| `subprocess.run(args, cwd, stdout, stderr, timeout, check=False)` | Launch fixed executable without shell interpolation, wait for completion, capture separate logs, raise `TimeoutExpired` on timeout; inspect `returncode` explicitly |
| `getattr/setattr` | Access literal or returned RNA property identifiers; they do not make an unknown property valid |
| `ValueError`, `RuntimeError` | Example's own rejected-input/contract-failure exceptions; distinguish them from Blender's errors by message and traceback |

Binary logs use `wb` so native output is preserved without decoding loss. Text artifacts use UTF-8 where specified. The examples do not install packages or modify environment variables. The host retains its ambient environment, so a future reproducibility record must describe relevant overrides as explained in [execution](../modules/01-execution.md).

## Shipped examples inspected

The pinned [background job template](../../../../../../docs/research-catalog.md#file-5362f1b9bd2869da) and [BMesh Object Mode](../../../../../../docs/research-catalog.md#file-bb6305495f88b577) / [Edit Mode](../../../../../../docs/research-catalog.md#file-38ba61ba4f34129d) templates were read in full. The background template demonstrates argument parsing, scene setup, save/render control and normal process completion. It assumes a particular startup and uses example defaults; it does not establish unique-output provenance, fail-closed acceptance, general camera framing or robust recovery. The BMesh Object Mode example copies data into caller-owned BMesh and writes it back; the Edit Mode example borrows Blender's mesh and updates it in place. Their different cleanup is intentional. Official provenance does not turn an illustrative script into a universal robust job runner.

The quickstart's included operator/panel examples were also read to resolve literal includes, but custom UI registration is outside the recommended background workflow. They were not executed.
