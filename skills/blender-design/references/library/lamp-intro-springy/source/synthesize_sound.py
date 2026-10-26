# HISTORICAL SOURCE: use the release example for a fresh runnable demonstration.
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Julian Turner
"""Original mechanical Foley from damped resonators, friction and clicks.

Requires only Blender's bundled NumPy and Python standard library. No samples,
speech synthesis, models, network calls, or recorded music. These are deliberately
stylized acoustic analogues, not a measured physical simulation of the lamp.
"""
from pathlib import Path
import argparse
import hashlib
import json
import math
import wave
import numpy as np
import motion

RATE=48000


def resonator(duration, frequencies, decay):
    t=np.arange(round(duration*RATE))/RATE
    tone=np.zeros_like(t)
    for frequency,gain in frequencies:
        tone+=gain*np.sin(2*math.pi*frequency*t)*np.exp(-t/decay)
    # Short finite attack prevents discontinuity at a cue boundary.
    tone*=1-np.exp(-t/.001)
    tone*=np.minimum(1,(duration-t)/.02)
    return tone


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    out=args.output.resolve()
    out.mkdir(parents=True,exist_ok=False)
    rng=np.random.default_rng(20260915)
    track=np.zeros((round(motion.FRAMES/motion.FPS*RATE),2),dtype=np.float64)
    cues=[]

    def place(sound,frame,gain,x,label):
        start=round((frame-1)/motion.FPS*RATE)
        if start<0:
            raise ValueError('Negative cue time')
        n=min(len(sound),len(track)-start)
        # Equal-power stereo pan linked to the character's stage coordinate.
        pan=max(-.75,min(.75,x/3))
        angle=(pan+1)*math.pi/4
        track[start:start+n,0]+=sound[:n]*gain*math.cos(angle)
        track[start:start+n,1]+=sound[:n]*gain*math.sin(angle)
        # One quiet delayed reflection, as on the visible open studio stage.
        delay=round(.043*RATE)
        m=min(n,len(track)-start-delay)
        if m>0:
            track[start+delay:start+delay+m]+=sound[:m,None]*gain*.08
        cues.append({'label':label,'frame':frame,'time_s':(frame-1)/motion.FPS,
                     'duration_s':n/RATE,'stage_x_m':x,'gain':gain})

    for i,frame in enumerate(motion.LANDINGS):
        is_stamp=i>=len(motion.ENTRY)
        severity=(.75+i*.035) if not is_stamp else (1.1+(i-4)*.20)
        # A compliant foot gives a low thump; the metal mechanism rings briefly.
        thump=resonator(.42,[(78 if is_stamp else 106,1),(157,.30),(238,.09)],.065)
        metal=resonator(.42,[(691,.065),(1117,.035),(1743,.016)],.055)
        noise=rng.normal(0,1,len(thump))
        noise=np.convolve(noise,np.ones(9)/9,mode='same')
        t=np.arange(len(noise))/RATE
        noise*=np.exp(-t/.018)*(1-np.exp(-t/.0008))*.30
        place(thump+metal+noise,frame,.56*severity,motion.state(frame)['position'][0],
              'letter impact' if is_stamp else 'rubber-foot landing')
        # Settling steel produces a quieter second mechanical tick.
        place(resonator(.18,[(900,.20),(1430,.08)],.028),frame+2,.25,
              motion.state(frame)['position'][0],'joint settle')
        # An intentionally cartoonish pitch wobble makes spring recoil audible.
        t=np.arange(round(.78*RATE))/RATE
        frequency=175+85*np.exp(-t/0.32)*np.cos(2*math.pi*9*t)
        phase=2*math.pi*np.cumsum(frequency)/RATE
        envelope=(1-np.exp(-t/.004))*np.exp(-t/.24)*np.minimum(1,(.78-t)/.04)
        boing=(np.sin(phase)+.32*np.sin(2*phase)+.12*np.sin(3*phase))*envelope
        place(boing,frame+1,.17 if is_stamp else .13,motion.state(frame)['position'][0],'spring boing')

    for start,end,height in motion.REBOUNDS:
        place(resonator(.22,[(120,1.),(293,.18),(733,.04)],.037),end,
              .15 if height>.08 else .075,motion.state(end)['position'][0],'rebound landing')

    for start,end,*_ in motion.ENTRY+motion.STAMPS:
        duration=(end-start)/motion.FPS*.55
        t=np.arange(round(duration*RATE))/RATE
        u=t/duration
        # Friction chirp: changing joint speed changes its instantaneous pitch.
        frequency=470+360*np.sin(math.pi*u)+110*u
        phase=2*math.pi*np.cumsum(frequency)/RATE
        envelope=np.sin(math.pi*u)**1.6
        friction=(np.sin(phase)+.17*np.sin(2.03*phase))*envelope
        place(friction,start-2,.024,motion.state(start)['position'][0],'joint friction')
        place(resonator(.12,[(220,.25),(815,.18)],.019),start,.12,
              motion.state(start)['position'][0],'lift-off click')

    # A delicate swivel as the shade finds the audience, then an electrical click.
    t=np.arange(round(.65*RATE))/RATE
    spin=np.sin(2*math.pi*(430*t+105*t*t))*np.sin(math.pi*t/.65)**2
    place(spin,319,.018,motion.I_X,'head swivel')
    place(resonator(.095,[(1800,.18),(2600,.07)],.010),338,.25,motion.I_X,'lamp click')
    raw_peak=float(np.max(np.abs(track)))
    gain=min(1,.84/raw_peak)
    track*=gain
    samples=np.rint(track*32767).astype('<i2')
    path=out/'foley.wav'
    with wave.open(str(path),'wb') as stream:
        stream.setnchannels(2)
        stream.setsampwidth(2)
        stream.setframerate(RATE)
        stream.writeframes(samples.tobytes())
    report={'sample_rate_hz':RATE,'channels':2,'duration_s':len(track)/RATE,
            'peak_absolute':float(np.max(np.abs(track))),
            'rms':float(np.sqrt(np.mean(track**2))),'clipped_samples':int(np.sum(np.abs(track)>=1)),
            'global_gain':gain,'deterministic_seed':20260915,
            'wav_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'cues':cues}
    (out/'sound-cues.json').write_text(json.dumps(report,indent=2))
    print(json.dumps({k:v for k,v in report.items() if k!='cues'},indent=2))


if __name__=='__main__':
    main()
