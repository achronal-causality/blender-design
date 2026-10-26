# Release validation

## 1.2.1 asset-guidance revision

Primary-source documentation reviewed 2026-10-26 for all six providers. New shared asset guidance/source directory are documentation, not new download/import tests. Poly Haven scripts, policy records, helper tests, all 24 audited research documents, and the procedural example remain byte-identical to `67ce88a`. The selected-provider policy is explicitly replaced by ADR 0002; its history is preserved.

The final 1.2.1 package is checked by exact members/hashes, local links, extracted unit tests, isolated Codex installation, installed-cache integrity, and original/finding preservation. The existing example's source hashes must match the previously rendered and reopened builds. No new render is necessary for unchanged example code. Machine-readable results/logs are retained under `build/asset-guidance-verification/`, outside the public payload. No new live provider API, acquisition, add-on, or asset import test is claimed.

## 1.2.0 runtime and publication-cleanup baseline

Validated locally on 2026-10-26. These prior runtime checks remain applicable only to the unchanged code and recorded environment; this is a local release candidate, not a published listing.

## Preservation and packaging

- Every one of the original package's 1,288 files is preserved by SHA-256 in the private snapshot and checked again inside the companion ZIP. Original package bytes: 95,635,369. The private ZIP is 10,794,854 bytes; SHA-256 `b67853d37167a21686fb0a46ce10803148a11f995034c67a507cb215498b7a08`. It is not cleared for public redistribution.
- Full normalized text comparison passed for 24 retained non-README research documents, including all ten modules, all 27 claims, failures, contradictory reports, open tests, baseline, preparatory reports, and source/reading indexes. Allowed differences are link targets, personal-path substitutions, and dash normalization. Every original README and script also remains recoverable from the snapshot. Public file transformations have their own hashes.
- The public ZIP uses an explicit file list. Exact inventory, hashes, Markdown local targets/anchors, and personal-path patterns pass validation. Full third-party source captures, historical installers, retrieval logs, and Python caches are outside the default payload.
- All 15 standard-library tests passed: seven helper tests and eight release-boundary tests. Helper coverage includes that acquisition receipts explicitly label the replacement policy records as summaries, not captured terms. Release tests reject missing/modified files, unexpected root files/caches, unsafe paths, broken links/anchors, and personal paths. Python source syntax checks passed.

## Installation

The release ZIP was extracted into a fresh path containing spaces. The README marketplace-add and plugin-add commands succeeded using Codex CLI 0.164.0 with a separate child-process Codex home. Plugin listing showed version 1.2.0 installed and enabled. The installed cache passed the complete release checker. No personal Codex config or existing installed 1.1.0 cache was changed. A clean OS, another user's account, and the graphical plugin browser were not tested.

## Blender example

Blender 5.2.2 LTS, build `d13f752e3b9c`, macOS ARM64, Cycles CPU, 24 samples, 640 x 480 PNG. Two fresh builds used width/angle pairs `(1.0, 28 degrees)` and `(1.3, 40 degrees)`.

Both rendered successfully, then their saved scenes were copied to another directory and reopened in independent processes. The inspector measured zero gap at the two panel edge attachments in both cases, checked dimensions/fold angles/topology/bevels/camera, and found no image or linked-library dependencies. It does not repair meshes. Preview headers/dimensions passed. Both PNGs were visually inspected: all three colored panels and two hinge axes were visible, framing was complete, and the parameter variation was visible.

[Default artifact hashes](docs/verification/default-artifacts.json), [default reopen](docs/verification/default-reopen.json), [wide artifact hashes](docs/verification/wide-artifacts.json), [wide reopen](docs/verification/wide-reopen.json).

The first build under the restricted execution sandbox terminated with a native segmentation fault at startup (process 25977), before any Python exception. An explicit-path retry outside that sandbox succeeded, as did the parameter variation. The user-provided macOS report matched the failed process. These observations suggest an execution-environment contribution; the native root cause was not established. Raw failed/successful logs and the crash report are retained privately. No application update or config change was made.

## Limits

No Windows/Linux or alternate-Blender compatibility claim, broad catalog import validation, continuous collision analysis, physical mechanism certification, animation test, or entire-research-example execution follows. Historical research examples marked unexecuted retain that status. Fresh source access was not OS-blocked during the divider reopen. No live Poly Haven request was needed for this cleanup; helper network behavior remains represented by bounded unit tests and separately labeled historical integration evidence.

Licenses for original contributions were explicitly authorized by the user. Whole captured third-party content remains outside the public artifact pending per-source clearance. The public report does not grant those third-party rights.
