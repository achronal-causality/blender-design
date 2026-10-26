# Build a release

The working tree is the curated public source. `.private/` preserves original material; `build/` contains rebuildable results. Neither belongs in Git or the public ZIP.

1. Edit source, update the explicit `release-plan.json` when adding/removing files, and update preservation records for changes to imported content. Never overwrite the original snapshot.
2. Run `python3 -B tools/release.py seal` to regenerate hashes of exactly the planned files. Unexpected files are errors, not silently added.
3. Run `python3 -B tools/release.py check` and `python3 -B -m unittest discover -s tests -v`.
4. Build into a new output: `python3 -B tools/release.py build --output build/blender-design-1.2.0.zip`.
5. Extract into a clean path, check the extracted package, follow README installation with an isolated test Codex home, run the example, inspect its PNG, and inspect the saved scene through the separate reopen process.
6. Record results and limitations in `VALIDATION.md`, reseal and rebuild, then rerun extraction/checks on the final ZIP. A changed example requires a new Blender check.
7. Review `docs/licensing.md`, Git diff, and artifact inventory. Obtain approval before pushing or publishing. The private companion archive is a separate unresolved redistribution decision.

The JSON file list and hashes are integrity metadata, not an authenticity signature or a comprehensive secret scanner. The archive builder separately verifies every original byte. Do not replace this explicit packaging with a recursive ZIP of the checkout.
