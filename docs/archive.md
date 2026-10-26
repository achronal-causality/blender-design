# Research archive and offline access

The original v1.1.0 package is preserved byte for byte at `.private/original-v1.1.0/` in the author's source checkout. This directory is ignored by Git. A complete private companion ZIP can be built and verified with:

```sh
python3 -B tools/release.py archive --snapshot .private/original-v1.1.0 --output .private/artifacts/blender-design-research-original-v1.1.0.zip
```

Choose an unused output path. The builder checks every original file against [the preservation inventory](preservation.json), then checks every ZIP member against the same hashes. The archive includes all original files, even files retained in the default release, so recovery does not depend on reversing public edits.

## Access status

No public archive download URL exists yet. The archive includes third-party captures and has not been cleared for public distribution. Do not upload it with the default release. It is a local preservation copy, not an off-device backup.

An authorized recipient with the companion ZIP can extract it outside the installed plugin and use `original-v1.1.0/` as the complete offline reference. The original package's checker can verify its historical indexed content, but does not check every extra file; the new archive command validates the full preservation inventory.

## Find a capture

[Research catalog](research-catalog.md) gives each relocated file a stable anchor, original relative path, archive member, byte count, and SHA-256. Public technical documents link to these exact entries. Source URLs and inspected ranges remain in the original source indexes and coverage metadata. An archive catalog entry is not the source's contents or proof that it was executed/read.

Public copies replace personal absolute paths with `/historical/author-home` or `/historical/user-home`; the exact originals remain in the private snapshot and archive. Original source hashes refer to original bytes. Public transformed hashes are recorded separately.

Future clearance can make a separate evidence download available without changing the working reference or silently replacing original captures.
