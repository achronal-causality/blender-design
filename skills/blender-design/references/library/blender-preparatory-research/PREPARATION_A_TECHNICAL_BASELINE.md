# Preparation A: Blender technical baseline

**Investigation date:** 15 September 2026.  
**Disposition:** Complete, with the provenance limits below.  
**Current baseline:** Blender **5.2.2 LTS**, native Apple Silicon, official release commit `d13f752e3b9c4f8c261cda552b1021f8bcc0382c`.

## 1. Result and authority

The initial application was Blender 5.2.0 LTS. During this investigation, you explicitly requested installation of the latest version if needed. The official download page and release directory identified **5.2.2 LTS**, published on 15 September 2026, as the current stable download. The application was updated to that release. This supersedes the earlier plan's no-installation boundary for Blender itself; it does not authorize installing an integration or running a capability test. [Official download](https://www.blender.org/download/), [release directory](https://download.blender.org/release/Blender5.2/).

The new installation passed:

- SHA-256 comparison of the downloaded disk image against the vendor's checksum file.
- Code-signature verification before and after application replacement.
- macOS execution-policy assessment, which accepted the application as a notarized Developer ID application.
- Execution of the installed binary's version-reporting option.
- Comparison of the existing Blender 5.2 configuration files before and after replacement.

The old application remains at [the temporary rollback location](../../../../../docs/history.md). This is temporary storage, not a permanent archival backup. The installer volume was ejected. No model-building script, render, simulation, benchmark, or integration server was executed.

## 2. Exact identity

| Field | Before update | Current installation |
|---|---|---|
| Application | `/Applications/Blender.app` | Same |
| Reported version | 5.2.0 LTS | **5.2.2 LTS** |
| Bundle version | 5.2.0 | 5.2.2 |
| Source branch | `blender-v5.2-release` | `blender-v5.2-release` |
| Full source commit | `fbe6228777e7d9afefcd61a413844e790ae75db7` | `d13f752e3b9c4f8c261cda552b1021f8bcc0382c` |
| Official tag | `v5.2.0` | `v5.2.2` |
| Source commit time, UTC | 2026-07-13 15:20:11 | 2026-09-14 15:14:06 |
| Binary build date/time, as reported | 2026-07-14 01:31:22 | 2026-09-15 01:49:19 |
| Build platform/type | Darwin / Release | Darwin / Release |
| Executable format | Mach-O 64-bit ARM64 | Mach-O 64-bit ARM64 |
| Bundled Python | 3.13.13 | 3.13.13 |
| Bundle identifier | `org.blenderfoundation.blender` | Same |
| Bundle minimum macOS version | 11.2 | 11.2 |

The application does not label the build timestamp's timezone. It is therefore preserved as reported, without assigning UTC. The commit API supplies a timezone; that timestamp was normalized to UTC.

The host reports macOS 26.6, build 25G72, and ARM64 architecture. This establishes the environment inspected, not measured renderer/device performance.

