# 01. Execution and environment

## Purpose and prerequisites

Understand which process executes Python, what startup supplies, and what a caller can infer from termination. Prerequisite: [baseline](../BASELINE.md). Continue with [data ownership](02-data.md) before writing modeling code.

## Mental model and invariants

A background job is a Blender application process with its embedded Python interpreter. The host starts Blender; Blender initializes its resource paths, preferences/startup scene, RNA API and registered engines; command-line actions load data and run Python; the background branch terminates after those actions. `bpy` is available because Blender initialized it. Launching the bundled `python3.13` executable alone does not initialize Blender or create an importable standalone `bpy` distribution.

A new process isolates Python globals, `sys.modules`, live IDs, evaluated caches and handler registrations from another process. It does **not** isolate the filesystem, environment, user resources, network, external textures, other processes or application installation. A fresh process is a recovery boundary for in-memory partial mutation, not a transaction over output files. [C01 - C03](../CLAIMS.md#c01).

There is no normal interactive event loop after background argument processing. Do not depend on a modal operator, future timer callback or redraw to finish a job. The regular Python call must reach its intended completion. Worker threads may exist inside Blender's implementation; that does not authorize calling `bpy` concurrently from Python threads.

## API contracts

### Startup and argument order

**Unexecuted reference command:**

```sh
/Applications/Blender.app/Contents/MacOS/Blender \
  --background --factory-startup --disable-autoexec \
  --python-exit-code 17 \
  --python /absolute/job.py -- --output-dir /absolute/new-job
```

| Token | Contract and consequence |
|---|---|
| Absolute executable path | Avoids resolving a different Blender through `PATH` |
| `--background` / `-b` | Runs without normal UI; background processing ends after command-line work |
| `--factory-startup` | Selects factory startup instead of the user's saved startup; it does not mean an empty scene, a clean OS environment or a security sandbox |
| `--disable-autoexec` / `-Y` | Disables automatic execution of embedded Python such as registered text/driver behavior where governed by this setting; explicitly supplied `--python` is still intentional code execution |
| `--python-exit-code 17` | Nonzero code to use when command-line Python execution fails; place before the script. `17` is this review's arbitrary distinguishable failure code, not a Blender constant. Zero disables this override |
| `--python /absolute/job.py` / `-P` | Executes the script in Blender; a normal Python exception produces a traceback and a failed script result |
| `--` | Ends Blender's normal option handling; original `sys.argv` remains available to Python |
| `--output-dir` | An example **script-defined** option; Blender does not implement it |

For a revision job, put `/absolute/input.blend` before `--python /absolute/revise.py`. Loading a file after setting a scene option can replace that option. Render actions execute at their position in the action sequence; settings intended for the render must precede it. Startup parsing uses multiple passes (environment, settings, GUI-related, forced settings, final actions), so the manual's ordering advice is not a claim of a single uniform left-to-right parser. The safe recipe explicitly initializes options early, loads before scripting, and configures/render/saves within one script. [CLI manual](https://docs.blender.org/manual/en/5.2/advanced/command_line/arguments.html), [C01](../CLAIMS.md#c01).

`--python-expr` executes a literal expression/string as Python; `--python-text` executes a named Text datablock already loaded; neither is needed for the reference workflow. `--addons` alters the enabled add-on set for that process and is excluded from the default. `--threads` controls Blender's requested thread count, not a complete limit on every native dependency. `--offline-mode` is application policy, not an OS network sandbox.

### Python namespace, imports and paths

`--python` creates a `__main__` namespace with `__file__`. Consecutive script invocations still share the process and imported modules; replacing the main namespace is not interpreter isolation. `sys.argv` includes Blender arguments, so parse only the tail after `--`. Explicitly add the directory of a trusted local helper if needed; do not assume the shell's current working directory equals the script directory.

```python
# UNEXECUTED: argument and local-import fragment inside Blender.
import argparse
import sys
from pathlib import Path

script_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(script_dir))  # Trusted sibling modules only.
args_tail = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
parser = argparse.ArgumentParser()
parser.add_argument('--output-dir', required=True, type=Path)
args = parser.parse_args(args_tail)
output_dir = args.output_dir.resolve()
```

`argparse` parses the script's options and rejects unknown/missing required options; its help/error path raises `SystemExit`, a separate Python exit mechanism. `pathlib.Path` represents filesystem paths; `resolve()` produces an absolute normalized path (it is not a guarantee that a target exists or is writable). `sys.path.insert(0, ...)` gives that directory import priority and can shadow modules, so keep it task-specific. `__file__` identifies the script; `Path.cwd()` would identify process working directory instead.

Blender's `//` convention is relative to the current `.blend` file, not Unix root, script location or CWD. `bpy.path.abspath(path, start=..., library=...)` resolves Blender paths, optionally against an explicit base or linked library; `bpy.path.relpath` creates a Blender-relative path. For an unsaved scene, use absolute paths rather than pretending `//` has a durable file base. Non-ASCII paths are supported, but filesystem byte encoding and strings are separate; use Python path APIs rather than lossy ASCII conversion. [Path reference](https://docs.blender.org/api/5.2/bpy.path.html).

### Environment and dependencies

| Interface | Meaning and default policy |
|---|---|
| `bpy.app.binary_path` | Blender executable path suitable for starting another Blender process; inspect rather than substituting `sys.executable` |
| `sys.executable` | Embedded interpreter's configured bundled Python executable in this build |
| `bpy.app.version`, `version_string`, `build_hash`, `background` | Runtime version tuple, label, revision bytes and execution-mode flag; validate before mutation |
| `PYTHONPATH`, `PYTHONHOME`, user site packages | Python import/runtime overrides. Default embedded startup uses isolated `PyConfig`; enabling environment support can reintroduce incompatible libraries |
| `--python-use-system-env` | Enables Python environment integration; pinned parser also enables user environment handling. It does not replace Blender's versioned API |
| `--python-use-user-env` | Pinned-source option for user Python environment behavior; selected manual omission is recorded. Avoid for reference jobs |
| `BLENDER_USER_RESOURCES` | Alternate user resource root; more-specific resource variables can override locations. Use only in a later explicitly configured job |
| `BLENDER_USER_CONFIG`, `BLENDER_USER_SCRIPTS`, `BLENDER_USER_DATAFILES` | Separate configuration, script and data resource directories |
| `BLENDER_SYSTEM_SCRIPTS`, `BLENDER_SYSTEM_DATAFILES`, `BLENDER_SYSTEM_PYTHON` | Can change system resource discovery; don't set them casually against the fixed application |
| `OCIO`, `BLENDER_OCIO` | Color-configuration environment controls; record effective configuration if set, because it affects interpretation and display of colors |
| `SSL_CERT_FILE` | Certificate store path; Blender supplies a bundled default when appropriate and unset. Relevant to imports performing network work, not required by these recipes |

The examples require `bpy`, `bmesh`, `mathutils` and Python's standard library, all supplied by Blender/the bundled Python. No dependency installation is required. Pure Python helpers can be shipped alongside a script. Native extension packages must match Python ABI, ARM64 architecture and linked libraries; a system package that imports successfully in another interpreter is not compatibility evidence. Do not change the application bundle or enable system Python just to make a helper import. The historical [PYTHONPATH report](../EXPERIENCE.md#r72807) illustrates the failure mechanism now addressed by isolated startup.

### Exit and completion

A Python traceback, operator `{'CANCELLED'}`, a nonzero process return code, native signal termination and missing output are distinct observations. `--python-exit-code` covers failure of the selected command-line Python execution, not every warning or caught exception. A script that catches an exception and exits normally can still return success. `sys.exit(n)` raises `SystemExit`; pinned Python glue deliberately preserves its exit behavior. Native crashes may bypass Python cleanup entirely. A host timeout bounds wall time; Cycles' render time limit does not bound startup, scene evaluation or all output work.

Use a host subprocess with an argument **list**, explicit `cwd`, separate logs and a fresh output directory. Do not build shell strings from user prompts or rely on the printed words “Blender quit.” [Unexecuted host example](../examples/host_job.py), [recovery module](09-revision.md).

## Implementation traces

- `creator.cc:481 - 671`: initialization passes, final actions, background exit versus `WM_main`.
- `creator_args.cc:2690 - 2897`: script dispatch, script failure code and environment switches.
- `bpy_interface.cc:368 - 597`: `PyConfig_InitIsolatedConfig`, bundled executable/home, environment and certificate handling.
- `bpy_interface_run.cc:70 - 252` → `py_capi_utils.cc:1256 - 1271`: `__main__`, `__file__`, error handling and cleanup. `py_capi_utils.cc:979 - 1038` handles `SystemExit`.
- `wm_init_exit.cc:718 - 727`: background exit suppresses ordinary user-exit actions and exits with the supplied code.

[Exact pinned links and inspected ranges](../SOURCE_TRACES.md). These traces establish control flow, not universal crash freedom or deterministic timing.

## Failure modes and diagnosis

| Symptom | First diagnosis |
|---|---|
| `ModuleNotFoundError: No module named 'bpy'` | Wrong executable/interpreter, or standalone Python route accidentally used |
| Wrong helper version imported | Inspect `sys.path`, actual module `__file__`, environment switches and local shadowing |
| Scene settings revert | File load or reset happened after assignment |
| Script error but host accepts job | Missing/late `--python-exit-code`, caught exception, or status-only validation |
| Process never exits | Work still active, thread/handler/native shutdown problem; preserve logs and use host timeout. Historical audio workaround is not a pinned-build diagnosis |
| Missing timer/modal work | No suitable event-loop lifecycle; make job synchronous |
| Relative resources fail after reopen | Confused CWD, script directory and `.blend`-relative root |

## Evidence and open questions

D/S establish ordinary background startup and error dispatch. R reports include historical environment and shutdown failures, with contradictory reproductions preserved. I recommends one process per job, explicit paths and application-level completion checks. Later [T01, T02 and T08](../FUTURE_TESTS.md) must verify concrete exit codes, failure artifacts and render output on the installed build. No such execution occurred during this review.
