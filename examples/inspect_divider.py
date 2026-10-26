# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Julian Turner
"""Independently inspect the loaded saved divider; no save or repair."""
import argparse
import json
import math
from pathlib import Path
import sys
import bpy
from mathutils import Vector
p=argparse.ArgumentParser();p.add_argument('--report',type=Path,required=True);args=p.parse_args(sys.argv[sys.argv.index('--')+1:])
if args.report.exists():raise ValueError('Report already exists')
s=bpy.context.scene
assert s.get('example')=='folding-divider-v1'
width=s['panel_width'];height=s['panel_height'];thickness=s['panel_thickness'];angle=s['fold_degrees']
assert 0.4<=width<=2.0 and 5<=angle<=60
panels=[bpy.data.objects[f'Panel-{i}'] for i in (1,2,3)]
assert len([o for o in s.objects if str(o.get('part_key','')).startswith('panel-')])==3
bpy.context.view_layer.update();errors=[]
for i,o in enumerate(panels):
    assert o.type=='MESH' and len(o.data.vertices)==8 and len(o.data.polygons)==6
    assert abs(o.scale.x-width)<1e-6 and abs(o.scale.y-thickness)<1e-6 and abs(o.scale.z-height)<1e-6
    expected=math.radians(angle)*(1 if i%2==0 else -1)
    assert abs(o.rotation_euler.z-expected)<1e-6
    assert all(math.isfinite(v) for vertex in o.data.vertices for v in o.matrix_world@vertex.co)
    assert len(o.modifiers)==1 and o.modifiers[0].type=='BEVEL'
    if i<2:
        edge=o.matrix_world@Vector((0.5,0,0));next_edge=panels[i+1].matrix_world@Vector((-0.5,0,0));hinge=bpy.data.objects[f'Hinge-{i+1}']
        error=(edge-next_edge).length;errors.append(error);assert error<1e-6
        assert (Vector((edge.x,edge.y,0))-Vector((hinge.location.x,hinge.location.y,0))).length<1e-6
assert all(not o.library for o in bpy.data.objects)
assert len(bpy.data.images)==0 and len(bpy.data.libraries)==0
assert s.camera and s.render.resolution_x==640 and s.render.resolution_y==480
report={'status':'PASS','blender':bpy.app.version_string,'build_hash':bpy.app.build_hash.decode(),'panels':3,'width':width,'angle':angle,'edge_gaps':errors,'external_images':0,'linked_libraries':0,'scope':'Saved native topology, dimensions, fold angles, attachment coincidence, camera, and dependency inspection. No collision or manufacturing certification.'}
args.report.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
