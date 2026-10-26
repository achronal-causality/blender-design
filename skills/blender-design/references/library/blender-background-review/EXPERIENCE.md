# Firsthand reports and contradictions

**Classification: R, reported experience.** Reports were selected for concrete failure mechanisms, not popularity. No reproduction attachment, screenshot, video or linked `.blend` was executed. Issue status alone does not establish that the pinned macOS build reproduces or fixes a report. Public issue bodies/comments were captured through Blender's API after browser access was blocked; the access route and hashes are retained. Stack Exchange API responses include full question/answer bodies and question comments, with `has_more=false`; answer-comment threads were not separately collected.

## R6101

**[Operator context question](https://blender.stackexchange.com/questions/6101/)**. Original question from the Blender 2.x era; answers revised across later versions, with both legacy and `temp_override` patterns. Platform/build of the original question is not specified. Reproduction symptom is `RuntimeError ... poll() failed, context is incorrect` for a View3D operation.

The discussion identifies editor/mode/context prerequisites and shows attempts to supply a real Area. It also acknowledges that an override did not correctly achieve the target behavior. Some examples retain removed APIs, a first-positional override dictionary or an undefined `context` name. An “any Blender version” wrapper still assumes a real window/screen and changes UI area type without fully robust exception restoration. These are historical examples, not a usable headless recipe.

**Resolution/relevance:** explanatory discussion rather than a tracked pinned-build fix. Current `bpy_operator_function.cc` and `bpy_rna_context.cc` establish the reviewed 5.2 contract. Prefer direct data, valid context and immediate execute operations. [Module 03](modules/03-context.md). Captures: [questions](../../../../../docs/research-catalog.md#file-3f082ca6d96cc772), [answers](../../../../../docs/research-catalog.md#file-b1534ef8f6900eef), [question comments](../../../../../docs/research-catalog.md#file-a01720afdb5d289c).

## R323805

**[Stale light data in background mode](https://blender.stackexchange.com/questions/323805/)**. September 2024. Reporter suspected Blender 4.1; their platform and complete invocation were not established. Code sets frames 1/3, updates the ViewLayer and reads light energy, reporting identical values despite expected animation changes.

A respondent reported correct behavior in 4.2 and later in 3.6/4.0/4.1/4.2, showing an explicit Windows command that loads the correct `.blend` before running the script. The response asks about actual keyframes and invocation; no final reporter confirmation resolves the discrepancy.

**Resolution/relevance:** unresolved and contradicted, not proof of a background evaluation defect. The study excludes animation authoring; this report tests the broader inference that stale observations may come from wrong input/context as well as missing evaluation. Verify loaded file, original/evaluated data and graph boundary before diagnosing Blender. [Module 03](modules/03-context.md), T05. Same three Stack Exchange captures above.

## R99755

**[Background process does not exit](https://blender.stackexchange.com/questions/99755/)**. Blender 2.79 Linux glibc219 x86_64, Ubuntu 16.04.3 LTS, lowlatency kernel 4.4.0-112. The reporter supplied a minimal print script and background invocation; even a single-frame render reportedly failed to exit.

An accepted short answer suggested explicitly quitting Blender. The reporter's later answer instead attributed the problem to JACK/QJackCtl audio configuration and reported that disabling audio allowed normal exit. A Windows 10 answer used a different, non-background command and discussed a quit prompt. These are not equivalent reproductions.

**Resolution/relevance:** reporter workaround on an old Linux environment, no current macOS reproduction. Do not add a forced quit to every 5.2 background job: pinned startup already exits after final actions. Keep a host timeout and distinguish script completion from native shutdown. [Module 01](modules/01-execution.md), T01/T08. Same Stack Exchange captures above.

## R105715

**[Freeing an Edit Mode BMesh leaves subsequent wrappers dead](https://projects.blender.org/blender/blender/issues/105715)**. Windows 11, Blender 3.5. Reproduction obtains `bmesh.from_edit_mesh`, updates, calls `free`, then retrieves another wrapper; reported result is a dead BMesh until Edit Mode is restarted. [Body](../../../../../docs/research-catalog.md#file-4cd2e23dc5bf8368), [all 1 comment](../../../../../docs/research-catalog.md#file-41d44adbd2ad2c15).

The comment identifies borrowed versus newly allocated ownership. Issue is closed; captured comments do not provide a fix commit. Pinned `bmesh_py_types.cc` explicitly references this issue and clears the wrapper handle for the wrapped case, while preserving Blender-owned BMesh memory.

**Resolution/relevance:** source establishes a changed wrapper mechanism, not an executed reproduction. The robust caller contract remains: do not free a borrowed Edit Mode BMesh. [Module 04](modules/04-mesh.md), T07.

## R119202

**[Area-close context regression](https://projects.blender.org/blender/blender/issues/119202)**. Windows 10, RTX 3050 Ti; broken 4.1 Alpha `76bf43f44d0c`, worked `23430f4db868`. Supplied reproduction closes several areas from a Text Editor script; `.blend` and crash attachment were not inspected. [Body](../../../../../docs/research-catalog.md#file-c1c24510504b1cec), [all 4 comments](../../../../../docs/research-catalog.md#file-8997ed4d72d03a7f).

Maintainers bisected a cause and reported a fix, while requiring the script to retain the screen before context-clearing operations. They explain that intentional context changes must not always be undone by the temporary override manager. Pinned context restoration code cites the issue and validates whether old UI members still exist.

**Resolution/relevance:** UI operation is excluded, but the source-backed lesson applies: temporary context restoration is not unconditional restoration after data/UI destruction, and it is not scene rollback. No need for an editor bridge follows from this report. [Module 03](modules/03-context.md).

## R72807

**[Blender fails to start with conflicting Python paths](https://projects.blender.org/blender/blender/issues/72807)**. Windows 10 64-bit, GeForce GT 710, Blender 2.81a; conflicting Python installation clarified as Python 3.8.1 32-bit. Error imports `io.py` from the external installation and cannot import `open_code`. [Body](../../../../../docs/research-catalog.md#file-7ecc397cf1ba9ecd), [all 19 comments](../../../../../docs/research-catalog.md#file-680c7c1df0158937).

The reporter initially confused Blender/Python version numbers; later messages identify `PYTHONPATH` entries for the external 32-bit Python. A maintainer reproduced the breakage, and the issue was marked resolved with commit `7c2f0074f3fe2411daa7a6e351d7cbc535246871`. The reporter also described a local path/reinstall workaround; this is not a recommended action here.

**Resolution/relevance:** pinned `bpy_interface.cc` explicitly cites this issue while choosing isolated Python initialization. Enabling system environment behavior can reintroduce the class of mismatch; no external Python dependency is needed for the reference. [Module 01](modules/01-execution.md).

## R129657

**[SIGPIPE closes Blender instead of raising a Python exception](https://projects.blender.org/blender/blender/issues/129657)**. Gentoo Linux; reported 4.2.1/4.2.3 LTS, system Python 3.11/3.12, both distribution and official builds. A socket write after closing the peer allegedly terminates Blender. [Body](../../../../../docs/research-catalog.md#file-4a11e7b004e6cdce), [all 6 comments](../../../../../docs/research-catalog.md#file-0854a5e418432bd9).

Several maintainers could not reproduce the initial sequence and observed `BrokenPipeError` instead. A later maintainer reproduced with repeated larger writes while closing the peer. The issue is closed, but the captured comment response does not itself prove a fix commit. The pinned embedded-Python initialization comments reference signal-handler behavior and this report.

**Resolution/relevance:** preserves contradictory initial results and stronger later reproduction. Network bridges are excluded. The applicable lesson is that a native signal can be distinct from a Python exception and bypass ordinary cleanup; a fresh process and host logs are useful. Do not alter signal handlers based solely on this old report. T01/T08.

## R96721

**[Dynamic Geometry Nodes material assignments and exporters](https://projects.blender.org/blender/blender-addons/issues/96721)**. Blender 3.1.0 `c77597cd0e`; platform unspecified. Reproduction joins geometry with different materials, exports with modifiers enabled, reimports, and sees one material; applying the modifier first reportedly works. [Body](../../../../../docs/research-catalog.md#file-e5dd17f05f0f3558), [all 18 comments](../../../../../docs/research-catalog.md#file-1179c1c531dcaf88).

The discussion distinguishes original material slots, evaluated mesh materials and object-level overrides. Its checklist marks the C++ OBJ exporter fixed by `d3eef4d22a021bf71c5e6cac492139cab397e4d2`; the overall issue remains open for other formats. Pinned `obj_export_mesh.cc:67 - 69` reads evaluated material assignments.

**Resolution/relevance:** source substantiates evaluated material lookup for this route. The report does not establish lossless MTL translation of procedural shaders or receiver compatibility. [Module 08](modules/08-persistence.md), T09.

## R160212

**[5.2 Pixel socket subtype crashes when opened in 5.1](https://projects.blender.org/blender/blender/issues/160212)**. Linux el9 x86_64/X11, RTX 4070/Vulkan; file authored in Blender 5.2.0 LTS Beta `2a1ca5553bac`, crash reported in 5.1.2. Steps create a Geometry Nodes Float input with Pixel subtype, save and open in the older version. [Body](../../../../../docs/research-catalog.md#file-ba20592b638a4557), [all 6 comments](../../../../../docs/research-catalog.md#file-016b7575549bf73a).

Maintainers confirm and propose write-time/read-time compatibility handling. The issue is closed, but the captured comments do not include the final implementation/merge receipt. No reproduction file was opened, and this review does not claim the fix was independently verified.

**Resolution/relevance:** useful evidence against assuming forward compatibility means lossless/safe behavior for every new socket subtype. The fixed 5.2.2 study does not require older-version round trips. Typed modifier-input migration is established independently by source, not by this report. [Modules 06](modules/06-nodes.md) and [08](modules/08-persistence.md), T10.

## R144340

**[Deletion with custom normals and modifiers freezes](https://projects.blender.org/blender/blender/issues/144340)**. Windows 10, RTX 3070/Vulkan; broken 5.0 Alpha `e0170883d428`, reportedly worked 4.5. Delete all vertices of an attached mesh; removing custom normals or disabling modifiers reportedly avoids the freeze. [Body](../../../../../docs/research-catalog.md#file-ccfd5fe4440ab80a), [4 comments captured](../../../../../docs/research-catalog.md#file-3e5e2f4bab5a043c).

Comments confirm a hang and debate GPU-worker waiting versus mesh normal-cache recursion. The report body and all comments' narrative were read; the lengthy native stack was only partially inspected. Attachment geometry was not inspected. Closed status and a “thanks” comment do not independently establish the final fix or applicability to 5.2.2 CPU background rendering.

**Resolution/relevance:** warns against equating a normal-cache or draw failure with invalid topology without evidence. The pinned mesh API's lazy normal access is independently inspected; no claim of reproducing this GUI hang is made. [Module 04](modules/04-mesh.md), T07.

## Search and access record

Discovery searches covered operator context, stale references and deferred updates, normals/modifiers, node migration, render/process exit and dependency paths. Search snippets were not used as completed reading. Browser access to Blender Projects was blocked by robots policy; public API capture succeeded for the selected issues. Wrong documentation/source paths and their corrections are retained in the corpus additions and failed-attempt receipts. Reports without a known platform/version/resolution retain those gaps explicitly rather than guessing.
