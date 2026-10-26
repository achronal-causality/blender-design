# Folding divider example

A new executable example, separate from the preserved historical lamp and unexecuted research examples.

```sh
python3 -B examples/run_example.py --output build/divider-01
python3 -B examples/run_example.py --output build/divider-wide-01 --width 1.3 --angle 40
```

Run from the package root. Host Python must be 3.10+. Discovery order: explicit `--blender`, `BLENDER_BIN`, `blender` on PATH, then the standard macOS application path. The runner never installs or updates Blender and refuses to reuse an output directory. Each Blender process has a configurable timeout (default 180 seconds). Logs and partial output remain on failure.

## Construction

Three identical-width panels alternate fold angle. For each panel, its left edge is the preceding panel's right edge. Its center is half a panel width along its rotated local x axis. Hinge axes lie at the resulting shared edges. Height and thickness remain fixed. Bevel modifiers soften the visible edges. This is a geometric illustration, not a mechanically certified hinge design.

Parameters: width 0.4 to 2.0 Blender units; angle 5 to 60 degrees. The model uses no external geometry, textures, fonts, audio, or packages.

## Outputs and acceptance

`scene/` contains the editable `.blend`, PNG, and builder result. `relocated/` contains a copied scene reopened in a separate Blender process. `reopen.json` is produced by the independent inspector. `validation.json` records source/output hashes, parameters, and bounded checks. Logs remain beside them.

The inspector checks original panel topology, dimension parameters, actual scale, fold angles, edge/hinge coincidence, finite coordinates, bevels, camera/resolution, and absence of linked libraries or images. It does not call mesh repair. The host checks PNG signature/dimensions. A human or image-capable agent must inspect the rendered PNG. The file is relocated, but source access is not OS-blocked in this example; the absence of external resource datablocks is checked directly.

Tested runtime and visual findings are recorded in [validation](../VALIDATION.md). No animation, continuous collision, physical assembly, Windows, Linux, or alternate-Blender compatibility is established.
