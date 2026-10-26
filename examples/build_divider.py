# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Julian Turner
"""Build a three-panel folding divider in Blender. No external assets."""
import argparse
import json
import math
from pathlib import Path
import sys
import bpy
from mathutils import Vector

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output-dir',type=Path,required=True);parser.add_argument('--width',type=float,default=1.0);parser.add_argument('--angle',type=float,default=28.0)
    args=parser.parse_args(sys.argv[sys.argv.index('--')+1:])
    if not math.isfinite(args.width) or not 0.4<=args.width<=2.0:raise ValueError('width must be finite and between 0.4 and 2.0')
    if not math.isfinite(args.angle) or not 5<=args.angle<=60:raise ValueError('angle must be finite and between 5 and 60 degrees')
    out=args.output_dir.resolve();out.mkdir(parents=True,exist_ok=False)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene=bpy.context.scene;scene['example']='folding-divider-v1';scene['panel_width']=args.width;scene['fold_degrees']=args.angle
    scene['panel_height']=1.8;scene['panel_thickness']=0.065
    # Hinge coincidence is derived from adjacent panel edge frames.
    angles=[math.radians(args.angle),-math.radians(args.angle),math.radians(args.angle)]
    left=Vector((-1.35*args.width,0,0));panels=[]
    for i,angle in enumerate(angles):
        direction=Vector((math.cos(angle),math.sin(angle),0));center=left+direction*(args.width/2)
        bpy.ops.mesh.primitive_cube_add(size=1,location=(center.x,center.y,0.9));obj=bpy.context.object;obj.name=f'Panel-{i+1}'
        obj.scale=(args.width,0.065,1.8);obj.rotation_euler.z=angle
        mat=bpy.data.materials.new(f'Panel material {i+1}');mat.diffuse_color=(*[(0.16,0.36,0.38),(0.63,0.31,0.16),(0.73,0.57,0.30)][i],1)
        mat.use_nodes=True;bs=mat.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=mat.diffuse_color;bs.inputs['Roughness'].default_value=0.6;obj.data.materials.append(mat)
        bevel=obj.modifiers.new('Soft panel edges','BEVEL');bevel.width=0.015;bevel.segments=3
        obj['part_key']=f'panel-{i+1}';panels.append(obj)
        left+=direction*args.width
        if i<2:
            bpy.ops.mesh.primitive_cylinder_add(vertices=24,radius=0.045,depth=1.86,location=(left.x,left.y,0.93));hinge=bpy.context.object;hinge.name=f'Hinge-{i+1}';hinge['part_key']=f'hinge-{i+1}'
    bpy.ops.mesh.primitive_plane_add(size=200);ground=bpy.context.object;ground.name='Ground'
    mat=bpy.data.materials.new('Ground material');mat.diffuse_color=(0.12,0.14,0.16,1);mat.use_nodes=True;mat.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=mat.diffuse_color;mat.node_tree.nodes.get('Principled BSDF').inputs['Roughness'].default_value=0.8;ground.data.materials.append(mat)
    world=bpy.data.worlds.new('Studio');world.use_nodes=True;world.node_tree.nodes['Background'].inputs[0].default_value=(0.22,0.22,0.22,1);world.node_tree.nodes['Background'].inputs[1].default_value=0.4;scene.world=world
    light=bpy.data.lights.new('Softbox','AREA');light.energy=700;light.shape='DISK';light.size=5;obj=bpy.data.objects.new('Softbox',light);scene.collection.objects.link(obj);obj.location=(1,-3,6)
    target=Vector((0,0.25,0.85));camera=bpy.data.cameras.new('Camera');obj=bpy.data.objects.new('Camera',camera);scene.collection.objects.link(obj);obj.location=(3,-6,3.4);obj.rotation_euler=(target-obj.location).to_track_quat('-Z','Y').to_euler();camera.type='ORTHO';camera.ortho_scale=max(4.5,4.3*args.width);scene.camera=obj
    scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=24;scene.render.resolution_x=640;scene.render.resolution_y=480;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG';scene.render.filepath=str(out/'preview.png')
    scene.view_settings.view_transform='Standard'
    bpy.context.view_layer.update()
    if bpy.ops.wm.save_as_mainfile(filepath=str(out/'divider.blend'),check_existing=False)!={'FINISHED'}:raise RuntimeError('Save failed')
    bpy.ops.render.render(write_still=True)
    (out/'build.json').write_text(json.dumps({'blender':bpy.app.version_string,'build_hash':bpy.app.build_hash.decode(),'width':args.width,'angle':args.angle,'scope':'Builder result; independent reopen check required'},indent=2)+'\n')
if __name__=='__main__':main()
