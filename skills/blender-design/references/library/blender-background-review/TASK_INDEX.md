# Task index

Start at the task, follow its prerequisite, then read the API contract before adapting an example. Every example is unexecuted. “Accept” below describes a later check, not an observed result. [Reading map](README.md#reading-map), [API index](API_INDEX.md), [failure index](FAILURE_INDEX.md).

| Task / search terms | Start here and prerequisites | Interfaces and acceptance boundary |
|---|---|---|
| Start background Blender; run Python; parse arguments | [Execution](modules/01-execution.md#startup-and-argument-order), [baseline](BASELINE.md) | Fixed executable, `--background`, `--python-exit-code`, `--python`, script tail after `--`; process and artifact status are separate |
| Import local helpers; find resources; use relative paths | [Imports and paths](modules/01-execution.md#python-namespace-imports-and-paths) | `sys.path`, `__file__`, `bpy.path.abspath`; distinguish CWD, script directory and `.blend` directory |
| Create mesh; create object; link collection | [Mesh](modules/04-mesh.md), first [ownership](modules/02-data.md) | `Mesh.from_pydata`, `Mesh.validate`, `bpy.data.objects.new`, `Collection.objects.link`; check topology, users and scene membership |
| Edit topology; extrude faces; bevel edges | [BMesh](modules/04-mesh.md), [example functions](examples/README.md) | `bmesh.new`, `from_mesh`, `bmesh.ops`, `to_mesh`, `free`; distinguish owned BMesh from borrowed Edit Mode data |
| Set attributes, UVs, normals, shading or selection | [Mesh representation](modules/04-mesh.md) | Domain, type and element count must agree; shading normals do not certify geometry orientation |
| Share geometry; make independent copy | [Ownership](modules/02-data.md), [mesh examples](examples/mesh_patterns.py) | `Object.copy`, `ID.copy`, `.data`, `.users`; geometry independence does not imply material/node-group independence |
| Move object; parent object; preserve world transform | [Transforms](modules/05-transforms.md) | `matrix_world`, `matrix_parent_inverse`, local transform components; distinguish points from directions and normals |
| Revise dimensions; resize; apply scale | [Transforms](modules/05-transforms.md), then [revision](modules/09-revision.md) | Change intrinsic parameters or transforms deliberately; refresh cached geometry before reading bounds or setting `dimensions` |
| Create curve; bevel path; add extrusion | [Curves](modules/05-transforms.md) | `Curve`, `Spline`, point allocation, resolution and profile controls; inspect evaluated tessellation |
| Add modifier; change modifier order; apply modifier | [Modifiers](modules/05-transforms.md), [context](modules/03-context.md) | Explicit Array/Bevel/Boolean/Mirror/Solidify/Subsurf/Nodes settings; stack order and render/view levels affect output |
| Create Geometry Nodes; expose parameter; revise node input | [Nodes](modules/06-nodes.md), first [evaluation](modules/03-context.md) | `NodeTree.interface`, socket identifiers, `NodesModifier.properties.inputs`; verify the 5.2 typed schema |
| Instance objects; realize instances; join geometry | [Node palette](modules/06-nodes.md#bounded-geometry-nodes-palette) | Instance placements are not Main Objects; realized and joined geometry is not automatically welded |
| Inspect evaluated geometry; calculate bounds | [Evaluation](modules/03-context.md#obtain-current-evaluated-geometry) | Fresh graph → `Object.evaluated_get` → `to_mesh` → copy values → `to_mesh_clear`; account for instances and graph mode |
| Create material; create shader graph; use procedural noise | [Shader palette](modules/06-nodes.md#bounded-shader-palette), [inspection](modules/07-render.md) | Socket values/links and color spaces; material node-tree behavior changed in 5.2 |
| Configure camera, lights, world; render PNG | [Rendered inspection](modules/07-render.md), [inspection example](examples/inspection.py) | Cycles CPU, explicit framing/sampling/color settings and synchronous render; inspect fresh pixels as well as file transport |
| Save editable scene; reopen; recover resources | [Persistence](modules/08-persistence.md) | `save_as_mainfile`, `open_mainfile`, paths and external resources; reacquire IDs after load and verify a later round trip |
| Export OBJ; export evaluated static geometry | [OBJ contract](modules/08-persistence.md), [persistence example](examples/persistence.py) | Collection scope, evaluation mode, axes, scale, OBJ/MTL; warning-only completion can produce no geometry file |
| Rebuild from parameters; revise existing object; avoid duplicates | [Controlled revision](modules/09-revision.md) | Owned semantic keys, ambiguity rejection, staged replacement; preserve manual edits according to an explicit policy |
| Recover after failure; detect stale output; handle timeout | [Recovery](modules/09-revision.md), [host illustration](examples/host_job.py) | Preserve failed attempt and logs; fresh process/root; require output provenance and later semantic acceptance |
| Design a capability test | [Future tests](FUTURE_TESTS.md), [open questions](modules/10-recipes.md#evidence-and-open-questions) | T01 - T10 give expected observations and failure criteria; none was run |

For a question not answered here, follow the selected reference page through the [source index](SOURCE_INDEX.md). Adding an unreviewed API changes the evidence boundary; record that addition before calling it an established recipe.
