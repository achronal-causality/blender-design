# Glossary and command reference

Terms below connect the public Python surface to Blender's implementation. Exact parameters and inherited members remain available in the local [API index](API_INDEX.md); [modules](README.md#reading-map) explain the preconditions and effects used by the recipes.

## Process, code and evidence

| Term | Meaning here |
|---|---|
| Background Blender | The Blender application launched without the normal interactive UI lifecycle; it initializes Blender and embedded Python before running supplied code |
| Host process | The external caller that starts Blender, waits, preserves logs and checks output. The host illustration uses Python's standard library and does not import `bpy` |
| Bundled Python | Interpreter and standard library shipped inside this Blender application. Its standalone executable does not itself initialize Blender |
| `bpy` | Blender's Python application interface: stored data, current context, operators, registered types and application information |
| RNA | Blender's runtime property/type reflection system exposed to Python; many Python objects are wrappers around Blender-owned C/C++ data |
| `bpy_struct` | Common RNA wrapper interface, including property access and reflection. It is not an independently owned scene datablock |
| `bpy.types` | Registered Python-visible RNA type namespace; classes such as `Object` describe instances obtained or created through the data API |
| Operator / `bpy.ops` | Application action with polling, execution/invocation mode, reports and a status set; can require active context and mutate before reporting failure |
| Standard library | Modules delivered with Python, such as `pathlib`, `json`, `subprocess` and `hashlib`; no extra package installation is used by this reference |
| ABI | Binary interface expected by native extension packages; Python version, architecture and linked libraries must be compatible |
| CWD | Current working directory of a process; separate from the Python script's directory and the saved `.blend` directory |
| `__main__`, `__file__`, `sys.modules` | Script execution namespace, script filename and process-wide imported-module cache. A new main namespace does not clear the module cache |
| Exit code, signal, timeout | Distinct process outcomes. Zero return status is not an artifact-validity certificate; a native signal can bypass Python cleanup; timeout is a caller-enforced limit |
| SHA-256 / receipt | A content digest and its recorded provenance (URL/path, time, size). Matching hashes establish identical bytes to the receipt, not semantic correctness |
| Git blob hash | Repository content identity, computed from the blob header and bytes using SHA-1. Comparing it with the captured pinned repository tree checks source-byte correspondence separately from the acquisition receipt |
| D / S / R / I | Documentation / pinned source / reported experience / inference. [Claim ledger](CLAIMS.md) separates their roles |
| Complete selected unit | Every paragraph, note, parameter description and example in the selected unit, with inherited definitions read once. It does not mean recursive reading of every linked page |
| Source range | Actual inspected line interval of a pinned file; it does not imply a full-file or full-subsystem audit |
| Syntax validation | Parsing code into an abstract syntax tree (AST). It checks grammar without importing modules, resolving RNA properties or executing a Blender operation |

## Data and ownership

| Term | Meaning here |
|---|---|
| Main / `bpy.data` | Blender's database of original editable IDs in the current file/process. Evaluated and temporary geometry are different ownership categories |
| ID / datablock | Named, reference-counted Blender data such as a Mesh, Object, Material, Collection or NodeTree. `ID` supplies shared interfaces, including users and copying |
| Object | Transformable scene entity that can reference geometry data; its location/scale differ from coordinates stored in its Mesh or Curve |
| Mesh / Curve | Geometry datablocks; multiple Objects can refer to one, so editing the geometry can affect all those Objects |
| User / fake user | A Blender reference keeping an ID in use, or an explicit persistence marker. Neither is the number of Python variables referring to a wrapper |
| Collection | Grouping/linking of Objects and child Collections; an Object can belong to several. Linking does not duplicate geometry |
| Scene / ViewLayer | Scene owns scene-level settings and a root Collection; ViewLayer determines an evaluated/filterable view and active/selection state |
| Original / evaluated ID | Editable authoring data versus graph-produced state. Evaluated wrappers may be invalidated by the next update; copy needed numbers immediately |
| Temporary mesh | `Object.to_mesh` conversion owned by that Object's temporary storage, released by `to_mesh_clear`; not an original Main Mesh to link as new editable data |
| Shared / independent data | Copying an Object retains shared referenced data until explicitly copied. A Mesh copy can still share its Materials |
| Semantic key | Job-defined metadata such as `part_key='body'`; separate from a Blender display name. Requires ownership and uniqueness checks; not a built-in identity guarantee |
| Partial mutation | Earlier changes survive a later failing operation unless explicitly repaired; Python exceptions and context-manager exit are not scene rollback |
| Idempotent revision | Reapplying the same intended revision does not produce duplicate parts or unintended extra effects. A fresh-allocation helper is not automatically idempotent |

## Geometry, evaluation and coordinates

