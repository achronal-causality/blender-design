# HISTORICAL SOURCE: use the release example for a fresh runnable demonstration.
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Julian Turner
"""Assemble this project's numbered PNGs and synthesized Foley into an MP4."""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import motion


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--frames',type=Path,required=True)
    parser.add_argument('--sound',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--ffmpeg',default='/opt/homebrew/bin/ffmpeg')
    args=parser.parse_args()
    frames=args.frames.resolve()
    sound=args.sound.resolve()
    out=args.output.resolve()
    if out.exists():
        raise FileExistsError(out)
    receipt=json.loads((frames/'render-receipt.json').read_text())
    if receipt['frame_step']!=1 or len(receipt['frames'])!=motion.FRAMES:
        raise RuntimeError('Expected the completed full frame sequence')
    for item in receipt['frames']:
        path=frames/f"frame_{item['frame']:04}.png"
        if hashlib.sha256(path.read_bytes()).hexdigest()!=item['sha256']:
            raise RuntimeError('Changed or missing frame: '+str(path))
    duration=motion.FRAMES/motion.FPS
    command=[args.ffmpeg,'-hide_banner','-n','-framerate',str(motion.FPS),
             '-start_number','1','-i',str(frames/'frame_%04d.png'),'-i',str(sound),
             '-map','0:v:0','-map','1:a:0',
             '-vf','fade=t=in:st=0:d=0.25,fade=t=out:st=15.25:d=0.5',
             '-af','afade=t=out:st=15.25:d=0.5',
             '-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p',
             '-c:a','aac','-b:a','192k','-t',str(duration),'-movflags','+faststart',
             '-metadata','title=AXIS: springy cartoon lamp intro',
             '-metadata','comment=Cartoon squash and stretch, rebound hops, delayed shade wobble, synthesized spring Foley.',
             str(out)]
    result=subprocess.run(command,capture_output=True,text=True)
    out.with_suffix('.encode.log').write_text(result.stdout+result.stderr)
    if result.returncode:
        raise RuntimeError('Film encoding failed; see '+str(out.with_suffix('.encode.log')))
    out.with_suffix('.encode.json').write_text(json.dumps({
        'command':command,'returncode':result.returncode,
        'movie_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),
        'sound_sha256':hashlib.sha256(sound.read_bytes()).hexdigest(),
        'scene_sha256':receipt['scene_sha256'],
        'frame_count':len(receipt['frames']),'duration_s':duration},indent=2))
    print(out)


if __name__=='__main__':
    main()
