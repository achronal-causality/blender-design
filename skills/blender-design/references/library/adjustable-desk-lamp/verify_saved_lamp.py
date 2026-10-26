# HISTORICAL SOURCE: use the release example for a fresh runnable demonstration.
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Julian Turner
"""Read back a saved AXIS 02 file, independently inspect native relationships.

Invoke after the .blend on Blender's command line. Does not import the builder,
save the edited scene or require automatic script execution.
"""
import argparse
import hashlib
import itertools
import json
import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree


def main():
    tail=sys.argv[sys.argv.index('--')+1:]
    p=argparse.ArgumentParser()
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args(tail)
    a.output.mkdir(parents=True,exist_ok=False)
    scene=bpy.context.scene
    controls=bpy.data.objects['LAMP · ADJUST HERE']
    dims=json.loads(scene['dimensions_json'])
    poses=json.loads(scene['pose_presets_json'])
    baseline=dict(controls.items())
    assert all(abs(controls[k]-v)<1e-6 for k,v in poses['working'].items())
    assert len(bpy.data.texts['build_lamp.py'].as_string())>10000
    assert bpy.data.texts['START HERE.txt'].as_string().startswith('AXIS / 02')
    assert scene.render.engine=='CYCLES' and scene.cycles.device=='CPU'
    assert not bpy.data.libraries
    assert not bpy.data.images
    expected_parents={
        'Pivot 1 · shoulder':'Pivot 0 · base yaw',
        'Pivot 2 · elbow':'Pivot 1 · shoulder',
        'Pivot 3 · head tilt':'Pivot 2 · elbow',
        'Lower arm · single spine':'Pivot 1 · shoulder',
        'Upper arm · fork rail -1':'Pivot 2 · elbow',
        'Upper arm · fork rail 1':'Pivot 2 · elbow',
        'Head · spun shade shell':'Pivot 3 · head tilt',
        'Head · opal diffuser':'Pivot 3 · head tilt',
        'Task light · warm downward beam':'Pivot 3 · head tilt'}
    for name,parent in expected_parents.items():
        assert bpy.data.objects[name].parent.name==parent,(name,parent)
    # Eight boundary poses complement the five intended visual poses.
    for i,(shoulder,bend,pitch) in enumerate(itertools.product((70.,130.),(45.,115.),(-25.,30.))):
        poses[f'boundary-{i+1}']=dict(yaw_deg=31.,shoulder_deg=shoulder,
            elbow_bend_deg=bend,head_pitch_deg=pitch)
    results={}
    selected=['Lower arm · single spine','Upper arm · fork rail -1',
              'Upper arm · fork rail 1','Head · spun shade shell']
    for name,pose in poses.items():
        for k,v in pose.items():
            controls[k]=v
        controls.update_tag()
        bpy.context.view_layer.update()
        dg=bpy.context.evaluated_depsgraph_get()
        objects=[bpy.data.objects[n].evaluated_get(dg) for n in
                 ('Pivot 1 · shoulder','Pivot 2 · elbow','Pivot 3 · head tilt')]
        shoulder,elbow,wrist=[o.matrix_world.translation.copy() for o in objects]
        t=math.radians(pose['shoulder_deg'])
        u=math.radians(pose['shoulder_deg']-pose['elbow_bend_deg'])
        yaw=math.radians(pose['yaw_deg'])
        tipx=dims['lower_length']*math.cos(t)+dims['upper_length']*math.cos(u)
        tipz=dims['shoulder_height']+dims['lower_length']*math.sin(t)+dims['upper_length']*math.sin(u)
        error=(wrist-Vector((tipx*math.cos(yaw),tipx*math.sin(yaw),tipz))).length
        angle=math.radians(pose['head_pitch_deg'])
        head_axis=objects[-1].matrix_world.to_3x3()@Vector((1,0,0))
        expected=Vector((math.cos(yaw)*math.cos(angle),math.sin(yaw)*math.cos(angle),math.sin(angle)))
        axis_error=(head_axis-expected).length
        lengths=((elbow-shoulder).length,(wrist-elbow).length)
        assert error<1e-6 and axis_error<1e-6,(name,error,axis_error)
        assert abs(lengths[0]-.290)<1e-6 and abs(lengths[1]-.275)<1e-6
        trees={}
        head_z=[]
        for n in selected:
            ev=bpy.data.objects[n].evaluated_get(dg)
            me=ev.to_mesh()
            try:
                verts=[ev.matrix_world@v.co for v in me.vertices]
                trees[n]=BVHTree.FromPolygons(verts,[list(f.vertices) for f in me.polygons])
                if n.startswith('Head'):
                    head_z=[p.z for p in verts]
            finally:
                ev.to_mesh_clear()
        collisions=[n for n in selected[:-1] if trees[n].overlap(trees[selected[-1]])]
        assert not collisions,(name,collisions)
        assert min(head_z)>0,(name,min(head_z))
        results[name]=dict(wrist_error_m=error,head_axis_error=axis_error,
            arm_lengths_m=lengths,head_shell_desk_clearance_m=min(head_z),
            head_shell_vs_arm_surface_intersections=collisions)
    for k,v in baseline.items():
        controls[k]=v
    controls.update_tag()
    bpy.context.view_layer.update()
    drivers=[f for o in bpy.data.objects if o.animation_data for f in o.animation_data.drivers]
    assert len(drivers)==4 and all(f.driver.is_valid for f in drivers)
    assert all(f.driver.is_simple_expression for f in drivers)
    report=dict(file=bpy.data.filepath,blend_sha256=hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest(),
        identity=dict(version=bpy.app.version_string,build_hash=bpy.app.build_hash.decode()),
        source_text_sha256=hashlib.sha256(bpy.data.texts['build_lamp.py'].as_string().encode()).hexdigest(),
        parent_checks=len(expected_parents),simple_native_drivers=4,poses=results,
        limitations='Finite pose/selected-surface tests. No general all-pairs solid collision, mechanics or electrical certification.')
    (a.output/'reopen-checks.json').write_text(json.dumps(report,indent=2))
    scene.render.resolution_x=scene.render.resolution_y=800
    scene.cycles.samples=32
    scene.render.filepath=str((a.output/'reopened-hero.png').resolve())
    assert bpy.ops.render.render('EXEC_DEFAULT',write_still=True)=={'FINISHED'}
    assert (a.output/'reopened-hero.png').read_bytes().startswith(b'\x89PNG\r\n\x1a\n')
    print('AXIS02_REOPEN_VERIFIED',len(results),'poses')


if __name__=='__main__':
    main()
