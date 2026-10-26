# Blender Design release source

Preserve `.private/original-v1.1.0/` byte for byte. Do not execute historical installers or overwrite recorded evidence. `.private/` is local only and must never be staged or published.

Use the release builder to produce explicit-file-list artifacts; never zip the whole checkout. Changes to the default/archive split need a preservation inventory update. Keep findings, caveats, claim IDs, and unexecuted-test status intact.

Run `python3 -B tools/release.py check`, unit tests, and artifact verification after changes. Use fresh example output directories and inspect renders after Blender changes. Do not update the installed plugin as a side effect. Pushes and publication require user approval.
