# HISTORICAL SOURCE: use the release example for a fresh runnable demonstration.
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Julian Turner
"""Validate this delivered movie, its editable scene and its source references."""
from pathlib import Path
from array import array
import ast
import datetime
import hashlib
import json
import re
import subprocess
import wave
import motion


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    root=Path(__file__).resolve().parent.parent
    movie=root/'lamp-intro.mp4'
    production=root/'runs/production-01'
    frames=production/'frames'
    render=json.loads((frames/'render-receipt.json').read_text())
    build=json.loads((production/'build-receipt.json').read_text())
    reopened=json.loads((frames/'reopen-checks.json').read_text())
    assert [item['frame'] for item in render['frames']]==list(range(1,motion.FRAMES+1))
    assert len(list(frames.glob('frame_*.png')))==motion.FRAMES
    for item in render['frames']:
        assert sha(frames/f"frame_{item['frame']:04}.png")==item['sha256']
    assert sha(root/'lamp-intro.blend')==render['scene_sha256']==build['scene_sha256']
    assert sha(root/'poster.png')==sha(frames/'frame_0342.png')
    for name,digest in build['source_sha256'].items():
        assert sha(root/'source'/name)==digest
    assert sha(root/'source/lamp_geometry.py')==sha(root.parent/'adjustable-desk-lamp/build_lamp.py')
    assert reopened['invalid_drivers']==[] and reopened['external_files']==[]
    assert reopened['min_stretch']<.7 and reopened['max_stretch']>1.2
    assert reopened['max_volume_scale_error']<1e-5
    assert len(reopened['rebound_frames'])>30
    assert reopened['min_character_camera_margin']>0
    for name,digest in json.loads((root/'previous-version-hashes.json').read_text()).items():
        assert sha(root.parent/name)==digest
    source_hashes={}
    for path in sorted((root/'source').glob('*.py')):
        ast.parse(path.read_text(),filename=str(path))
        source_hashes[path.name]=sha(path)

    probe_command=['/opt/homebrew/bin/ffprobe','-v','error','-count_frames',
                   '-show_streams','-show_format','-of','json',str(movie)]
    result=subprocess.run(probe_command,capture_output=True,text=True,check=True)
    probe=json.loads(result.stdout)
    (root/'media-probe.json').write_text(json.dumps(probe,indent=2))
    video=next(s for s in probe['streams'] if s['codec_type']=='video')
    audio=next(s for s in probe['streams'] if s['codec_type']=='audio')
    assert (video['width'],video['height'])==(1280,720)
    assert video['avg_frame_rate']=='24/1' and int(video['nb_read_frames'])==384
    assert video['codec_name']=='h264' and video['pix_fmt']=='yuv420p'
    assert audio['codec_name']=='aac' and audio['channels']==2 and int(audio['sample_rate'])==48000
    assert abs(float(probe['format']['duration'])-16)<.05
    decode_command=['/opt/homebrew/bin/ffmpeg','-v','error','-xerror','-i',str(movie),'-f','null','-']
    decoded=subprocess.run(decode_command,capture_output=True,text=True)
    (root/'decode-check.log').write_text(decoded.stdout+decoded.stderr)
    assert decoded.returncode==0 and not decoded.stderr.strip()
    # Check the actual encoded first and last frames are black, rather than
    # assuming the chosen fade duration reached its endpoint before the cut.
    endpoints=[]
    for frame in (0,383):
        command=['/opt/homebrew/bin/ffmpeg','-v','error','-i',str(movie),
                 '-vf',f'select=eq(n\\,{frame}),scale=1:1,format=rgb24',
                 '-frames:v','1','-f','rawvideo','-']
        pixel=subprocess.run(command,capture_output=True,check=True).stdout
        assert len(pixel)==3 and max(pixel)<=2
        endpoints.append(list(pixel))
    with wave.open(str(root/'sound/foley.wav'),'rb') as stream:
        assert stream.getnchannels()==2 and stream.getsampwidth()==2 and stream.getframerate()==48000
        assert stream.getnframes()==16*48000
        pcm=array('h',stream.readframes(stream.getnframes()))
    peak=max(abs(v) for v in pcm)/32768
    assert .001<peak<.99
    cues=json.loads((root/'sound/sound-cues.json').read_text())
    assert [c['frame'] for c in cues['cues'] if c['label'] in ('rubber-foot landing','letter impact')]==motion.LANDINGS
    assert cues['wav_sha256']==sha(root/'sound/foley.wav')
    assert [c['frame'] for c in cues['cues'] if c['label']=='spring boing']==[f+1 for f in motion.LANDINGS]
    assert [c['frame'] for c in cues['cues'] if c['label']=='rebound landing']==[b for a,b,h in motion.REBOUNDS]
    local_links=[]
    for destination in re.findall(r'\]\(([^)]+)\)',(root/'README.md').read_text()):
        if '://' in destination or destination.startswith('#'):
            continue
        destination=destination.split('#')[0]
        if destination!='validation.json':
            assert (root/destination).exists(),destination
        local_links.append(destination)
    report={
        'status':'passed','checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'movie':{'sha256':sha(movie),'bytes':movie.stat().st_size,'duration_s':16.,
                 'frames':384,'width':1280,'height':720,'fps':24,
                 'video_codec':video['codec_name'],'audio_codec':audio['codec_name'],
                 'full_decode_exit_code':decoded.returncode,'fade_endpoint_rgb':endpoints},
        'audio':{'duration_s':16.,'sample_rate_hz':48000,'channels':2,'pcm_peak':peak,
                 'clipped_samples':sum(abs(v)>=32767 for v in pcm),'impact_frames':motion.LANDINGS},
        'scene_reopen_checks':reopened,'source_sha256':source_hashes,
        'source_syntax':'All delivered Python sources parsed without importing Blender.',
        'frame_integrity':'Every frame hash matched the completed renderer receipt.',
        'scene_integrity':'Delivered editable scene matches the built and independently reopened scene.',
        'local_readme_links':len(local_links),
        'visual_review':{'method':'Direct inspection of actual rendered stills; not a claim of continuous real-time playback review.',
                         'full_resolution_frames':[53,118,124,342],
                         'storyboard_frames':[47,53,189,194],
                         'observations':['Landing compression makes the body low and wide.',
                                         'Takeoff visibly extends the body and the joint chain.',
                                         'The first stamp compresses beyond its resting pose.',
                                         'The rebound clears the I while the body overshoots upward.']},
        'commands':{'probe':probe_command,'decode':decode_command}}
    (root/'validation.json').write_text(json.dumps(report,indent=2))
    print(json.dumps({'status':report['status'],'movie':report['movie'],
                      'source_files':len(source_hashes),'local_links':len(local_links)},indent=2))


if __name__=='__main__':
    main()
