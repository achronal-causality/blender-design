# HISTORICAL SOURCE: use the release example for a fresh runnable demonstration.
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Julian Turner
"""Cartoon spring performance: preload, release, impact, recoil and follow-through.

Metres, degrees and 24-fps frames. The articulated model is rigid in character
space; a separate volume-preserving scale deliberately squashes/stretches it.
Rebound arcs and damped impact responses represent stored/released spring energy.
This is authored animation, not a physical simulation of a real lamp.
"""
import math

FPS=24
FRAMES=384
SCALE=1.2
I_X=-.92
I_Y=.12
LETTER_HEIGHT=.82
ENTRY=[(28,45,3.45,2.10,.30),(51,68,2.10,1.10,.36),
       (74,91,1.10,.05,.40),(97,116,.05,I_X,.34)]
STAMPS=[(160,186,0.,1.,.78),(208,229,.58,.58,.60),(252,274,.22,.22,.68)]
LANDINGS=[x[1] for x in ENTRY]+[x[1] for x in STAMPS]
# These small hops are a visible loss of energy after the main impacts.
REBOUNDS=[(120,128,.12),(131,136,.038),(190,198,.15),(200,205,.045),
          (233,241,.15),(244,249,.045),(278,286,.18),(289,295,.055)]


def smooth(t):
    t=max(0.,min(1.,t))
    return t*t*(3.-2.*t)


def mix(a,b,t):
    return a+(b-a)*t


def tween(frame,keys):
    if frame<=keys[0][0]:
        return keys[0][1]
    for (a,x),(b,y) in zip(keys,keys[1:]):
        if frame<=b:
            return mix(x,y,smooth((frame-a)/(b-a)))
    return keys[-1][1]


def spring(age,period=12.,decay=11.):
    """Damped displacement after an impulse; starts at zero, then compresses."""
    return -math.exp(-age/decay)*math.sin(2*math.pi*age/period) if age>=0 else 0.


def letter_scale(frame):
    # Each impact compresses past equilibrium, then the letter springs back.
    return tween(frame,[(1,1.),(186,1.),(190,.47),(194,.64),(199,.58),
                        (229,.58),(233,.125),(237,.265),(243,.22),
                        (274,.22),(278,.006),(282,.031),(290,.009),(FRAMES,.009)])


def flight_pose(u):
    # A deep preload releases in approximately two frames. The long middle
    # silhouette stays open; impact compression occurs AFTER touching down.
    shoulder=tween(u,[(0,134),(.11,94),(.40,107),(.68,111),(.87,104),(1,118)])
    bend=tween(u,[(0,148),(.11,28),(.40,48),(.68,61),(.87,38),(1,82)])
    stretch=tween(u,[(0,.76),(.105,1.30),(.32,1.05),(.62,1.),(.86,1.14),(1,1.)])
    return shoulder,bend,stretch


def state(frame):
    x,y,z=ENTRY[0][2],-.55,0.
    shoulder,bend,stretch=118.,82.,1.
    phase='hold'
    support=LETTER_HEIGHT*letter_scale(frame) if frame>=186 else 0.
    latest=max((end for end in LANDINGS if end<=frame),default=None)
    if latest is not None:
        # Secondary motion is underdamped, not a one-way ease back to neutral.
        wave=spring(frame-latest)
        shoulder-=22*wave
        bend-=99*wave
        stretch+=.50*wave
        phase='spring-recovery'
    for index,(start,end,xa,xb,h) in enumerate(ENTRY):
        if frame>end:
            x=xb
        elif frame>=start:
            u=(frame-start)/(end-start)
            x=mix(xa,xb,u)
            z=4*h*u*(1-u)
            shoulder,bend,stretch=flight_pose(u)
            phase='entry-flight'
            break
        elif frame>=start-6:
            u=(frame-start+6)/6
            if index:
                shoulder=tween(u,[(0,118),(.33,136),(.67,108),(1,134)])
                bend=tween(u,[(0,82),(.33,156),(.67,48),(1,148)])
                stretch=tween(u,[(0,1.),(.33,.64),(.67,1.18),(1,.76)])
            else:
                shoulder=tween(u,[(0,118),(.72,134),(1,134)])
                bend=tween(u,[(0,82),(.72,148),(1,148)])
                stretch=tween(u,[(0,1.),(.72,.70),(1,.76)])
            phase='preload'
            break
    if frame>=116:
        x=I_X
    if frame>=186:
        y=I_Y
        z=support
    for start,end,ha,hb,apex in STAMPS:
        if start-5<=frame<start:
            # Enter preload continuously from the damped recovery, including
            # the preceding small rebound, rather than resetting the pose.
            age=start-5-max(e for e in LANDINGS if e<start)
            wave=spring(age)
            u=(frame-start+5)/5
            shoulder=tween(u,[(0,118-22*wave),(.75,136),(1,134)])
            bend=tween(u,[(0,82-99*wave),(.75,158),(1,148)])
            stretch=tween(u,[(0,1+.50*wave),(.75,.63),(1,.76)])
            phase='stamp-preload'
        elif start<=frame<=end:
            u=(frame-start)/(end-start)
            y=mix(-.55,I_Y,smooth(u)) if start==160 else I_Y
            z=LETTER_HEIGHT*mix(ha,hb,u)+4*apex*u*(1-u)
            shoulder,bend,stretch=flight_pose(u)
            phase='stamp-flight'
    rebound_lift=0.
    if phase not in ('entry-flight','stamp-flight'):
        for a,b,height in REBOUNDS:
            if a<=frame<=b:
                u=(frame-a)/(b-a)
                rebound_lift=4*height*u*(1-u)
                z=support+rebound_lift
                if phase!='stamp-preload':
                    phase='rebound'
    if frame>=300:
        shoulder=tween(frame,[(300,118-22*spring(26)),(314,124),(FRAMES,124)])
        bend=tween(frame,[(300,82-99*spring(26)),(314,54),(FRAMES,54)])
        stretch=tween(frame,[(300,1+.50*spring(26)),(314,1.),(FRAMES,1.)])
        phase='look-and-hold'
    yaw=tween(frame,[(1,180),(121,180),(153,0),(FRAMES,0)])
    look_camera=smooth((frame-314)/27)
    if frame<124:
        gaze=(x-.65,y-.06,.10)
    elif frame<155:
        gaze=(I_X,I_Y,LETTER_HEIGHT*.82)
    else:
        gaze=(I_X,I_Y,.03)
    # A second, slower oscillator gives the shade delayed follow-through.
    head_wobble=sum(29*spring(frame-end-1.5,period=13.5,decay=13.)
                    for end in LANDINGS if 0<=frame-end<55)
    head_wobble*=1-smooth((frame-307)/20)
    lateral=1/math.sqrt(stretch)
    return dict(frame=frame,position=(x,y,z),shoulder=shoulder,bend=bend,
                yaw=yaw,pitch=0.,gaze=gaze,look_camera=look_camera,
                stretch=stretch,character_scale=(SCALE*lateral,SCALE*lateral,SCALE*stretch),
                head_wobble_deg=head_wobble,support_height=support,rebound_lift=rebound_lift,
                lamp_power=tween(frame,[(1,1.5),(332,1.5),(342,5.),(FRAMES,5.)]),
                letter_scale=letter_scale(frame),phase=phase)
