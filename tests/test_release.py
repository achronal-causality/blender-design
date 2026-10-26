# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Julian Turner
"""Release boundary tests: reject changes, extras, missing files and invalid links."""
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('release',ROOT/'tools/release.py');release=importlib.util.module_from_spec(spec);spec.loader.exec_module(release)
class ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)/'copy'
        shutil.copytree(ROOT,self.root,ignore=shutil.ignore_patterns('.git','.private','build','.scratch','__pycache__'))
    def tearDown(self):self.tmp.cleanup()
    def test_clean(self):self.assertEqual(release.check(self.root)['status'],'PASS')
    def test_tamper(self):
        (self.root/'README.md').write_text('changed');self.assertEqual(release.check(self.root)['status'],'FAIL')
    def test_missing(self):
        (self.root/'NOTICE.md').unlink();self.assertEqual(release.check(self.root)['status'],'FAIL')
    def test_unexpected_cache(self):
        p=self.root/'skills/blender-design/scripts/__pycache__';p.mkdir();(p/'extra.pyc').write_bytes(b'cache')
        self.assertEqual(release.check(self.root)['status'],'FAIL')
    def test_unexpected_root_file(self):
        (self.root/'accidental.txt').write_text('extra');self.assertEqual(release.check(self.root)['status'],'FAIL')
    def test_unsafe_plan(self):
        p=self.root/'release-plan.json';p.write_text(json.dumps({'files':['../outside']}))
        with self.assertRaises(ValueError):release.plan(self.root)
    def test_link_target_and_anchor(self):
        (self.root/'probe.md').write_text('[bad](missing.md)\n[bad anchor](README.md#does-not-exist)')
        errors,count=release.links(self.root,{'probe.md'});self.assertEqual(len(errors),2)
    def test_personal_path(self):
        p=self.root/'README.md';p.write_text('/'+'Users'+'/private-person/secret')
        manifest=self.root/'release-files.json';m=json.loads(manifest.read_text())
        for e in m['files']:
            if e['path']=='README.md':e.update(bytes=p.stat().st_size,sha256=release.digest(p.read_bytes()))
        manifest.write_text(json.dumps(m));self.assertTrue(any('Personal absolute paths' in x for x in release.check(self.root)['errors']))
