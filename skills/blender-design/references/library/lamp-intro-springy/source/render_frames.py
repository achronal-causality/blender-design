# HISTORICAL SOURCE: use the release example for a fresh runnable demonstration.
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Julian Turner
"""Reopen verification and full-resolution sequence rendering inside Blender."""
from pathlib import Path
import argparse
import hashlib
import json
import sys
import time

sys.path.insert(0,str(Path(__file__).resolve().parent))
import bpy
from mathutils import Vector
import build_intro
import motion


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--step',type=int,default=1)
    parser.add_argument('--percentage',type=int,default=100)
    args=parser.parse_args(sys.argv[sys.argv.index('--')+1:])
    out=args.output.resolve()
    out.mkdir(parents=True,exist_ok=False)
    scene=bpy.context.scene
    if not bpy.data.filepath or scene.frame_end!=motion.FRAMES:
        raise RuntimeError('Expected the saved animated scene')
    report=build_intro.verify(scene,bpy.data.objects['CHARACTER · stage motion'],
                              {'I':bpy.data.objects['Letter I']})
    for name in ('build_intro.py','motion.py','lamp_geometry.py'):
        if bpy.data.texts[name].as_string()!=Path(__file__).with_name(name).read_text():
            raise RuntimeError('Embedded source differs: '+name)
    graph=bpy.context.evaluated_depsgraph_get()
    gimbal=bpy.data.objects['Head · gaze gimbal'].evaluated_get(graph)
    beam=(gimbal.matrix_world.to_quaternion() @ Vector((0,0,-1))).normalized()
    toward=(scene.camera.matrix_world.translation-gimbal.matrix_world.translation).normalized()
    report['final_gaze_dot_camera']=beam.dot(toward)
    if report['final_gaze_dot_camera']<.98:
        raise RuntimeError('Final gaze missed the audience')
    invalid=[obj.name for obj in bpy.data.objects if obj.animation_data
             for curve in obj.animation_data.drivers if not curve.driver.is_valid]
    if invalid:
        raise RuntimeError(('Invalid drivers',invalid))
    report['invalid_drivers']=invalid
    report['external_files']=list(bpy.utils.blend_paths(absolute=True))
    if report['external_files']:
        raise RuntimeError(('Unexpected external dependency',report['external_files']))
    (out/'reopen-checks.json').write_text(json.dumps(report,indent=2))
    scene.render.resolution_percentage=args.percentage
    scene.render.image_settings.file_format='PNG'
    scene.render.image_settings.color_mode='RGB'
    before=time.monotonic()
    captures=[]
    for frame in range(1,motion.FRAMES+1,args.step):
        scene.frame_set(frame)
        path=out/f'frame_{frame:04}.png'
        scene.render.filepath=str(path)
        status=bpy.ops.render.render('EXEC_DEFAULT',write_still=True)
        if status!={'FINISHED'} or not path.is_file():
            raise RuntimeError(('Render failed',frame,status))
        captures.append({'frame':frame,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                         'bytes':path.stat().st_size})
        if frame%24==0 or frame==1:
            print('FRAME',frame,'/',motion.FRAMES,'elapsed_s',round(time.monotonic()-before,1),flush=True)
    (out/'render-receipt.json').write_text(json.dumps({
        'scene_sha256':hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest(),
        'blender':bpy.app.version_string,'build_hash':bpy.app.build_hash.decode(),
        'engine':scene.render.engine,'resolution_percentage':args.percentage,
        'frame_step':args.step,'elapsed_seconds':time.monotonic()-before,
        'frames':captures},indent=2))
    print('SEQUENCE_FINISHED',len(captures),flush=True)


if __name__=='__main__':
    main()
