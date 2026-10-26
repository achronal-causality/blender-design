# Artifact validation

**Result: PASS for the research artifact.** The [machine-readable receipt](validation.json) contains the final run time, interpreter identity, counts, search results, content digests and errors. This validates documents and source correspondence, not Blender's modeling capability. No modeling example, render, save/export operation or future capability test was executed.

## Objective checks

| Check | Result and limit |
|---|---|
| Baseline | Read-only identity recheck matched Blender 5.2.2 LTS, ARM64, `d13f752e3b9c`; full revision resolution retained from preparation and pinned repository tree. No application update/configuration change |
| Capture integrity | All **295 successful bodies** match recorded SHA-256 and byte counts; retrieval times and URLs present. **16 reused preparation bodies** also match their originals |
| Exact source correspondence | All **103 commit-pinned bodies** match their Git blob hashes in the captured complete repository tree. This includes source, narrative RST and shipped examples |
| Corpus accounting | All **298 unique planned capture IDs** have receipts and dispositions; three failed guessed paths have successful replacements. Selected documentation entries have recorded readings |
| Implementation evidence | **120 recorded intervals across 85 source files**, with valid line bounds. Every linked source interval is contained in the union of actually recorded inspected ranges |
| Navigation | Local files and Markdown heading targets resolve. Task/API/failure indexes are linked from the entry point. Exact link counts are in the JSON receipt |
| Example syntax | **Five example files and 22 Python blocks** parsed by bundled Python 3.13 using `ast.parse`. Nothing was imported from the examples or executed |
| Structure | All ten modules contain the required common sections and explicitly identify unexecuted examples; the ledger contains 27 consequential claims |
| Discoverability | Eleven real `rg` searches reach expected modules, including “create mesh,” “revise dimensions,” “inspect evaluated geometry,” “recover after failure,” `bpy.data.objects`, `bmesh.new`, `Object.evaluated_get`, `ReferenceError`, context failure and stale output |
| Research boundary | No `.blend`, PNG, OBJ or MTL output exists under the review directory. Ten later test scenarios remain specifications only |

The first check found three broken claim links, one source citation extending past its recorded reading extent, two absent literal search terms and a validation receipt not yet created. The links/terms were corrected, the cited source interval was read and recorded, and the check was rerun. These were artifact defects, not Blender runtime results.

## Reading coverage

| Corpus category | Coverage disposition |
|---|---|
| Twelve required pinned narrative guides | Complete selected units, including literal-include dependencies; no recursive reading claim |
| 107 API reference captures | Complete defining content for selected units; shared inherited definitions read once and cross-referenced |
| Three operator reference captures | Complete **selected entries** used by this review, not every operator on those large pages |
| 60 selected manual captures | Complete selected article content, including notes, examples and captions; external image pixels/videos not examined |
| 5.2 migration notes and compatibility dependency | Both selected pages read completely; conflicts with generated/pinned interfaces are recorded in the baseline and nodes module |
| Five official example captures | Complete code reading, including Object/Edit Mode ownership distinction and quickstart literal includes; never executed |
| Implementation files | Actual function/range inspection only. No complete dependency-graph, rendering-integrator or numeric modeling-kernel audit |
| Ten firsthand cases in 17 report captures | Full captured bodies/comments within stated scope; unknown versions/platforms and contradictory reproductions retained. One long native stack was only partially inspected |
| Three index/discovery captures | Repository tree/path discovery and optional release index material; not labeled complete documentation reading |

[Source index](SOURCE_INDEX.md), [coverage manifest](coverage.json), [reading batches](reading-log.json), [additional readings](additional-reading-log.json) and [source ranges](SOURCE_TRACES.md) own the detailed accounting. Counts identify the bounded corpus; they were not quotas used to select examples or reviews.

## Evidence and explanation audit

The final manual audit checked consequential recommendations against the captured documentation and the inspected source behaviors. The automated citation check confirms paths/range containment, not semantic truth. No agent's declaration or passing syntax check is substituted for Blender execution.

| Recommendation group | Evidence / explanation location | Remaining runtime question |
|---|---|---|
| Execution, imports, argument order, exit handling | C01 - C03; module 01; baseline diagnostic flag table | T01/T02 actual exception/exit paths |
| Ownership, removal, copies, stale wrappers | C04 - C06; module 02; ID and collection definitions | T03/T06 sharing and reopen behavior |
| Context, evaluation, temporary mesh cleanup | C07 - C09; module 03 | T04/T05 concrete context and geometry |
| Mesh/BMesh validation, attributes and write-back | C10 - C13; module 04 | T07 shape-specific topology/normal behavior |
| Coordinates, dimensions, curves and modifiers | C14 - C16; module 05 | T05/T07 scale, ordering and materialization |
| Node interfaces, typed input migration, instances | C17 - C19; module 06 | T05/T10 runtime schema refresh and old recipes |
| Material/camera/light/color/render configuration | C20 - C22; module 07 | T08 fresh image, framing and failure signals |
| Save/resource/export behavior | C23 - C25; module 08 | T06/T09 editability, resources and receiver losses |
| Revision and acceptance policy | C26 - C27 explicitly classified as inference; module 09 | T02/T03/T08 partial mutation and stale artifacts |

Every command introduced in the operational examples has a flag table or glossary route. The example map explains function arguments, returns, mutations and cleanup; standard-library interfaces are explained there separately. Literal Blender API identifiers route to modules and the full local selected references, where parameter defaults/ranges and inherited contracts are available. The bounded palettes have socket/field/instance explanations. No assertion is made that all APIs mentioned by a captured reference page are recommended by this review.

## Bounded gaps and contradictions

- Three inaccessible guessed source paths were replaced by verified paths. They are preserved in receipts and do not leave an unresolved required implementation entry point.
- `rna_node_socket.cc` was captured during dependency discovery but not read or used as evidence; the needed generated input behavior was resolved in the inspected `nodes/intern/node_socket.cc` and geometry-node execution code.
- Published manual/API pages are captured release-series HTML. Their content hashes do not establish an exact documentation-build commit. Dynamic enum placeholders, legacy Array documentation, deprecated `use_nodes`, mesh conversion errors and node-input migration mismatches are reconciled in [BASELINE](BASELINE.md#resolved-documentation-mismatches).
- Issue-tracker browser access was blocked; public API captures supplied selected report bodies/comments. Reproduction attachments, images and uncollected answer comments remain unexamined. Historical closed status is not treated as a verified fix.
- No runtime RNA acceptance, geometric robustness, render quality/performance, `.blend` round trip, external-resource resolution or OBJ receiver fidelity has been demonstrated. [Future tests](FUTURE_TESTS.md) attach concrete expected observations and failure criteria to these limits.

## Rerun artifact validation

From the directory containing this review, the following **artifact-check command was executed**:

```sh
/Applications/Blender.app/Contents/Resources/5.2/python/bin/python3.13 \
  -I -B blender-background-review/validate_reference.py
```

This launches the bundled Python interpreter, not Blender. `-I` isolates Python startup; `-B` prevents bytecode-cache writes. The final argument is the task-local checker, which reads captures/documents, parses example syntax, invokes `rg` for text searches and writes `validation.json`. It performs no network request, example import or modeling operation. Exit code zero means its artifact checks passed; it does not certify the future examples' runtime behavior.
