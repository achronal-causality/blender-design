# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Julian Turner
#!/usr/bin/env python3
"""Discover Blender, build a divider, then inspect a relocated saved scene."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import struct
import subprocess
import sys

def discover(explicit=None):
    if explicit:
        path=Path(explicit).expanduser()
        if not path.is_file():raise ValueError(f'Blender executable not found: {path}')
        return str(path.resolve())
    configured=os.environ.get('BLENDER_BIN')
    if configured:return discover(configured)
    found=shutil.which('blender')
    if found:return found
    mac=Path('/Applications/Blender.app/Contents/MacOS/Blender')
    if sys.platform=='darwin' and mac.is_file():return str(mac)
    raise ValueError('Set BLENDER_BIN or pass --blender with the installed executable path')

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--blender');p.add_argument('--output',type=Path,required=True);p.add_argument('--width',type=float,default=1);p.add_argument('--angle',type=float,default=28);p.add_argument('--timeout',type=int,default=180);args=p.parse_args()
    executable=discover(args.blender);out=args.output.resolve();out.mkdir(parents=True,exist_ok=False);scripts=Path(__file__).resolve().parent
    def run(name,argv):
        with (out/(name+'.stdout.log')).open('wb') as stdout,(out/(name+'.stderr.log')).open('wb') as stderr:
            result=subprocess.run([executable,*argv],cwd=out,stdout=stdout,stderr=stderr,timeout=args.timeout,check=False)
        if result.returncode:raise RuntimeError(f'{name} failed with exit {result.returncode}; see logs in {out}')
    run('identity',['--version'])
    run('build',['--background','--factory-startup','--disable-autoexec','--python-exit-code','17','--python',str(scripts/'build_divider.py'),'--','--output-dir',str(out/'scene'),'--width',str(args.width),'--angle',str(args.angle)])
    png=(out/'scene/preview.png').read_bytes()
    if png[:8]!=b'\x89PNG\r\n\x1a\n' or struct.unpack('>II',png[16:24])!=(640,480):raise ValueError('Invalid preview header/dimensions')
    relocated=out/'relocated';relocated.mkdir();shutil.copy2(out/'scene/divider.blend',relocated/'divider.blend')
    run('reopen',['--background','--factory-startup','--disable-autoexec',str(relocated/'divider.blend'),'--python-exit-code','17','--python',str(scripts/'inspect_divider.py'),'--','--report',str(out/'reopen.json')])
    report=json.loads((out/'reopen.json').read_text());assert report['status']=='PASS'
    artifacts={str(f.relative_to(out)):hashlib.sha256(f.read_bytes()).hexdigest() for f in (out/'scene/divider.blend',out/'scene/preview.png',relocated/'divider.blend')}
    report={'status':'PASS','scope':'Fresh build, PNG header, relocated scene reopen and independent structural inspection; visual inspection is separate.','artifacts':artifacts,'parameters':{'width':args.width,'angle':args.angle},'source_hashes':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in scripts.glob('*.py')}}
    (out/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':
    try:main()
    except (OSError,ValueError,RuntimeError,subprocess.TimeoutExpired) as exc:print(str(exc),file=sys.stderr);sys.exit(1)
