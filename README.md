# Blender Design

A Codex plugin for designing and revising editable Blender scenes through Python. Define useful parameters and construction rules, derive geometry, inspect renders, and check the intended relationships.

Version 1.2.0 is a local release candidate. No public repository or directory listing has been published.

## Requirements

- Codex with local plugin support, file access, command execution, and image inspection.
- An installed Blender executable. The release example is tested on Blender 5.2.2 LTS, macOS ARM64. Other versions/platforms require compatibility checks.
- Host Python 3.10+ for helpers and the example runner. No pip dependencies are required.
- Network access only for optional Poly Haven searches/downloads. No service account or API key is required by the helper.

The plugin supplies instructions, references, and helpers. Blender runs the modeling code. Installing it does not provide Blender or a remote rendering service.

## Install locally

Download and extract the release ZIP, or clone the eventual source repository. Keep the whole `blender-design` folder together, including hidden metadata. From its root:

```sh
python3 -B tools/release.py check
codex plugin marketplace add .
codex plugin add blender-design@blender-design-local
```

Start a new Codex chat after installation. Example request:

> Use $blender-design to create a parameter-driven folding divider. Derive hinge locations from panel edges, inspect the render, and deliver an editable scene, source, and preview.

Commands above are tested with the local Codex CLI. Plugin availability and installation interfaces vary by client. [Official packaging documentation](https://developers.openai.com/plugins/build/plugins).

## Run the example directly

From the extracted package root, choose an output directory that does not exist:

```sh
python3 -B examples/run_example.py --output build/divider-01
```

The runner discovers `blender` on PATH or the standard macOS application. Set `BLENDER_BIN` or pass `--blender "/path/to/blender"` for another installation. Try `--width 1.3 --angle 40` with a different output directory. [Construction and verification details](examples/README.md).

Outputs include `scene/divider.blend`, `scene/preview.png`, source hashes, logs, and an independent relocated-file inspection. The three panels share derived edge/hinge positions. Render appearance still requires visual inspection.

## Reference and assets

- [Skill](skills/blender-design/SKILL.md), [design philosophy](skills/blender-design/references/design-philosophy.md), and [working guide](skills/blender-design/references/working-guide.md).
- [Technical reference](skills/blender-design/references/library/blender-background-review/README.md): ten modules, API/task/failure indexes, 27 scoped claims, reading coverage, examples, contradictions, and open tests.
- [Historical lamp examples](skills/blender-design/references/demo-transfer.md) are preserved sources, separate from the runnable release example.
- [Poly Haven workflow](skills/blender-design/references/polyhaven.md): search, bounded acquisition, offline byte verification, and native collection import. Assets come from [Poly Haven](https://polyhaven.com); downloaded geometry is not original procedural authorship.
- [Research archive and offline access](docs/archive.md), [file-by-file preservation](docs/preservation.json), and [historical validation](docs/history.md).

No findings were discarded to make the default download small. Full captures and historical tooling remain in a separate private snapshot/archive pending per-source redistribution clearance. The default package contains findings, source links, hashes, and archive locations, not all captured source bytes.

## License and verification

Original contributions by Julian Turner are licensed as follows: code under GPL-3.0-or-later, original prose under CC BY-SA 4.0. Third-party material retains its original terms. See [LICENSE](LICENSE), [NOTICE](NOTICE.md), and the [licensing review](docs/licensing.md).

[Validation](VALIDATION.md) records what was actually tested. Research examples marked unexecuted remain unexecuted; one runnable example does not validate the entire reference or all Blender versions.

To contribute or build a release, see [release instructions](docs/releasing.md).
