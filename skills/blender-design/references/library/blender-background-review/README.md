# Blender background scripting: technical working reference

Public distribution: findings and metadata are bundled. Full source captures are separately preserved; [archive access](../../../../../docs/archive.md). Research-stage exclusions below are historical scope, not a restriction on new user-authorized design work.

**Baseline:** Blender 5.2.2 LTS, commit `d13f752e3b9c4f8c261cda552b1021f8bcc0382c`, installed macOS ARM64 application, bundled Python 3.13.13. Research captures: 15 September 2026. [Identity and evidence](BASELINE.md).

**Purpose:** give a future coding agent enough implementation-backed guidance to construct, inspect, revise and save procedural objects using Python inside a background Blender process. This is a research reference. **Every modeling example and future test is unexecuted.** Syntax validation is not API validation or demonstrated modeling capability.

## Reading map

| Order | Module | Main dependency |
|---|---|---|
| 1 | [Execution and environment](modules/01-execution.md) | Process, paths, startup and failure status |
| 2 | [Data ownership and scene structure](modules/02-data.md) | IDs, shared data, linking and lifetime |
| 3 | [Context, operators and evaluation](modules/03-context.md) | Original versus evaluated state |
| 4 | [Mesh construction and BMesh](modules/04-mesh.md) | Topology, attributes and write-back |
| 5 | [Transforms, curves and modifiers](modules/05-transforms.md) | Coordinates and ordered geometry operations |
| 6 | [Python-created node graphs](modules/06-nodes.md) | Interfaces, fields, instances and 5.2 migration |
| 7 | [Materials and rendered inspection](modules/07-render.md) | Controlled Cycles CPU / PNG feedback |
| 8 | [Saving, reopening and export](modules/08-persistence.md) | Editable `.blend` versus static OBJ |
| 9 | [Controlled revision and recovery](modules/09-revision.md) | Identity, partial mutation and stale outputs |
| 10 | [Operational recipes and unresolved questions](modules/10-recipes.md) | Task sequences and later experiments |

Read 1 - 3 before modifying any scene. Read 4 - 6 as required by the object representation. Read 7 - 9 before accepting an output. Module 10 is a route into the reference, not a substitute for the contracts.

## Find an answer

- [Task index](TASK_INDEX.md): create mesh, revise dimensions, inspect evaluated geometry, recover after failure.
- [API index](API_INDEX.md): literal identifiers and complete captured reference units.
- [Failure index](FAILURE_INDEX.md): exceptions, diagnostic strings and misleading symptoms.
- [Glossary and command reference](GLOSSARY.md).
- [Consequential claims](CLAIMS.md): evidence classification, limitations and tests.
- [Firsthand reports](EXPERIENCE.md): historical versions, reproduction, contradictions and current relevance.
- [Source index and documentation coverage](SOURCE_INDEX.md), [implementation ranges](SOURCE_TRACES.md), [machine-readable reading coverage](coverage.json).
- [Examples](examples/README.md), [future test scenarios](FUTURE_TESTS.md), [artifact validation](VALIDATION.md).

## Boundary

Native `bpy` executes inside the installed Blender executable, in a fresh background process per job. Objects remain editable in `.blend`; PNG supplies conventional rendered feedback. Cycles CPU is the reference configuration. OBJ is the sole static export case. Geometry Nodes and shader graphs are construction techniques within this route.

The review does not install standalone `bpy`, introduce MCP/editor bridges/add-on infrastructure, generate diffusion assets, download finished models, run examples, generate scenes or change Blender configuration. Rigging, animation design, physics, dataset pipelines and manufacturing certification are excluded. Frame/evaluation behavior appears only where necessary to understand scene state. Render implementation inspection stops at configuration, execution, reporting and file output; it does not audit the integrator.

## Evidence rules

**D** = documentation; **S** = pinned implementation; **R** = reported experience; **I** = inference or recommended engineering policy. A source-derived mechanism is not a runtime observation on this machine. Published `/5.2/` documentation is a release-series snapshot, not an exact documentation commit. Receipts retain URL, retrieval time, byte count and SHA-256. Pinned source URLs contain the full commit. Failed captures and corrected paths remain recorded.

“Complete reading” means all content of the selected documentation unit, including notes, parameters and examples, not all linked pages. Shared inherited definitions are read once. The coverage manifest distinguishes complete units, selected operator entries, bounded source ranges, discovery-only material and inaccessible paths. Diagrams' captions and surrounding prose were read; remote image pixels and attached reproduction `.blend` files were not fetched or executed.

## Search locally

Unexecuted search examples, run from the directory containing this review:

```sh
rg -n --glob '*.md' 'create mesh|revise dimensions' blender-background-review
rg -n --glob '*.md' 'Object.evaluated_get|to_mesh_clear' blender-background-review
rg -n --glob '*.md' 'context is incorrect|stale output|ReferenceError' blender-background-review
```

`rg` is ripgrep, a filesystem text-search tool. `-n` prints line numbers; `--glob '*.md'` restricts results to Markdown; `|` within the quoted regular expression means “either pattern.” The final argument is the search directory. These commands do not invoke Blender. Identifiers can instead be searched literally with `rg -n -F 'bpy.data.objects' blender-background-review`; `-F` disables regular-expression interpretation.