| Term | Meaning here |
|---|---|
| Dependency graph / Depsgraph | Evaluation structure relating original IDs to computed geometry and transforms for a scene/view layer and evaluation mode |
| Refresh versus lookup | Refresh evaluates tagged work; `ID.evaluated_get` only looks up corresponding evaluated data. Use an evaluation boundary after mutation |
| Local / world space | Coordinates relative to an Object's geometry origin versus scene world coordinates. Apply the correct evaluated world matrix before comparing global extents |
| Point / direction / normal | Point transforms include translation; direction transforms do not. Surface normals use the inverse transpose of the nonsingular linear transform and normalization |
| Radians / scene units | Rotation and angle values normally use radians. Mesh coordinates and many modifier lengths use scene/object-space units; UI unit display alone does not rewrite all geometry |
| Handedness / determinant | A negative determinant reverses coordinate orientation; negative scale can change winding interpretation and normal/export behavior |
| Vertex / edge / polygon / loop | A mesh point, connection between points, face, and face corner. A vertex can belong to multiple loops, allowing corner-specific UVs and split normals |
| Attribute / domain | Typed per-element data and the element set carrying it, such as point, edge, face or corner. Type/domain/count must match the intended geometry |
| Named / anonymous attribute | Explicit name usable at an external inspection boundary versus graph-managed attribute identity/lifetime |
| Normal / smooth shading | A direction used for surface orientation/lighting and interpolation policy. Smooth appearance does not add topology or certify a manifold solid |
| BMesh | Editable topology representation with explicit vertices/edges/faces/loops and connectivity, distinct from Mesh's compact arrays |
| Owned / wrapped BMesh | Caller-created BMesh that must be freed versus Blender's borrowed Edit Mode BMesh, which is updated through the edit-mesh API |
| Object Mode / Edit Mode | Different geometry-editing ownership/lifecycle. Compact Mesh storage can be out of date while Edit Mode owns current topology |
| Manifold / watertight | Topological properties with additional orientation/closure assumptions; `Mesh.validate` repairing structural faults is not a complete proof of either |
| Modifier stack | Ordered geometry operations on an Object. Evaluation preserves original data; applying a modifier changes original data and usually removes that operation |
| Tessellation | Conversion/subdivision into discrete geometry for a consumer; some subdivision materialization is delayed until demanded |
| GeometrySet | Evaluated Geometry Nodes container with potentially several geometry components and instance references; not necessarily only a Mesh |
| Node interface / socket / link | Group's exposed contract, typed input/output endpoint, and connection between endpoints. Labels differ from stable identifiers |
| Field | An expression evaluated over geometry elements in a consumer's context; it is not a Python list contained in a socket |
| Instance / realization / join | Referenced geometry placement; expansion into geometry; combination of geometry components. None of these inherently performs welding or Boolean union |
| Procedural noise | Numeric function evaluated in a shader or graph; it is not diffusion image generation and need not download an asset |

## Inspection and persistence

| Term | Meaning here |
|---|---|
| Cycles CPU | Bundled path-tracing engine configured for CPU rendering; reference choice without benchmark or integrator correctness claim |
| Sample / adaptive sampling / denoising | Rendering estimate contribution, convergence-dependent sample allocation, and post-estimation reconstruction. Each can affect apparent small features |
| Projection / clipping / DOF | Camera mapping to image, visible distance limits, and depth-of-field blur. These can hide geometry independently of modeling errors |
| Working space / display / view transform | Numeric color representation used for scene calculations, target display, and mapping of scene values to displayed values |
| OCIO / AgX | OpenColorIO configuration system and selected view transform. Effective configuration can change available enums and appearance |
| `.blend` | Editable Blender file storing selected persistent scene/datablock state; it does not automatically embed every external resource or the host program |
| PNG / RGBA / IHDR | Lossless raster file format, red/green/blue/alpha channels, and PNG's header chunk containing dimensions. Checking the header does not decode or judge pixels |
| OBJ / MTL | Static Wavefront geometry text and limited material sidecar. They discard the procedural construction and much Blender-specific scene/material information |
| Stale output | File left by a previous or failed attempt that could be mistaken for current success. Fresh exclusive directories and receipts help distinguish attempts |
| Reproducibility | Enough recorded version, inputs, parameters, environment and settings to reconstruct and explain a result; not a promise of bit-identical render pixels |

## Commands and environment reference

All Blender command examples are unexecuted except the identity diagnostics explicitly listed in [BASELINE](BASELINE.md#diagnostic-commands-and-fields). The following are reference routes, not instructions to run the later tests now.

| Command/interface | Where its arguments and effects are explained |
|---|---|
| Blender executable; `--version`; `/usr/bin/file`; bundled `python3.13 -I -B -c` | [Identity diagnostics](BASELINE.md#diagnostic-commands-and-fields) |
| `--background`, `-b`, `--factory-startup`, `--disable-autoexec`, `-Y`, `--python-exit-code`, `--python`, `-P`, `--`, `--output-dir` | [Startup and order](modules/01-execution.md#startup-and-argument-order); `--output-dir` belongs to the example script |
| `--python-expr`, `--python-text`, `--addons`, `--threads`, `--offline-mode` | [Execution alternatives](modules/01-execution.md#startup-and-argument-order); not required defaults |
| `--python-use-system-env`, `--python-use-user-env`; Python/Blender resource and color environment variables | [Environment table](modules/01-execution.md#environment-and-dependencies) |
| `--cycles-device` | [Cycles settings](modules/07-render.md#cycles-and-output-settings); Cycles-specific parser reads its argument after Blender's `--` separator |
| `rg`, `-n`, `-F`, `--glob` | [Filesystem search examples](README.md#search-locally) |
| `rg -i -l` | Validator's search modifiers: case-insensitive matching and matching filenames only, respectively; searches the review's module Markdown |
| `subprocess.run`, `Path`, `json`, `hashlib`, `struct`, exception classes | [Example standard-library contract](examples/README.md#standard-library-interfaces-used) |

## Research-only files

The Markdown files and captured sources are the deliverable; no helper installation is required. `research_fetch.py` retrieves public reference bodies and records receipts, `extract_articles.py` derives searchable article text from raw HTML, and the reading helpers/logs record explicit reading scope. `build_reference_indexes.py` and `build_claims.py` produce plain indexes from that evidence. These helpers are task-local research machinery, not a Blender execution framework.

`validate_reference.py` checks local links/headings, receipt hashes/sizes, pinned revision/range references, coverage accounting, example syntax and search discoverability. It uses only the Python standard library and `rg`. It does not import or execute the example modules. [Validation results and rerun command](VALIDATION.md).
