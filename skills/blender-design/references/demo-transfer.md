# Transfer from the lamp demonstrations

These are historical examples, not universal templates or a complete animation manual. Source snapshot: `lamp-demo-2026-09-15`, commit `1da4d193eeef51d3739b923d56c5ff3123ae18ba`. Selected unchanged source and receipts are bundled; scenes, movies, images and raw frames remain in the parked project and are not plugin dependencies.

## Articulated object

[Lamp builder](library/adjustable-desk-lamp/build_lamp.py) shows native construction, shared attachment frames and parameter-driven articulation. [Independent inspector](library/adjustable-desk-lamp/coordinator-review/inspect_saved_scene.py), [acceptance record](library/adjustable-desk-lamp/coordinator-review/acceptance.json) and [saved-file checks](library/adjustable-desk-lamp/final-reopen/reopen-checks.json) describe finite checks.

Useful transfer: express links/joints through local frames, derive coordinates, verify selected poses. These checks do not certify a physical mechanism or collision freedom at every pose. Do not copy dimensions or topology into another subject without a reason.

## Cartoon motion

[Motion source](library/lamp-intro-springy/source/motion.py), [scene builder](library/lamp-intro-springy/source/build_intro.py) and [lamp geometry](library/lamp-intro-springy/source/lamp_geometry.py) illustrate anticipation, rebound, squash/stretch and delayed response. Read relevant functions; do not run historical commands into old destinations.

The intended invariant changed: an undeformed character linkage remains coherent while deliberate deformation changes world-space shape. [Geometry receipt](library/lamp-intro-springy/runs/production-01/geometry-checks.json) and [movie validation](library/lamp-intro-springy/validation.json) record sampled structural/media checks for the historical 384-frame, 16-second demo, not every subframe or parameter choice.

The user liked the springy revision. That qualitative feedback is separate from automated checks. The exact cold-agent context was not preserved sufficiently to call this a controlled independent benchmark.

## Dependencies and limits

Static presentation used Cycles CPU; animation used EEVEE. Sound synthesis used bundled NumPy; movie assembly used an existing FFmpeg. These are demo dependencies, not prerequisites for loading the skill or making a basic model. Demo sources contain build guards and old paths. Adapt into the current task with live runtime checks and new outputs before use.

Migration checks observed future Blender 6.0 deprecation warnings for `Material.use_nodes` and `World.use_nodes`. Verify affected APIs when changing versions; historical observations do not establish future compatibility.

[Research examples](library/blender-background-review/examples/README.md) were syntax-checked, not executed in the research. Related executed demo code does not make those examples tested.
