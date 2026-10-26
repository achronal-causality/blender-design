# ADR 0002: Make asset guidance provider independent

- Status: accepted
- Date: 2026-10-26

## Context

The original skill selected Poly Haven as its sole catalog. The user requested a shared workflow and a short directory of six sources while retaining useful, tested helpers and all findings/evidence. The core product is procedural Blender design and portable technical knowledge.

## Options

- Retain a selected catalog: limits guidance to one provider despite the brief and format varying by task.
- Add a universal provider interface and multiple integrations: adds unrequested runtime and maintenance work without a demonstrated recurring need.
- Separate shared asset reasoning from a dated source directory and optional provider-specific tools: generalizes guidance without inventing tested capabilities.

## Decision

Choose the third option, as explicitly requested. No provider is the default. Use native Blender construction first, then choose optional assets according to the brief, item terms, dependencies, provenance, native import, dimensions/materials, and actual appearance. Keep the existing Poly Haven scripts and tests unchanged, with their bounded historical and current evidence distinguished.

Add documentation research for Poly Haven, ambientCG, Kenney, Quaternius, NASA 3D Resources, and BlenderKit/Blendkit. Listing a provider establishes neither automated access nor import compatibility. No new provider integrations, accounts, add-ons, or universal framework are introduced. Future scripts require concrete recurring needs.

## Consequences

The skill no longer promotes the historical catalog choice into a present default. That operational policy is superseded, while its original wording/evidence remain recoverable from the private v1.1.0 snapshot and Git history at `67ce88a`. All technical findings, qualifications, and source citations remain. Source descriptions need dated primary-source rechecks; actual acquisitions/imports still need item-specific verification.