**Primary identity evidence:** [original commit](https://projects.blender.org/blender/blender/commit/fbe6228777e7d9afefcd61a413844e790ae75db7), [current commit](https://projects.blender.org/blender/blender/commit/d13f752e3b9c4f8c261cda552b1021f8bcc0382c), [official current tag metadata](https://projects.blender.org/api/v1/repos/blender/blender/tags/v5.2.2), [installation receipt](../../../../../docs/research-catalog.md#file-e7e8a4d8e67100a6), [post-installation diagnostics](../../../../../docs/research-catalog.md#file-050e151e933924fc).

### Release identity is independently corroborated

The executable reports the short hash `d13f752e3b9c`. The official repository resolves it to the full commit above. The `v5.2.2` tag points to that same commit, whose message identifies the release-version update.

At that commit, the version header declares major/minor value 502, patch 2, release cycle `release`, and suffix `LTS`. Thus “5.2.2 LTS” is corroborated across installed metadata, executable output, tag mapping, and source constants. It is not inferred merely from the application's filename. [Pinned version header](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/blenkernel/BKE_blender_version.h).

Three relevant files shipped in the installed application were also compared byte-for-byte with this pinned source: the background-job template, the BMesh template, and the Python operator-dispatch module. All matched. This supports the source mapping for those files, not a claim that the complete binary was independently rebuilt. [Comparison receipt](../../../../../docs/research-catalog.md#file-9b02268e0c32c493).

### Checksums and their meaning

| Artifact | SHA-256 |
|---|---|
| Official 5.2.2 ARM64 disk image, downloaded and verified | `dc4125399b8bfefe283cc1624d6cfc7809d1cac20ace51072127eb371f31f210` |
| Current installed Blender executable | `f5c1f2a0c0bca3389ec772d355242b700975ea84e66cbb3f5257a7bce8e5adeb` |
| Previous installed Blender executable | `60ba7a9b6743f7acf101274361fa76409e382ae07cd2007ce07dea30f6b129f2` |

The downloaded image contains 346,286,611 bytes. Its hash was compared with the entry for `blender-5.2.2-macos-arm64.dmg` in the [official checksum file](https://download.blender.org/release/Blender5.2/blender-5.2.2.sha256). The executable hashes are local fingerprints of a different artifact; they must not be compared directly with the disk-image hash. [Checksum receipt](../../../../../docs/research-catalog.md#file-83c20cd629b12e6b).

## 3. Which documentation matches?

| Source | Appropriate use | Precision and limitation |
|---|---|---|
| [Blender 5.2 Python API](https://docs.blender.org/api/5.2/) | Reference for the installed release series | Published as “5.2”; the inspected index does not expose the exact generating commit |
| [Blender 5.2 manual: scripting](https://docs.blender.org/manual/en/5.2/advanced/scripting/index.html) | Workflow and UI guidance | Versioned by series, but the inspected page's edit/source links point to manual `main`; it is not proof of a frozen source revision |
| [Blender 5.2 command-line manual](https://docs.blender.org/manual/en/5.2/advanced/command_line/arguments.html) | Argument semantics and ordering | Corroborate operational flags with the installed executable's `--help` |
| [5.2 release notes](https://developer.blender.org/docs/release_notes/5.2/) | Features, compatibility changes, and release-series context | A living explanatory document, not an immutable description of every patch |
| [5.2 Python API release notes](https://developer.blender.org/docs/release_notes/5.2/python_api/) | Migration hazards relevant to generated code | Changes are linked to individual commits; use those links for disputed details |
| Source files at the full 5.2.2 commit | Exact implementation and narrative-source baseline | Immutable reference for the inspected code; dependent code still needs tracing when a claim requires it |
| API `current` / source `main` | Discovery only | Moving targets; not authoritative for an installed-version claim without checking compatibility |

The release notes date Blender 5.2 LTS to 14 July 2026 and describe maintenance through July 2028. The latest *patch* release checked during this task is 5.2.2. A release series and its latest patch are distinct facts. [Release-series notes](https://developer.blender.org/docs/release_notes/5.2/).

The research archive retains downloaded source bytes, retrieval timestamps, URLs, and hashes. This fixes what was actually read even when the upstream document later changes. A content hash does not reveal an unpublished documentation-build commit.

### Compatibility details that already affect route selection

The 5.2 Python release notes identify a change from custom-property access to RNA property access for Geometry Nodes modifier inputs and output attribute names. They also identify changed socket identifiers and newly available background GPU initialization. These are relevant to code copied from older tutorials, wrappers that assume older field names, and overly broad assertions that background mode cannot access GPU functionality. They do **not** establish working GPU rendering through each wrapper on this Mac. [Python compatibility changes](https://developer.blender.org/docs/release_notes/5.2/python_api/).

The updated installation still uses the `5.2` resource/configuration directory. The pre/post installation configuration comparison found the same `platform_support.txt` hash; no other files existed in that inspected config directory. Project files were not opened or rewritten during replacement. The check is precisely a comparison of that directory, not a claim to have hashed every user file.

## 4. Python environments: an important distinction

The bundled interpreter's diagnostic output is:

```text
3.13.13 (main, Apr 25 2025, 12:39:20) [Clang 21.0.0 (clang-2100.0.123.102)]
```

This is the interpreter's own build string, retained literally. Its embedded compiler timestamp was not independently reconstructed. The Blender application build date is separately reported above.

The bundled Python executable and Blender's embedded interpreter are related but different entry points. Running the Python executable directly was used only to inspect Python identity. It does not establish that ordinary external Python execution gains the running application's `bpy` state.

The official standalone package **`bpy==5.2.2`** exists for CPython 3.13 and macOS ARM64. Its wheel is named `bpy-5.2.2-cp313-cp313-macosx_11_0_arm64.whl`: `cp313` identifies the CPython 3.13 interpreter/ABI, and the platform suffix identifies macOS ARM64 packaging. Registry metadata requires Python `==3.13.*`. The wheel was **not installed or imported**. Its existence establishes an available candidate, not equivalence to the application build or working renderer parity. [Version-specific registry metadata](https://pypi.org/pypi/bpy/5.2.2/json), [Blender's module documentation](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/doc/python_api/rst/info_advanced_blender_as_bpy.rst).

## 5. Diagnostics and installation commands explained

These explain commands actually used; they are not instructions to repeat the update.

| Command or mechanism | Meaning and evidentiary limit |
|---|---|
| `Blender --version` | Runs the named executable to print Blender version, build flags, branch and commit information, then exits. Does not evaluate a scene |
| `Blender --help` | Prints the installed build's command-line options. Confirms available flags, not their behavior in a modeling workload |
| `plutil -p …/Info.plist` | macOS property-list inspection; `-p` prints the application's metadata in a readable representation |
| `PlistBuddy -c 'Print :CFBundleShortVersionString' …/Info.plist` | Reads a specific property-list key; `-c` supplies the read command. This was the initial version check |
| `file …/MacOS/Blender` | Inspects executable-format information, distinguishing ARM64 from Intel or a universal binary |
| `uname -m`; `sw_vers` | Report host architecture and macOS product/build versions respectively |
| `python3.13 -I -B -c '…'` | Runs a small identity query: `-I` isolates Python from user-site/environment influence, `-B` suppresses bytecode-cache writes, `-c` supplies Python statements. `sys.version`, `sys.executable`, and `platform.machine()` report interpreter identity, executable path, and architecture |
| `codesign -dv --verbose=4 …/Blender.app` | Displays signing metadata. Displaying a signature is not verification |
| `codesign --verify --deep --strict --verbose=2 …/Blender.app` | Verifies the bundle, including nested signed code, with additional strict checks and diagnostic output |
| `spctl --assess --type execute --verbose=2 …/Blender.app` | Asks macOS whether its execution policy accepts this application; reports notarized Developer ID acceptance here |
| `pgrep -fl …/MacOS/Blender` | Checks running processes; `-f` matches the full command and `-l` includes names. Replacement was gated on Blender having exited |
| `curl --fail --location --silent --show-error --max-time … --output … URL` | Downloads from an HTTPS URL: reject HTTP errors, follow redirects, suppress progress but preserve errors, bound duration, and write the response to the specified file. Certificate checks remained enabled |
| SHA-256 comparison | Reads both files' bytes through a cryptographic hash and compares the downloaded image with the vendor's published value. It does not execute the image |
| `hdiutil attach -readonly -nobrowse -mountpoint … image.dmg` | Mounts the verified disk image read-only, without opening a Finder window, at an explicit temporary location |
| `ditto source.app staged.app` | Copies the application bundle using the macOS bundle-aware copying utility |
| Rename of staged/previous applications | Preserves the old application, then places the verified staged bundle at the existing application path; no merge with old bundle contents |
| `hdiutil detach mountpoint` | Ejects the mounted installer volume after installation |

The raw command arrays, return codes, stdout, and stderr for the replacement are in the [installation receipt](../../../../../docs/research-catalog.md#file-e7e8a4d8e67100a6). The research used local text searches and a task-local GET-only source downloader; downloaded code was read as text and never imported.

## 6. Access problems and remaining uncertainty

1. **Sandbox-dependent signing result.** The original bundle initially failed signature verification inside the restricted execution environment. The same read-only verification succeeded outside it. The new bundle also passed verification and execution-policy assessment outside the sandbox. The initial result is not treated as evidence that the application was tampered with.
2. **Documentation retrieval.** The web reader returned access errors for Blender pages. Direct certificate-validated HTTPS retrieval succeeded. Blender's bundled Python initially lacked a usable trust configuration for these downloads; macOS `curl` succeeded without disabling verification.
3. **Source endpoint.** Blender's primary raw-file endpoint returned 403. The same commit-addressed files were retrieved from Blender's official GitHub mirror. Historical failed attempts remain recorded.
4. **Corrective-release page.** A candidate developer-documentation URL returned 404; a candidate LTS URL redirected to the general 5.2 release page. Neither is counted as a patch-by-patch corrective changelog. The stable download, official tag, commit and installed binary still establish 5.2.2 identity.
5. **Binary reproducibility.** This task verified vendor distribution integrity and identity, not a from-source reproducible build or a complete source-to-binary equivalence proof.
6. **Operational capability.** Renderer performance, graphics initialization, Python scene execution, standalone-package parity and third-party integration compatibility remain untested by design.

**Completion:** The exact installed research baseline is established and the requested update is complete. The remaining uncertainty concerns document-build provenance and untested runtime capabilities, not which release is installed.

