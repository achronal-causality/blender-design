# Blender interface and working guide

## Execution interface

Codex reads these files and writes task-local Python. The installed Blender executable runs it inside its own process, providing `bpy`, `bmesh`, and `mathutils`. Host Python can orchestrate subprocesses; it does not acquire `bpy` by loading this skill. The plugin supplies knowledge and guidance, not an RPC server, Blender add-on, or separate modeling engine.

This needs file access, permission to execute Blender, and a way to inspect generated images. Tools and permissions vary by host. The bundle is readable offline and contains no executable Blender installation. Do not install standalone `bpy` into system Python as an implicit fix for `ModuleNotFoundError`.

## Runtime identity

The project's recorded executable is `/Applications/Blender.app/Contents/MacOS/Blender`. Confirm it exists. On another host, use its configured executable or application/PATH discovery; do not copy this macOS path blindly.

```sh
# EXAMPLE: for an actual Blender task; not run by skill loading.
"/Applications/Blender.app/Contents/MacOS/Blender" --version
```

`--version` prints version, build date, branch, hash and platform information and exits. Compare with the [recorded baseline](library/blender-background-review/BASELINE.md). Inside a job, `bpy.app.version` is an integer tuple; `bpy.app.build_hash` is bytes; `bpy.app.version_string` is a label; `sys.version` identifies embedded Python. Record relevant identity fields, not the whole environment.

```python
# UNEXECUTED FRAGMENT: before scene changes in a future job.
import bpy
import sys
runtime = {
    'blender': bpy.app.version_string,
    'version': list(bpy.app.version),
    'build_hash': bpy.app.build_hash.decode('ascii', errors='replace'),
    'python': sys.version,
}
print(runtime)
```

The baseline is evidence, not an instruction to reinstall an old application. Investigate affected APIs if the live build differs, and state adaptations and tests. Original demo scripts enforce their baseline; adapt a new copy when compatibility changes are needed.

## Background commands

For a new procedural scene, replace example absolute paths with actual task paths. Allocate a fresh output directory for the attempt; decide whether host or job creates it exclusively so both do not compete.

```sh
# UNEXECUTED TEMPLATE: write job.py for the current task.
"/Applications/Blender.app/Contents/MacOS/Blender" \
  --background --factory-startup --disable-autoexec \
  --python-exit-code 17 \
  --python "/absolute/task/job.py" \
  -- --output-dir "/absolute/task/new-attempt"
```

| Element | Semantics |
|---|---|
| Executable path | Launches Blender with its embedded Python and native libraries; quoting preserves spaces. |
| `--background` | Omits interactive UI; does not make context-dependent operators valid or supply an interactive timer/modal loop. |
| `--factory-startup` | Uses factory startup data instead of the user's saved startup scene; not an empty scene or complete environment sandbox. |
| `--disable-autoexec` | Blocks automatic Python execution from loaded content, not the explicit script. Scripted drivers may need a deliberate trust decision. |
| `--python-exit-code 17` | Makes uncaught command-line Python failure nonzero. Must precede the script. 17 is an example choice of failure code. |
| `--python /.../job.py` | Runs the file inside Blender. The job controls scene changes and synchronous output work. |
| `--` | Ends Blender option parsing; the job parses the tail of `sys.argv`. |
| `--output-dir ...` | Our job's option, not a Blender option; the script must implement it. |

For revision, load the existing scene before the edit script:

```sh
# UNEXECUTED TEMPLATE: save a new output and preserve input.blend.
"/Applications/Blender.app/Contents/MacOS/Blender" \
  --background --disable-autoexec "/absolute/task/input.blend" \
  --python-exit-code 17 --python "/absolute/task/revise.py" \
  -- --output-dir "/absolute/task/revision-attempt"
```

The `.blend` positional argument loads the scene. Later loads/resets can erase assignments and invalidate references; reacquire datablocks after loading. A script may instead use `bpy.ops.wm.open_mainfile(filepath=...)` with the same lifetime constraints. Blender's `//` path prefix is relative to the `.blend`, not the script or shell directory.

Host automation should use `subprocess.run` with an argument list, explicit working directory, output logs and a suitable timeout. Do not interpolate a brief into a shell command. Inspect return status and artifacts, including native crashes and timeouts. The [unexecuted host example](library/blender-background-review/examples/host_job.py) illustrates mechanics; its paths and completion record are examples, not a mandatory framework.

## Construction and revision

- Separate meaningful parameters from derived geometry. Prefer native curves/modifiers/nodes where they express the relationship well.
- Objects and mesh datablocks differ. Shared geometry changes all objects using it; decide when to copy. Link objects into the intended collection.
- Direct data access often avoids unnecessary context. For operators, handle polling/context and result; `{'CANCELLED'}` is distinct from a Python exception.
- Update/evaluate before measuring derived geometry. Original data omits modifier results. Release temporary meshes and discard wrappers invalidated by deletion, reset or file loading.
- Use identifiers proportionate to the scene. Repeated creation can add `.001` duplicates. Scope revisions to intended parts and preserve unrelated data.
- Exceptions do not undo earlier mutations. Retain failed outputs/logs, repair the script, then use a new process and destination.

Exact contracts: [ownership](library/blender-background-review/modules/02-data.md), [evaluation](library/blender-background-review/modules/03-context.md), [revision](library/blender-background-review/modules/09-revision.md).

## Feedback and acceptance

Check relationships tied to the brief: finite geometry, attachment coincidence, symmetry, bounds, selected clearances, counts, or behavior at relevant parameter values. Cartoon squash/stretch can intentionally violate world-space rigid lengths; check the invariant in its intended representation.

Static inspection defaults to Cycles CPU and PNG. These are reference settings, not renderer restrictions; the animation demo used EEVEE. Lighting, camera, normals and color management can mislead. Inspect actual renders. For animation inspect motion/timing through a movie or sufficient frames; a still cannot establish springiness.

Save editable `.blend` output with its generator/parameters. Reopen important deliverables in a fresh process to inspect structure and external dependencies. Export requested formats and explain losses such as OBJ discarding procedural stacks, animation and Blender materials. Zero exit status or a nonempty file alone is weak acceptance evidence.

For analysis/planning requests, do not run construction. For requested models/changes, complete authorized construction and verification; research-era instructions saying examples remain unexecuted do not prohibit new work.

## Search the library

From this skill directory:

```sh
rg -n -F 'bpy.data.objects' references/library/blender-background-review
rg -n --glob '*.md' 'context is incorrect|ReferenceError|stale output' references/library/blender-background-review
```

`rg` is ripgrep; `-n` includes line numbers; `-F` means literal text; `--glob '*.md'` limits files to Markdown; `|` means alternatives in a regular expression. These only read files. Ordinary file search is a valid fallback; ripgrep is not a mandatory new dependency.

The preserved research README's shorter commands target `blender-background-review` from its parent directory, `references/library`. If already inside `blender-background-review`, use `.` as the search target. The commands above instead use the skill directory as their explicit base.

The [task index](library/blender-background-review/TASK_INDEX.md), [API index](library/blender-background-review/API_INDEX.md), [source index](library/blender-background-review/SOURCE_INDEX.md) and [coverage manifest](library/blender-background-review/coverage.json) lead to full captured units and inspected ranges. The preparations explain the original route choice; new requirements may warrant revisiting it.
