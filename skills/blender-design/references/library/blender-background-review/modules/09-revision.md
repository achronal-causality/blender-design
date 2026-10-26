# 09. Controlled revision and failure recovery

## Purpose and prerequisites

Revise intentional data without duplication and reject partial or stale results. Read [execution](01-execution.md), [ownership](02-data.md), [evaluation](03-context.md) and [persistence](08-persistence.md). This module's orchestration policy is explicitly **inference/design guidance**, supported by the documented ownership and failure mechanisms. It has not been exercised against Blender.

## Mental model and invariants

There are two valid revision modes:

- **Rebuild from parameters:** create a fresh scene from versioned source and parameters. Edits not represented in those parameters are intentionally absent.
- **Reopen and revise:** load a previous `.blend`, identify owned parts, preserve unrelated content, apply a bounded change and save to a new path.

Do not silently switch between them. A procedural rebuild is reproducible only to the degree its inputs, resource files, Blender revision and effective settings are controlled. A `.blend` alone may preserve editability without preserving the external generator. [C26](../CLAIMS.md#c26).

A Python exception is not an undo transaction. Datablocks, attributes, collection links, modifier settings and disk files created before the exception may remain. `try/finally` ensures Python cleanup on ordinary exceptions; it cannot recover from every native crash, kill or power failure. A fresh Blender process prevents the next job from inheriting a failed process's in-memory state, while fresh output paths prevent old files from masquerading as new results. [C27](../CLAIMS.md#c27).

## API contracts and revision policy

### Locate existing data

Use an explicit application namespace in ID custom properties, a schema version and a stable part key. These are application contracts, not built-in Blender identities. Restrict selection by ID type and local ownership; reject multiple matches. Names can be renamed/uniquified, array indices can shift, and `session_uid` is not a cross-process contract.

```python
# UNEXECUTED: exact semantic lookup; missing is distinct from ambiguous.
def find_part(objects, owner, part_key):
    matches = [o for o in objects
               if o.get('review_owner') == owner and o.get('part_key') == part_key]
    if len(matches) > 1:
        raise RuntimeError(f'Ambiguous owned part: {part_key}')
    return matches[0] if matches else None
```

`objects` should be the intended scene/owned collection's object set or a deliberately scoped `bpy.data.objects`; a global query can find unrelated scene content with copied keys. `ID.get(key)` reads a custom property without creating it. A missing match permits construction only in the chosen rebuild/update policy. A type mismatch, linked data, unknown schema or duplicate key is a conflict, not permission to delete candidates until one remains.

### Stage geometry before replacement

A direct Mesh constructor can create and validate a candidate Mesh before changing `obj.data`. This localizes ordinary failures. It does not make changes after the swap transactional. Keep the old mesh until the new assignment and required inspections succeed; remove it only if verified owned and zero-user. Shared meshes require an explicit share/copy decision first. Reusing a shared material or node group can mutate other objects even when the mesh itself is staged.

```python
# UNEXECUTED: replacement policy, assuming candidate is fully built and validated.
old_mesh = obj.data
obj.data = candidate
bpy.context.view_layer.update()
# Evaluate required counts/bounds/attributes here before accepting the revision.
if old_mesh.users == 0 and old_mesh.get('review_owner') == OWNER:
    bpy.data.meshes.remove(old_mesh)
```

`candidate` must be an original Mesh ID in Main, not `to_mesh()` temporary data. `OWNER` is an application-defined string. The comment is a deliberate task-specific acceptance step, not a supplied test that has already passed. If acceptance fails after swap, a still-valid `old_mesh` could be restored before deletion, but a fresh process and new output are the simpler failure boundary. Do not delete the old mesh before you can use it for recovery.

Revising topology can invalidate point/edge/face selection and application annotations tied to indices. Stable feature IDs need a defined propagation/re-identification rule. Named attributes may help, but modifiers can interpolate, duplicate or discard values. Node-interface revisions similarly require identifier preservation and schema checking; a new socket with the same display name is not necessarily the same parameter.

### State ownership across retries

The minimal acceptance record should contain job identifier, Blender version/hash, script/parameter digest, input `.blend` digest if any, output paths/digests and the intended scene/part keys. A JSON file is sufficient; no database or service is needed. Store only relevant environment/settings, not a dump of credentials or the entire host environment.

An output directory is **fresh** when the caller creates it exclusively and it did not previously contain artifacts. A retry gets a different directory. Do not delete failure evidence to simulate freshness. Timestamps alone can be ambiguous due to filesystem granularity; a unique directory plus explicit content digests establishes association more strongly. A digest proves identity of bytes, not correctness of geometry.

**Stale output detection** means rejecting files from an earlier or incomplete attempt even when their names and formats look correct. Freshness, matching provenance and semantic validity are three distinct checks.

### Host-side execution and artifact acceptance

The unexecuted [host_job.py](../examples/host_job.py) uses `subprocess.run` with an argument list, a fixed executable, explicit working directory, bounded timeout and separate stdout/stderr files. It checks the return code and a completion record. The host does not import Blender. A signal termination can appear as a negative return code on POSIX; preserve the actual return value and logs. `TimeoutExpired` is a distinct outcome, not an unhandled modeling exception.

A complete future acceptance sequence is:

1. Create a unique job directory and preserve source/parameters or their digests.
2. Launch the pinned application with exception exit handling established before the script.
3. In Blender, verify identity before mutation; construct/revise; refresh and inspect expected geometry.
4. Configure/save `.blend`, request a synchronous PNG, and export the bounded OBJ if requested.
5. Check operation statuses **and** required artifacts. Validate the PNG signature/dimensions; inspect OBJ's expected nonempty geometry and required MTL/resource files. A nonempty file is only a minimal transport check.
6. Write a completion record last. Let an independent future reopen/visual check decide capability acceptance.
7. On any failure, retain logs and partial files, mark the attempt failed and start a new process/directory for a repaired attempt.

A script-written completion record is a claim by the script, not independent verification. The host should verify listed paths remain inside the intended output root and recompute hashes; later capability tests must reopen and inspect the saved file. The examples distinguish this record from a tested acceptance suite.

## Implementation traces

`bpy_operator_function.cc:115 - 435` converts reports after operation execution, so error reporting does not imply no mutation. `bmesh_py_ops_call.cc:760 - 870` likewise executes before converting operation errors. `object_modifier.cc:1991 - 2078` iterates objects and can continue after per-object failure. `writefile.cc:1889 - 2064` remaps paths and writes before final rename. `io_obj.cc:89 - 138` plus `obj_exporter.cc:351 - 361` establishes warning-only no-output success. [Pinned ranges](../SOURCE_TRACES.md), [claims](../CLAIMS.md#c27).

## Failure modes and diagnosis

| Symptom | Recovery policy |
|---|---|
| Duplicate `.001` objects | Stop unconditional creation; enforce unique owner/part lookup |
| Ambiguous owner key | Preserve all candidates; require deliberate migration or new key, not arbitrary first match |
| Exception after material/mesh creation | Preserve logs; clean only verified owned unlinked candidates or discard process |
| Save succeeded, render failed | Partial job; don't publish it as complete merely because `.blend` exists |
| Old PNG remains after new failure | Output root was reused or freshness unchecked; allocate a new root |
| Run returns zero after caught error | Reraise/explicitly fail, and require the acceptance record plus artifact checks |
| Reopened references point nowhere | Reacquire IDs after load; don't reuse previous wrappers |
| Global cleanup removed another asset | Ownership boundary violated; use scoped removals and preserve previous accepted files |

## Evidence and open questions

D/S establish why partial mutation is credible. I supplies staged replacement, unique directories and independent acceptance. The reference does not claim filesystem crash consistency or bitwise deterministic rendering. [T01 - T03, T06 and T08](../FUTURE_TESTS.md) exercise these boundaries later. A native crash prevents ordinary Python cleanup; process-level failure isolation remains necessary even with careful `finally` blocks.
