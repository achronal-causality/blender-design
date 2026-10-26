# External assets in a procedural design

Start with the brief and a coherent native Blender construction. External assets are optional inputs when they serve the design; a request for everything from scratch excludes downloaded assets. No provider is the default or a prerequisite. The [source directory](asset-sources.md) describes possible sources, and the [Poly Haven utilities](polyhaven.md) implement one optional, bounded acquisition path.

## Choose a representation and an asset

Decide what the scene needs: a modeled component, material maps, an HDRI, or reference geometry. Judge silhouette, style, topology, editable structure, resolution, and resource cost against the brief. Choose the actual item and variant rather than treating a catalog ranking, preview, or advertised dimensions as acceptance evidence. Keep downloaded geometry distinguishable from geometry authored procedurally.

## Check the intended use and access route

Read the item's license and the provider's current terms before acquisition. Distinguish rights to use an asset in a render from rights to deliver raw files or an editable scene containing it. Record attribution, redistribution limits, third-party exceptions, and branding/personality restrictions relevant to the intended use. A free download, an open-source add-on, or an API endpoint does not itself grant asset rights or authorize bulk access.

Use the provider's documented website, download links, API, or an explicitly selected add-on. Check account/payment requirements, API terms, request limits, and actual variant availability. Do not bypass access controls or install an add-on as an implicit dependency of this skill. Add acquisition scripts only when concrete recurring needs justify them.

## Preserve dependencies and provenance

Choose a bounded download size and a fresh destination. Keep the original payload and relative dependency layout, including textures, material sidecars, linked libraries, and any required caches. Inspect archive members before extracting; reject escaping paths and unplanned executable setup. Avoid flattening folders or assuming a single model file is self-contained.

Keep a short note or JSON receipt with the provider/item URL, creator, item ID, selected variant/format/resolution, acquisition date, license/terms URLs and review date, included license files, and original file hashes. Distinguish a captured policy from an original summary linking to it. Record local modifications, unit/axis conversion, and dependency mapping separately from the original files. This does not require a universal schema, database, or provider framework. Byte verification establishes identity, not quality or authorship.

## Import with Blender's own interfaces

For native `.blend` content, inspect available datablocks and deliberately append or link the intended objects/collections using `bpy.data.libraries.load`; appending (`link=False`) and linking have different editability and dependency consequences. Select specific content, including a particular level of detail, rather than loading every alternative into the scene.

For interchange files, use the importer supported by the actual Blender build through its native Python interface. Check format-specific options and operator context; do not assume all listed providers offer every format or that an importer's existence proves compatibility. For texture sets, wire the appropriate material nodes, UVs, color spaces, normal convention, and displacement deliberately. For HDRIs, configure the World rather than treating an image as a model. An official provider add-on is an optional acquisition route; native Blender data and APIs remain the scene construction and inspection interface.

Disable automatic embedded script execution when loading external content, as in the [working guide](working-guide.md). Explicit scripts still execute intentionally, and this setting is not a complete OS/native-parser sandbox. Preserve an input and use a fresh output when testing an unfamiliar file. See [data ownership](library/blender-background-review/modules/02-data.md), [evaluation/context](library/blender-background-review/modules/03-context.md), and [persistence](library/blender-background-review/modules/08-persistence.md) for the existing scoped API findings and source references.

## Verify in the actual scene

Measure evaluated bounds, orientation, units, and attachment/clearance relationships against known scene references. Account for unapplied transforms and modifiers before changing scale. Inspect topology/normals, assigned materials, image paths, missing maps, shader support, and the chosen render engine. A catalog size or thumbnail is not a unit, material, or appearance guarantee.

Render controlled views and judge appearance, framing, and consistency with procedural parts. Save the editable scene and reopen important outputs in a fresh process after relocation. Pack supported resources or retain an explicit relative dependency layout; inspect linked IDs, images, fonts, caches, and other external paths. A packed image or a successful import alone does not prove portability. Deliver only what the item's terms permit, together with source credit and bounded verification results.

## Evidence boundary

This is shared guidance, not a claim that every provider or format has been exercised. The [source directory](asset-sources.md) is dated documentation research. The existing [Poly Haven utility evidence](polyhaven.md#acceptance-and-tested-scope) covers one historical native collection import and helper tests, not universal catalog compatibility. The core folding-divider example uses no external assets.
