# HISTORICAL SOURCE: use the release example for a fresh runnable demonstration.
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Julian Turner
"""UNEXECUTED host-side orchestration illustration. Does not import Blender.

Caller supplies a trusted future job entry script; this file is not that entry script.
No command is launched merely by importing this module.
"""
from pathlib import Path
import hashlib
import json
import subprocess

BLENDER = '/Applications/Blender.app/Contents/MacOS/Blender'


def run_job(script, new_root, timeout_seconds=300):
    """Launch one future job, preserve logs, verify transport-level output digests.

    Timeout is an illustrative host budget, not a measured Blender runtime.
    Baseline check must also be first in the supplied script, before scene mutation.
    """
    script = Path(script).resolve(strict=True)
    root = Path(new_root).resolve()
    root.mkdir(parents=False, exist_ok=False)  # Reject reused output roots.
    args = [BLENDER, '--background', '--factory-startup', '--disable-autoexec',
            '--python-exit-code', '17', '--python', str(script),
            '--', '--output-dir', str(root)]
    with (root / 'stdout.log').open('wb') as stdout, (root / 'stderr.log').open('wb') as stderr:
        try:
            result = subprocess.run(args, cwd=script.parent, stdout=stdout, stderr=stderr,
                                    timeout=timeout_seconds, check=False)
        except subprocess.TimeoutExpired:
            (root / 'failure.json').write_text(json.dumps({'kind': 'timeout'}))
            raise
    if result.returncode != 0:
        (root / 'failure.json').write_text(json.dumps({'kind': 'process', 'returncode': result.returncode}))
        raise RuntimeError(f'Blender exited with {result.returncode}; preserve {root}')
    receipt_path = root / 'complete.json'
    if not receipt_path.is_file():
        raise RuntimeError('Process returned zero without a completion receipt')
    receipt = json.loads(receipt_path.read_text())
    if receipt.get('status') != 'script-complete-unverified':
        raise RuntimeError('Unexpected receipt status')
    for key in ('blend', 'png', 'obj', 'mtl'):
        item = receipt['outputs'][key]
        p = (root / item['name']).resolve()
        if p.parent != root or not p.is_file():
            raise RuntimeError('Output path escaped root or is missing')
        if hashlib.sha256(p.read_bytes()).hexdigest() != item['sha256']:
            raise RuntimeError('Output digest mismatch')
    # These checks do not prove scene editability or visual/modeling correctness.
    return receipt
