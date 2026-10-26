# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Julian Turner
import hashlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'skills/blender-design/scripts'))
import polyhaven as ph

def file(name, payload=b'content'):
    return {'url':'https://dl.polyhaven.org/file/' + name, 'size':len(payload), 'md5':hashlib.md5(payload).hexdigest()}

class CatalogTests(unittest.TestCase):
    def test_dependency_layout(self):
        main = dict(file('model.blend'), include={'textures/color.png': file('color.png')})
        name, plan = ph.plan_files({'blend':{'1k':{'blend':main}}}, 'blend/1k/blend')
        self.assertEqual(name, 'model.blend')
        self.assertEqual([x['path'] for x in plan], ['model.blend','textures/color.png'])

    def test_unsafe_paths_and_hosts(self):
        for name in ['../escape', '/absolute', 'a/../b', 'a\\b', 'a//b', 'C:/file']:
            with self.subTest(name=name), self.assertRaises(ValueError): ph.safe_relative(name)
        for url in ['http://dl.polyhaven.org/a','https://polyhaven.org.evil.example/a','file:///tmp/a','https://user@polyhaven.com/a']:
            with self.subTest(url=url), self.assertRaises(ValueError): ph.checked_url(url)

    def test_reserved_and_conflicting_paths(self):
        with self.assertRaises(ValueError): ph.plan_files({'x':file('provenance.json')}, 'x')
        main = dict(file('model.blend'), include={'model.blend':file('other.blend')})
        with self.assertRaises(ValueError): ph.plan_files({'x':main}, 'x')

    def test_integrity_failure_keeps_partial(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _, plan = ph.plan_files({'x':file('model.blend')}, 'x')
            item = plan[0]
            with patch.object(ph,'response',return_value=io.BytesIO(b'changed')):
                with self.assertRaises(ValueError): ph.fetch_file(item,root)
            self.assertFalse((root/'model.blend').exists())
            self.assertTrue((root/'model.blend.part').exists())

    def test_budget_and_existing_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)/'new'
            with patch.object(ph,'get_json',side_effect=[{}, {'x':file('model.blend')}]), self.assertRaises(ValueError):
                ph.download('example','x',root,1)
            self.assertFalse(root.exists())
            root.mkdir()
            with patch.object(ph,'get_json',side_effect=[{}, {'x':file('model.blend')}]), self.assertRaises(FileExistsError):
                ph.download('example','x',root,100)

    def test_download_then_tampering(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)/'new'
            with patch.object(ph,'get_json',side_effect=[{'authors':{'Artist':'All'}},{'x':file('model.blend')}]), patch.object(ph,'response',return_value=io.BytesIO(b'content')):
                record=ph.download('example','x',root,100)
            self.assertEqual(ph.verify(root)['authors'], {'Artist':'All'})
            self.assertEqual(len(record['license_evidence']),2)
            self.assertTrue(all(e['evidence_kind']=='original_source_linked_summary' for e in record['license_evidence']))
            self.assertTrue(all(e['retrieved_utc'] is None for e in record['license_evidence']))
            (root/'model.blend').write_bytes(b'changed')
            with self.assertRaises(ValueError): ph.verify(root)

    def test_failed_attempt_not_accepted(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)/'new'
            with patch.object(ph,'get_json',side_effect=[{}, {'x':file('model.blend')}]), patch.object(ph,'response',return_value=io.BytesIO(b'bad')):
                with self.assertRaises(ValueError): ph.download('example','x',root,100)
            self.assertEqual(json.loads((root/'provenance.json').read_text())['status'],'incomplete')
            with self.assertRaises(ValueError): ph.verify(root)

if __name__ == '__main__': unittest.main()
