# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Julian Turner
#!/usr/bin/env python3
"""Build and verify explicit-file-list releases. Standard library only."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
IGNORED = {'.git', '.private', 'build', '.scratch'}
MANIFEST = 'release-files.json'

def digest(data): return hashlib.sha256(data).hexdigest()
def dump(path, value): path.write_text(json.dumps(value, indent=2, ensure_ascii=True) + '\n')
def safe(name):
    p = PurePosixPath(name)
    if not name or p.is_absolute() or any(x in ('', '.', '..') for x in name.split('/')) or '\\' in name or ':' in name:
        raise ValueError(f'Unsafe release path: {name}')
    return name

def files(root):
    result = set()
    for p in root.rglob('*'):
        rel = p.relative_to(root)
        if rel.parts[0] in IGNORED: continue
        if p.is_symlink(): raise ValueError(f'Symlink in source: {rel}')
        if p.is_file(): result.add(rel.as_posix())
    return result

def plan(root):
    names = json.loads((root/'release-plan.json').read_text())['files']
    if len(names) != len(set(names)): raise ValueError('Duplicate planned file')
    for name in names:
        safe(name)
        if any(x in {'.private', '__pycache__', '.git', '.DS_Store'} for x in PurePosixPath(name).parts) or name.endswith(('.pyc','.pyo')):
            raise ValueError(f'Forbidden release member: {name}')
    return set(names)

def links(root, names):
    errors=[]; count=0
    pattern=re.compile(r'!?\[[^\]]*\]\(([^\s)]+)\)')
    from urllib.parse import unquote, urlsplit
    for name in sorted(names):
        if not name.endswith('.md'): continue
        for match in pattern.finditer((root/name).read_text()):
            target=match[1]
            if urlsplit(target).scheme or target.startswith('//'): continue
            path, _, anchor = target.partition('#')
            dest=(root/name).parent / unquote(path) if path else root/name
            dest=dest.resolve()
            if not dest.is_relative_to(root.resolve()) or not dest.is_file():
                errors.append(f'{name}: broken local link {target}');continue
            if anchor and dest.suffix=='.md':
                body=dest.read_text()
                headings=[]
                for heading in re.findall(r'^#+\s+(.+)$',body,re.M):
                    text=re.sub(r'<[^>]+>','',heading).lower()
                    text=re.sub(r'[^\w\- ]','',text).replace(' ','-')
                    headings.append(text)
                if anchor not in headings and not re.search(r'(?:id|name)=[\"\x27]'+re.escape(anchor)+r'[\"\x27]',body):
                    errors.append(f'{name}: missing anchor {target}')
            count+=1
    return errors,count

def check(root=ROOT):
    expected=plan(root); actual=files(root)
    errors=[]
    if actual != expected: errors += [f'Missing: {sorted(expected-actual)}', f'Unexpected: {sorted(actual-expected)}']
    manifest=json.loads((root/MANIFEST).read_text())
    records=manifest['files']; names=[e['path'] for e in records]
    if len(names)!=len(set(names)) or set(names) != expected-{MANIFEST}: errors.append('Manifest and release plan disagree')
    for entry in records:
        safe(entry['path']);p=root/entry['path']
        if not p.is_file():continue
        data=p.read_bytes()
        if len(data)!=entry['bytes'] or digest(data)!=entry['sha256']: errors.append(f'Changed: {entry["path"]}')
    if not errors:
        more,count=links(root,expected);errors+=more
    else: count=0
    # Scan only project-owned source/reference text, not license legal text.
    personal=[]
    for name in sorted(actual):
        if name.endswith(('.md','.py','.json','.toml','.yaml')):
            if re.search(r'/(?:Users|home)/[^/\s]+|[A-Z]:\\Users\\', (root/name).read_text()):personal.append(name)
    if personal:errors.append(f'Personal absolute paths: {personal}')
    report={'status':'FAIL' if errors else 'PASS','files':len(actual),'bytes':sum((root/n).stat().st_size for n in actual),'local_links':count,'errors':errors,'scope':'Exact release inventory, hashes, local links/anchors, and personal-path patterns; not a comprehensive secret scan or Blender test.'}
    return report

def seal():
    expected=plan(ROOT)
    if files(ROOT)-{MANIFEST} != expected-{MANIFEST}: raise ValueError('Source differs from explicit release plan')
    dump(ROOT/MANIFEST,{'format':1,'files':[{'path':n,'bytes':len((ROOT/n).read_bytes()),'sha256':digest((ROOT/n).read_bytes())} for n in sorted(expected-{MANIFEST})]})
    report=check();print(json.dumps(report,indent=2))
    if report['errors']:raise ValueError('Release failed validation')

def bundle(output):
    report=check()
    if report['errors']:raise ValueError(report)
    output=output.resolve();output.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(output,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name in sorted(plan(ROOT)):
            info=zipfile.ZipInfo('blender-design/'+name, date_time=(2026,10,26,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16
            z.writestr(info,(ROOT/name).read_bytes())
    print(json.dumps({'artifact':str(output),'bytes':output.stat().st_size,'sha256':digest(output.read_bytes())},indent=2))

def archive(snapshot, output):
    inventory=json.loads((ROOT/'docs/preservation.json').read_text())['files']
    expected={e['original_path'] for e in inventory}
    actual={p.relative_to(snapshot).as_posix() for p in snapshot.rglob('*') if p.is_file()}
    if expected!=actual:raise ValueError('Original snapshot inventory mismatch')
    # Verify every source before opening the archive output.
    for e in inventory:
        data=(snapshot/e['original_path']).read_bytes()
        if digest(data)!=e['sha256'] or len(data)!=e['bytes']:raise ValueError(f'Original changed: {e["original_path"]}')
    output.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(output,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for e in inventory:z.write(snapshot/e['original_path'],e['archive_member'])
    with zipfile.ZipFile(output) as z:
        if set(z.namelist())!={e['archive_member'] for e in inventory}:raise ValueError('Archive members mismatch')
        for e in inventory:
            if digest(z.read(e['archive_member']))!=e['sha256']:raise ValueError('Archive bytes mismatch')
    print(json.dumps({'status':'PASS','scope':'Private preservation archive; NOT cleared for public distribution','files':len(inventory),'bytes':output.stat().st_size,'sha256':digest(output.read_bytes())},indent=2))

def main():
    parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='command',required=True)
    sub.add_parser('seal');sub.add_parser('check')
    b=sub.add_parser('build');b.add_argument('--output',type=Path,required=True)
    a=sub.add_parser('archive');a.add_argument('--snapshot',type=Path,required=True);a.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    if args.command=='seal':seal()
    elif args.command=='check':
        report=check();print(json.dumps(report,indent=2));return bool(report['errors'])
    elif args.command=='build':bundle(args.output)
    else:archive(args.snapshot.resolve(),args.output.resolve())
    return 0
if __name__=='__main__':
    try:sys.exit(main())
    except (OSError,ValueError,KeyError) as exc:print(str(exc),file=sys.stderr);sys.exit(1)
