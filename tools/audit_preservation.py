# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Julian Turner
"""Verify original recovery and retained findings against the private snapshot."""
import argparse
import hashlib
import json
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]
def sha(data):return hashlib.sha256(data).hexdigest()
def normalize(body):
    # Only presentation/link targets and personal paths may differ in retained findings.
    body=re.sub(r'(!?\[[^\]]*\]\()([^\s)]+)(\))',r'\1TARGET\3',body)
    body=body.replace('/'+'Users'+'/julianturner','/historical/author-home').replace('/private/tmp','/historical/tmp')
    body=re.sub(r'/(?:Users)/[^/\s"\x27<>]+','/historical/user-home',body)
    return body.replace('—',' - ').replace('–',' - ')
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--snapshot',type=Path,required=True);args=p.parse_args();snapshot=args.snapshot.resolve()
    inv=json.loads((ROOT/'docs/preservation.json').read_text())['files'];errors=[];findings=[]
    actual={p.relative_to(snapshot).as_posix() for p in snapshot.rglob('*') if p.is_file()}
    if actual!={e['original_path'] for e in inv}:errors.append('Original file set differs')
    for e in inv:
        path=e['original_path'];p=snapshot/path
        if not p.is_file() or sha(p.read_bytes())!=e['sha256']:errors.append(f'Original missing/changed: {path}');continue
        if 'public_path' in e:
            public=ROOT/e['public_path']
            if not public.is_file() or sha(public.read_bytes())!=e['public_sha256']:errors.append(f'Public mapping changed: {path}')
            if '/references/library/' in path and path.endswith('.md') and not path.endswith('README.md'):
                if normalize(p.read_text())!=normalize(public.read_text()):errors.append(f'Finding text differs beyond allowed transformations: {path}')
                findings.append(path)
    print(json.dumps({'status':'FAIL' if errors else 'PASS','original_files':len(inv),'retained_finding_documents':len(findings),'finding_documents':findings,'errors':errors,'scope':'Every original byte and mapped public hash, plus full normalized text equality for retained non-README research Markdown; no claim of legal clearance.'},indent=2))
    return bool(errors)
if __name__=='__main__':raise SystemExit(main())
