# ADR 0001: Separate public reference from private captures

- Status: accepted
- Date: 2026-10-26

## Context

The original 1.1.0 plugin bundled about 95 MB, predominantly source captures. The user requested publication cleanup without losing findings or information. Captures include mixed third-party rights and historical machine paths.

## Options

- Publish the original package unchanged: preserves immediate offline access but mixes rights, history, local paths, and operational guidance.
- Replace research with a short summary: smaller, but discards detail and uncertainty the user explicitly wants preserved.
- Keep the detailed reference in the default package, preserve the complete original separately, and map every transformation: modest installation with recoverable original evidence.

## Decision

Choose the third option. Preserve all original files byte for byte in an ignored private snapshot and verified companion archive. Keep the technical modules, claims, caveats, indexes, coverage, useful examples, and source citations in the default package. Redirect removed-file links to exact catalog entries. No archive publication is implied.

Use GPL-3.0-or-later for original code and CC BY-SA 4.0 for original prose, explicitly authorized by the user. Preserve third-party ownership and exclude uncleared whole captures. Use a new runnable example rather than modifying historical demos into apparent fresh evidence.

## Consequences

Default installation becomes smaller and clearer. Complete offline captured-source access requires the companion archive, whose public redistribution remains uncleared. Two inventories and link checks are required. Historical hashes identify original bytes; public transformations receive separate hashes. Installing or publishing this candidate does not automatically update the author's installed plugin.
