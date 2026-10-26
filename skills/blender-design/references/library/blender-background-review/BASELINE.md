# Technical baseline and reconciliation

## Observed identity

The read-only recheck at **2026-09-15T18:21:19 UTC** matched the approved baseline. No Blender update was performed during this review. [Raw diagnostic receipt](baseline-recheck.json).

| Field | Observation | Meaning and limit |
|---|---|---|
| Executable | `/Applications/Blender.app/Contents/MacOS/Blender` | Absolute executable inside the macOS application bundle |
| Version | `Blender 5.2.2 LTS` | Application's own release label |
| Source hash reported by executable | `d13f752e3b9c` | Short hash; matched to the full approved commit and captured repository tree |
| Full source revision | `d13f752e3b9c4f8c261cda552b1021f8bcc0382c` | [Pinned source](https://github.com/blender/blender/tree/d13f752e3b9c4f8c261cda552b1021f8bcc0382c) |
| Branch | `blender-v5.2-release` | Build metadata, not a promise that a moving branch stays at this commit |
| Build time | 2026-09-15 01:49:19 | Time printed by application; timezone not supplied |
| Commit time | 2026-09-14 15:14 | Time printed by application; full repository evidence lives in preparation |
| Platform/type | Darwin / Release | macOS release build |
| Architecture | Mach-O 64-bit `arm64` | Native ARM64 executable, verified independently of version label |
| Bundled Python | `3.13.13`, Clang 21.0.0 | Reported by the bundled interpreter; this diagnostic does not import `bpy` |

The Python banner includes `main, Apr 25 2025, 12:39:20`; preserve it as reported metadata rather than inferring a Blender release date from it. The application's version diagnostic emitted an OpenUSD `ArchWarn: ARCH_CACHE_LINE_SIZE != Arch_ObtainCacheLineSize()` message, returned zero and printed the identity. It is retained, not explained away. This diagnostic is neither a render failure nor evidence that rendering works.

## Diagnostic commands and fields

These commands **were used only to inspect identity**:

```sh
/Applications/Blender.app/Contents/MacOS/Blender --version
/usr/bin/file /Applications/Blender.app/Contents/MacOS/Blender
/Applications/Blender.app/Contents/Resources/5.2/python/bin/python3.13 -I -B -c 'import sys; print(sys.version)'
```

`--version` prints release/build metadata and exits without running a modeling script. `file` inspects executable format and architecture. The Python command uses the bundled executable; `-I` selects isolated Python startup, `-B` prevents bytecode-cache writes, and `-c` executes the quoted standard-library-only diagnostic. `sys.version` is the interpreter's version/build banner. Return code, stdout and stderr were captured separately. Build C/C++/link flags describe compilation, not live user settings or enabled render devices.

## Matching documentation and provenance

- [Blender 5.2 manual](https://docs.blender.org/manual/en/5.2/) and [Python API](https://docs.blender.org/api/5.2/) are release-series pages. This review stores the actual retrieved bodies and hashes, not an invented documentation-build revision.
- [5.2 Python API migration notes](https://developer.blender.org/docs/release_notes/5.2/python_api/) were read in full. Feature-specific manual pages were cross-checked with pinned implementations.
- [Prior Preparation A](../blender-preparatory-research/PREPARATION_A_TECHNICAL_BASELINE.md), [Preparation B](../blender-preparatory-research/PREPARATION_B_ROUTE_SELECTION.md), and [preparation coverage](../blender-preparatory-research/SOURCE_COVERAGE.md) retain original installation/provenance evidence. Their conclusions predate this focused reading; they do not override a discrepancy resolved here.
- [Capture receipts and dispositions](SOURCE_INDEX.md) identify reused preparation bodies and new retrievals. Source is pinned; the manual and API are captured snapshots. “Latest” and development-branch behavior are outside this baseline.

## Resolved documentation mismatches

1. The main Array manual page describes a newer Geometry Nodes based workflow. The explicitly added **Array legacy** page describes the classic `ArrayModifier` used here. Do not transplant node-asset controls into `obj.modifiers.new(..., 'ARRAY')`.
2. Generated API pages sometimes show dynamic enums as placeholder values. The displayed `NodeTreeInterface.new_socket` enum and render engine enum are not exhaustive runtime type catalogues. Pinned registration and declarations establish the intended strings; later tests still check their runtime acceptance.
3. `use_nodes` survives in several references as deprecated compatibility surface. It is not a reliable feature switch in 5.2. Construct and inspect the actual node tree.
4. An evaluated-mesh documentation example describes unsupported objects returning `None`; the pinned RNA entry reports an error for unsupported object types. Restrict conversion to supported geometry types and handle failure. [Evaluation module](modules/03-context.md).
5. The migration notes and generated node-input implementation support `.properties.inputs.<identifier>.value`; older material in the compatibility discussion uses a different intermediate shape. The final pinned structure owns this review's recommendation.
6. Source exposes `--python-use-user-env`; the selected manual capture did not document it. It is recorded as a source-derived option, not silently promoted into the recommended command.

## Remaining provenance limits

Build metadata and official revision resolution establish identity as far as available evidence permits; this review does not reproduce the build or establish bit-for-bit compiler reproducibility. API/manual hashes identify retrieved bytes, not the source revision used to build their HTML. No automatic upgrade or installation occurs if a future agent sees drift: record the new identity, compare compatibility, and obtain a revised research baseline.
