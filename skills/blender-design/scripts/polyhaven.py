# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Julian Turner
#!/usr/bin/env python3
"""Small, standard-library Poly Haven catalog and dependency downloader."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlsplit, unquote
from urllib.request import Request, build_opener, HTTPRedirectHandler

API = 'https://api.polyhaven.com'
USER_AGENT = 'BlenderDesignSkill/1.2 (procedural-design workflow)'
CREDIT = 'Assets from Poly Haven — https://polyhaven.com'
EVIDENCE = Path(__file__).resolve().parents[1] / 'references/polyhaven-evidence'


def checked_url(url):
    u = urlsplit(url)
    host = u.hostname or ''
    if (u.scheme != 'https' or u.username or u.password or u.port not in (None, 443)
            or not any(host == d or host.endswith('.' + d) for d in ('polyhaven.com', 'polyhaven.org'))):
        raise ValueError(f'Unrecognized Poly Haven HTTPS URL: {url}')
    return url


class Redirects(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        checked_url(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def response(url):
    req = Request(checked_url(url), headers={'User-Agent': USER_AGENT})
    return build_opener(Redirects()).open(req, timeout=30)


def get_json(path):
    with response(API + path) as r:
        data = r.read(16 * 1024 * 1024 + 1)
    if len(data) > 16 * 1024 * 1024:
        raise ValueError('Metadata response exceeds 16 MiB')
    return json.loads(data)


def safe_relative(name):
    if not isinstance(name, str) or not name or '\\' in name or '\x00' in name:
        raise ValueError(f'Unsafe dependency path: {name!r}')
    parts = name.split('/')
    if any(p in ('', '.', '..') or ':' in p for p in parts):
        raise ValueError(f'Unsafe dependency path: {name!r}')
    return PurePosixPath(name).as_posix()


def variants(tree, prefix=()):
    if isinstance(tree, dict) and 'url' in tree:
        yield '/'.join(prefix), tree
    elif isinstance(tree, dict):
        for key, child in tree.items():
            yield from variants(child, prefix + (key,))


def plan_files(tree, variant):
    available = dict(variants(tree))
    if variant not in available:
        raise ValueError(f'Unknown variant {variant!r}; use inspect to list exact choices')
    chosen = available[variant]
    main = safe_relative(unquote(urlsplit(chosen['url']).path.rsplit('/', 1)[-1]))
    planned = {}

    def add(name, item):
        name = safe_relative(name)
        if name.split('/')[0] in ('provenance.json', 'info.json', 'files.json', 'source-evidence'):
            raise ValueError(f'Reserved provenance path: {name}')
        checked_url(item['url'])
        size = item.get('size')
        digest = item.get('md5', '')
        if type(size) is not int or size <= 0 or not re.fullmatch(r'[0-9a-fA-F]{32}', digest):
            raise ValueError(f'Missing/invalid byte size or MD5 for {name}')
        row = {'path': name, 'url': item['url'], 'bytes': size, 'md5': digest.lower()}
        if name in planned:
            if planned[name] != row: raise ValueError(f'Conflicting dependency path: {name}')
            return
        planned[name] = row
        if len(planned) > 256: raise ValueError('More than 256 dependency files; inspect manually')
        parent = PurePosixPath(name).parent
        for relative, child in item.get('include', {}).items():
            safe_relative(relative)
            add((parent / relative).as_posix(), child)

    add(main, chosen)
    return main, list(planned.values())


def fetch_file(item, root):
    target = root / item['path']
    target.parent.mkdir(parents=True, exist_ok=True)
    part = target.with_name(target.name + '.part')
    md5 = hashlib.md5(); sha = hashlib.sha256(); count = 0
    with response(item['url']) as r, part.open('xb') as stream:
        while True:
            chunk = r.read(min(1024 * 1024, item['bytes'] - count + 1))
            if not chunk: break
            count += len(chunk)
            if count > item['bytes']: raise ValueError(f'Download exceeds declared size: {item["path"]}')
            stream.write(chunk); md5.update(chunk); sha.update(chunk)
    if count != item['bytes'] or md5.hexdigest() != item['md5']:
        raise ValueError(f'Byte size or MD5 mismatch: {item["path"]}')
    if target.exists(): raise FileExistsError(target)
    part.rename(target)
    return dict(item, sha256=sha.hexdigest())


def download(asset, variant, output, max_bytes):
    info = get_json('/info/' + asset)
    files = get_json('/files/' + asset)
    main, plan = plan_files(files, variant)
    total = sum(x['bytes'] for x in plan)
    if total > max_bytes: raise ValueError(f'Variant needs {total} bytes; budget is {max_bytes}')
    output = output.expanduser().resolve()
    output.mkdir(parents=True, exist_ok=False)
    record = {'provider': 'Poly Haven', 'credit': CREDIT, 'asset_id': asset,
              'asset_page': f'https://polyhaven.com/a/{asset}', 'authors': info.get('authors'),
              'license': 'CC0-1.0', 'license_url': 'https://polyhaven.com/license',
              'api_terms_url': 'https://github.com/Poly-Haven/Public-API/blob/master/ToS.md',
              'retrieved_utc': datetime.now(timezone.utc).isoformat(), 'variant': variant,
              'main_file': main, 'declared_bytes': total, 'status': 'incomplete', 'files': []}
    def save():
        (output / 'provenance.json').write_text(json.dumps(record, indent=2) + '\n')
    (output / 'info.json').write_text(json.dumps(info, indent=2) + '\n')
    (output / 'files.json').write_text(json.dumps(files, indent=2) + '\n')
    evidence_dir = output / 'source-evidence'
    evidence_dir.mkdir()
    record['license_evidence'] = []
    for entry in json.loads((EVIDENCE / 'manifest.json').read_text()):
        if entry['id'] not in ('poly-license', 'poly-tos-pinned'): continue
        data = (EVIDENCE / entry['path']).read_bytes()
        if hashlib.sha256(data).hexdigest() != entry['sha256']:
            raise ValueError('Bundled policy record changed')
        (evidence_dir / entry['path']).write_bytes(data)
        record['license_evidence'].append(dict(entry, path='source-evidence/' + entry['path']))
    save()
    try:
        for item in plan:
            record['files'].append(fetch_file(item, output)); save()
        record['status'] = 'downloaded_and_hash_verified'
        save()
    except Exception as exc:
        record['error'] = str(exc); save()
        raise
    return record


def verify(root):
    root = root.expanduser().resolve()
    record = json.loads((root / 'provenance.json').read_text())
    if record.get('status') != 'downloaded_and_hash_verified':
        raise ValueError('Acquisition is incomplete')
    if not record.get('files'): raise ValueError('Empty acquisition')
    seen = set()
    for item in record['files']:
        name = safe_relative(item['path'])
        p = root / name
        if name in seen or not p.resolve().is_relative_to(root) or p.is_symlink():
            raise ValueError('Duplicate or escaping file path')
        seen.add(name)
        sha = hashlib.sha256(); md5 = hashlib.md5(); size = 0
        with p.open('rb') as f:
            while chunk := f.read(1024 * 1024):
                sha.update(chunk); md5.update(chunk); size += len(chunk)
        if (size != item['bytes'] or sha.hexdigest() != item['sha256'] or md5.hexdigest() != item['md5']):
            raise ValueError(f'Changed acquisition: {name}')
    if safe_relative(record['main_file']) not in seen: raise ValueError('Main file absent from manifest')
    for entry in record.get('license_evidence', []):
        p = root / safe_relative(entry['path'])
        if not p.resolve().is_relative_to(root) or hashlib.sha256(p.read_bytes()).hexdigest() != entry['sha256']:
            raise ValueError('Changed license evidence')
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='action', required=True)
    p = sub.add_parser('search'); p.add_argument('query'); p.add_argument('--type', choices=['models','textures','hdris','all'], default='models'); p.add_argument('--limit', type=int, default=8)
    p = sub.add_parser('inspect'); p.add_argument('asset')
    p = sub.add_parser('download'); p.add_argument('asset'); p.add_argument('--variant', required=True); p.add_argument('--output', type=Path, required=True); p.add_argument('--max-mib', type=int, default=128)
    p = sub.add_parser('verify'); p.add_argument('directory', type=Path)
    args = parser.parse_args()
    if hasattr(args, 'asset') and not re.fullmatch(r'[a-z0-9_\-]+', args.asset):
        parser.error('Asset must be a Poly Haven slug')
    print(CREDIT, file=sys.stderr)
    if args.action == 'search':
        query = args.query.strip().lower()
        if not 1 <= len(query) <= 100 or not 1 <= args.limit <= 100:
            parser.error('Query length and result limit must be 1..100')
        result = get_json('/search?' + urlencode({'q':query,'t':args.type,'limit':args.limit}))
    elif args.action == 'inspect':
        info = get_json('/info/' + args.asset); tree = get_json('/files/' + args.asset)
        choices = []
        for key, _ in variants(tree):
            main_file, plan = plan_files(tree, key)
            choices.append({'variant':key,'main_file':main_file,'files':len(plan),'total_bytes':sum(x['bytes'] for x in plan)})
        result = {'info':info,'variants':choices}
    elif args.action == 'download':
        if args.max_mib <= 0: parser.error('--max-mib must be positive')
        result = download(args.asset, args.variant, args.output, args.max_mib * 1024 * 1024)
    else:
        result = verify(args.directory)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    try:
        main()
    except HTTPError as exc:
        print(f'Poly Haven HTTP {exc.code}; Retry-After={exc.headers.get("Retry-After", "not supplied")}. No automatic retry.', file=sys.stderr)
        sys.exit(1)
    except (ValueError, OSError, URLError, KeyError, TypeError) as exc:
        print(f'Poly Haven request failed: {exc}', file=sys.stderr)
        sys.exit(1)
