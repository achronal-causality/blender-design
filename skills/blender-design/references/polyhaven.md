# Poly Haven assets

Poly Haven is the selected catalog for this skill. Use its assets when external assets fit the user's brief; a request to create everything from scratch still excludes them. Choose scale, attachments, material response and style deliberately. A downloaded model is not evidence that the agent constructed that model procedurally.

## Service and license

Assets are supplied by **[Poly Haven](https://polyhaven.com)** under [CC0](https://polyhaven.com/license). The live [API](https://polyhaven.com/our-api) has separate terms: identify requests and visibly credit Poly Haven when surfacing live content. The helper prints that credit and includes it in provenance. Preserve a visible source credit in user-facing asset results as well. No API key, account or Blender add-on is needed for the documented default endpoints.

The bundled [policy records](../../../docs/research-catalog.md#file-434400ed04031397) identify original source-linked summaries reviewed 2026-10-26, not copies of the provider's terms. Acquisition receipts label these summaries explicitly and hash their bytes. The original 2026-09-15 captures and pinned terms are preserved in the private research archive, with their original hashes and retrieval records. Recheck primary terms when behavior or use changes. CC0 does not certify topology, scale, provenance, or suitability for a scene.

## Search and inspect

Commands below run from this skill's directory; replace paths and asset identifiers for the actual task. `python3` is host Python 3, `-B` suppresses bytecode caches, and `scripts/polyhaven.py` is the provider-specific standard-library helper. It does not import Blender or modify any scene.

```sh
python3 -B scripts/polyhaven.py search 'desk lamp' --type models --limit 8
python3 -B scripts/polyhaven.py inspect dirty_football
```

- `search QUERY` calls `/search`, trims/lowercases the query, and preserves returned ranking. `--type` accepts `models`, `textures`, `hdris`, or `all`; it defaults to models. `--limit` caps results, default 8, permitted 1 - 100. Query length is limited to 100 characters. Search uses the provider's metadata retrieval, not diffusion generation.
- `inspect ASSET` calls `/info/{id}` and `/files/{id}`. The slug is the catalog identifier, not a display name. Output includes author/metadata and exact available variant names, dependency counts and total declared bytes. Do not assume every asset has a `.blend` or every resolution.
- The service's similarity score is not a quality/suitability proof. Inspect available previews and evaluate the actual asset when needed. This helper does not download thumbnails or automatically choose a model from a ranking.

JSON goes to standard output; credit/errors go to standard error. A shell `>` redirects standard output to a file; use a fresh filename when retaining results. HTTP errors return exit code 1. For 429, the helper reports `Retry-After`; it does not automatically retry. Wait as directed before any deliberate retry. For 503, retain the failure and use the catalog's official browsing route or a bounded keyword lookup; do not loop indefinitely.

## Acquire one variant

```sh
python3 -B scripts/polyhaven.py download dirty_football \
  --variant blend/1k/blend \
  --output /absolute/task/assets/dirty-football-01 \
  --max-mib 8
python3 -B scripts/polyhaven.py verify /absolute/task/assets/dirty-football-01
```

`download ASSET` requires `--variant`, the exact key reported by inspect; `--output` must not already exist. `--max-mib` limits total declared payload bytes, using 1 MiB = 1,048,576 bytes; default 128. Choose a task-appropriate bound rather than downloading the largest resolution. Metadata reads are independently capped at 16 MiB and socket operations at 30 seconds. These are bounded requests, not a whole-job wall-time deadline; a supervising process may impose its own timeout.

The helper downloads the selected file and its declared `include` dependencies, preserving relative paths. Each file must match the provider's size and MD5; a local SHA-256 is also recorded. It rejects unsafe paths, conflicting dependencies, unexpected hosts and oversized files. It follows HTTPS redirects only within Poly Haven domains. It does not unpack ZIPs, install packages, run assets, or perform catalog-wide synchronization.

Output includes `info.json`, `files.json`, the payload, license evidence, and `provenance.json`. The receipt records author, canonical page, selected variant, dated evidence, hashes and completion status. A failed attempt retains `.part` files and an incomplete receipt; use a new output directory for retry. `verify DIRECTORY` is offline and rechecks stored payload/evidence hashes. It establishes byte identity, not geometric quality or cryptographic proof of authorship.

No asset payload is embedded in the plugin itself. Acquisitions belong in the current task/project. Retain their provenance when editing them.

## Bring a native collection into Blender

Use Blender's background process with `--disable-autoexec`, as explained in [the working guide](working-guide.md). Automatic execution stays disabled while loading downloaded files. This is not a complete native-code sandbox. The import helper verifies the local acquisition before appending.

```python
# TEMPLATE: this helper's collection/packing path was tested on one asset.
# Adapt these two absolute paths and the collection name for the current task.
import sys
sys.path.insert(0, '/absolute/plugin/skills/blender-design/scripts')
import polyhaven_blender

asset_dir = '/absolute/task/assets/dirty-football-01'
print(polyhaven_blender.list_datablocks(asset_dir))
asset_collection = polyhaven_blender.append_collection(
    asset_dir, 'dirty_football_LOD0', pack_images=True)
```

`sys.path.insert` makes the trusted helper directory importable; do not add downloaded code directories. `list_datablocks` verifies the acquisition and returns available collection/object/material names without appending them. Inspect this list first. Import a specific collection instead of all objects indiscriminately; otherwise multiple levels of detail can overlap.

`append_collection(directory, name, pack_images=True)` uses `bpy.data.libraries.load(..., link=False)` to copy the named collection and its dependencies into the current file, links it under the current scene, and returns a `bpy.types.Collection`. It adds source/license/variant custom properties and a provenance Text datablock. It does not save, render, reposition, or rescale the asset.

With `pack_images=True`, newly loaded file images must resolve to declared, verified files inside the acquisition. They are packed into the `.blend`; pre-existing scene images are untouched. Set `pack_images=False` only when deliberately retaining external image dependencies and managing their paths yourself. Appending again creates new data; reuse the returned collection or make collection instances when duplication is intended. Errors can follow partial scene mutation, so preserve the failed process's evidence and retry in a new output.

Packing images is not a blanket guarantee that every possible asset dependency is internal. Inspect imported modifiers, node groups, drivers, caches, linked IDs and external resources. A library record may remain after append without any linked datablock: in the tested asset it represented source provenance. Determine dependency status from actual linked IDs and a reopen test, not merely `len(bpy.data.libraries)`.

Other acquired formats use the corresponding native Blender APIs. HDRIs require deliberate World setup; material maps require correct channels and color-space interpretation. See [render/material guidance](library/blender-background-review/modules/07-render.md). Those mappings are task-specific; this version does not offer a universal auto-material or HDRI importer.

## Acceptance and tested scope

For the current design, measure actual evaluated bounds/orientation, inspect image paths and materials, check intended attachments, and render controlled views. Provider dimensions alone are not a Blender unit contract. Reopen important outputs after relocation and check dependencies without relying on the original acquisition directory.

The implementation exercise used `dirty_football`, variant `blend/1k/blend`, collection `dirty_football_LOD0`: four files, 3,530,774 payload bytes. Live search/metadata/download and helper failure handling were tested. The saved-file inspection results are summarized in the plugin's [validation record](../../../VALIDATION.md). This finite case does not establish every asset's Blender-version compatibility or universal import behavior.
