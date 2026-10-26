# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Julian Turner
#!/usr/bin/env python3
"""Check the exact installed release, including unexpected files."""
from pathlib import Path
import runpy
import sys
root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(root/'tools'))
if __name__ == '__main__':
    sys.argv = [str(root/'tools/release.py'), 'check']
    runpy.run_path(str(root/'tools/release.py'), run_name='__main__')
