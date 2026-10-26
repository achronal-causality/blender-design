# Blender preparatory investigations

Completed on **15 September 2026**, before any capability test.

## Results

- **Blender updated:** 5.2.0 LTS → **5.2.2 LTS**, the current official stable release at inspection. Installer checksum, installed signature and notarization assessment passed; inspected configuration files remained unchanged.
- **Recommended deep-dive target:** native Python scene construction and revision in Blender 5.2.2, executed as controlled background jobs.
- **Strongest alternative:** Blender MCP for persistent GUI-scene editing. Selecting that route adds transport, scheduling and observation behavior to the research subject.

## Reports

1. [Preparation A: technical baseline](PREPARATION_A_TECHNICAL_BASELINE.md) establishes build/source identity, documentation precision, Python environments, update verification and remaining uncertainty.
2. [Preparation B: route selection](PREPARATION_B_ROUTE_SELECTION.md) compares execution routes and integrations, traces consequential implementation paths, checks examples and user reports, and proposes a narrow research boundary.
3. [Source coverage](SOURCE_COVERAGE.md) states what was fully read, inspected selectively, merely captured or inaccessible.

The reports are self-contained, written for a technical audience. Every command exposed as part of the diagnostic or recommended workflow is explained.

## Verification and records

[Installation receipt](../../../../../docs/research-catalog.md#file-e7e8a4d8e67100a6) · [installer checksum](../../../../../docs/research-catalog.md#file-83c20cd629b12e6b) · [installed/source comparison](../../../../../docs/research-catalog.md#file-9b02268e0c32c493) · [delivery validation](VALIDATION.json)

The previous application is retained in [temporary rollback storage](../../../../../docs/history.md). Temporary storage may be cleaned by the system; it is not a permanent backup.

No integration was installed, no capability test ran, and no project scene was generated. Only the Blender update expanded the original read-only scope, following your explicit instruction.

## Decision pending

Choose the **native background-script** research boundary or the **live Blender MCP** boundary described in Preparation B, or revise that boundary. The separate exhaustive deep-dive plan follows that selection; neither route has been silently selected or started.

