# HISTORICAL SOURCE: use the release example for a fresh runnable demonstration.
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Julian Turner
"""Build the scratch-made AXIS lamp / PIXAR intro adaptation in native Blender.

The earlier lamp is regenerated from its source, never loaded as a finished asset.
Letter contours are drawn here without a font. Animation is baked to native
keyframes and simple drivers; no playback handler or Python auto-run is needed.
"""
from pathlib import Path
import argparse
import hashlib
import json
import math
import sys
import time

sys.path.insert(0,str(Path(__file__).resolve().parent))
import bpy
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector, Quaternion
import lamp_geometry as lamp
import motion


def polygon_area(points):
    return sum(x*yy-y*xx for (x,y),(xx,yy) in zip(points,points[1:]+points[:1]))*.5


def contour_object(name, contours, material, collection, parent):
    """Filled, extruded serif contour; opposite winding marks a counter/hole."""
    data=bpy.data.curves.new(name+' outline','CURVE')
    data.dimensions='2D'
    data.resolution_u=12
    data.fill_mode='BOTH'
    data.extrude=.044
    data.bevel_depth=.0015
    data.bevel_resolution=2
    for index,points in enumerate(contours):
        points=list(points)
        if (polygon_area(points)>0)!=(index==0):
            points.reverse()
        spline=data.splines.new('POLY')
        spline.points.add(len(points)-1)
        for point,(x,y) in zip(spline.points,points):
            point.co=(x,y*motion.LETTER_HEIGHT/.75,0,1)
        spline.use_cyclic_u=True
    obj=lamp.link_obj(name,data,collection,parent)
    obj.rotation_euler.x=math.pi/2
    data.materials.append(material)
    return obj


def ellipse_half(cx,cy,rx,ry):
    return [(cx+rx*math.cos(-math.pi/2+math.pi*i/32),
             cy+ry*math.sin(-math.pi/2+math.pi*i/32)) for i in range(33)]


def letters(collection):
    mat=lamp.material('Lettering · charcoal enamel',(.009,.014,.020),.08,.35)
    roots={}
    for letter,x in [('P',-1.92),('I',motion.I_X),('X',-.48),('A',.43),('R',1.35)]:
        roots[letter]=lamp.link_obj('Letter '+letter,None,collection,xyz=(x,motion.I_Y,0))
    p=[(0,0),(.32,0),(.32,.035),(.20,.035),(.20,.345),(.30,.345)]
    p+=ellipse_half(.30,.5475,.245,.2025)
    p +=[(0,.75),(0,.715),(.10,.715),(.10,.035),(0,.035)]
    counter=[(.20,.435)]+ellipse_half(.30,.55,.140,.115)+[(.20,.665)]
    contour_object('P · serif and bowl',[p,counter],mat,collection,roots['P'])
    contour_object('R · serif and bowl',[p,counter],mat,collection,roots['R'])
    leg=[(.20,.377),(.318,.377),(.582,.035),(.65,.035),(.65,0),(.43,0),(.43,.035),(.455,.035)]
    contour_object('R · diagonal leg',[leg],mat,collection,roots['R'])
    ip=[(-.14,0),(.14,0),(.14,.037),(.045,.037),(.045,.713),(.14,.713),
        (.14,.75),(-.14,.75),(-.14,.713),(-.045,.713),(-.045,.037),(-.14,.037)]
    contour_object('I · squashable serif',[ip],mat,collection,roots['I'])
    # X: two contrasting diagonal strokes with slab serifs. All parts are authored.
    for n,poly in enumerate([
        [(0,0),(.23,0),(.23,.035),(.17,.035),(.54,.715),(.62,.715),(.62,.75),(.40,.75),(.40,.715),(.47,.715),(.10,.035),(0,.035)],
        [(0,.75),(.22,.75),(.22,.715),(.16,.715),(.56,.035),(.64,.035),(.64,0),(.40,0),(.40,.035),(.46,.035),(.06,.715),(0,.715)]
    ]):
        contour_object('X · stroke '+str(n),[poly],mat,collection,roots['X'])
    for n,poly in enumerate([
        [(0,0),(.19,0),(.19,.035),(.13,.035),(.345,.64),(.30,.75),(.025,.035),(0,.035)],
        [(.30,.75),(.36,.75),(.635,.035),(.67,.035),(.67,0),(.425,0),(.425,.035),(.50,.035)],
        [(.158,.255),(.497,.255),(.474,.313),(.182,.313)]
    ]):
        contour_object('A · stroke '+str(n),[poly],mat,collection,roots['A'])
    return roots


def create_scene():
    scene,controls=lamp.build_scene(lamp.DIMENSIONS)
    scene.name='AXIS · a lamp intro from scratch'
    lampcol=bpy.data.collections['01 · LAMP | editable parts']
    rig=bpy.data.collections['02 · PIVOTS | controls']
    stage=bpy.data.collections['03 · STUDIO']
    # Free the character to hop; retain the previous lamp as untouched source.
    for obj in list(lampcol.objects):
        if obj.name.startswith(('Supply cord','Base · rotary','Base · dimmer','Base · maker')):
            bpy.data.objects.remove(obj,do_unlink=True)
    mover=lamp.link_obj('CHARACTER · stage motion',None,rig)
    mover.empty_display_type='ARROWS'
    mover.scale=(motion.SCALE,)*3
    for col in (lampcol,rig):
        for obj in list(col.objects):
            if obj!=mover and obj.parent is None:
                obj.parent=mover
    # A new shade gimbal provides readable gaze without detaching the arm chain.
    wrist=bpy.data.objects['Pivot 3 · head tilt']
    gaze=lamp.link_obj('Head · gaze gimbal',None,rig,wrist,(lamp.DIMENSIONS['head_offset'],0,-.012))
    gaze.rotation_mode='QUATERNION'
    for obj in list(wrist.children):
        if obj.name.startswith(('Head · spun','Head · reflector','Head · opal','Head · cooling','Task light')):
            obj.parent=gaze
            obj.location -= Vector((lamp.DIMENSIONS['head_offset'],0,-.012))
    lamp.cylinder('Head · swivel bearing',.020,.018,bpy.data.materials['03 · Satin aluminium'],
                  lampcol,wrist,(lamp.DIMENSIONS['head_offset'],0,-.012),bevel=.003)
    # Film materials retain the sage/copper character, with a subdued studio floor.
    coat=bpy.data.materials['01 · Deep sage | powder coat'].node_tree.nodes.get('Principled BSDF')
    coat.inputs['Base Color'].default_value=(.055,.18,.13,1)
    coat.inputs['Roughness'].default_value=.38
    for obj in list(stage.objects):
        bpy.data.objects.remove(obj,do_unlink=True)
    titlecol=bpy.data.collections.new('04 · LETTERS | original contours')
    scene.collection.children.link(titlecol)
    title=letters(titlecol)
    floor=lamp.material('Stage · cool grey cyclorama',(.45,.50,.55),0,.8)
    lamp.mesh_obj('Stage · infinite floor',[(-100,-100,-.002),(100,-100,-.002),(100,100,-.002),(-100,100,-.002)],
                  [(0,1,2,3)],floor,stage)
    scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.55,.62,.72,1)
    scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.45
    for name,loc,power,size,color in [
        ('Key · broad window',(-3,-4,6),1150,5.,(1.,.93,.83)),
        ('Fill · sky',(3,-1,4),600,4.,(.75,.85,1.)),
        ('Rim · soft',(0,4,5),950,4.,(1.,1.,1.))]:
        data=bpy.data.lights.new(name,'AREA')
        data.energy=power
        data.shape='DISK'
        data.size=size
        data.color=color
        light=lamp.link_obj(name,data,stage,xyz=loc)
        lamp.aim(light,(0,0,.4))
    camdata=bpy.data.cameras.new('Camera · title stage')
    camdata.type='ORTHO'
    camdata.ortho_scale=5.30
    camdata.clip_start=.05
    camdata.clip_end=200
    camera=lamp.link_obj('Camera · title stage',camdata,stage,xyz=(0,-8,2.3))
    lamp.aim(camera,(0,.1,.80))
    scene.camera=camera
    scene.render.engine='BLENDER_EEVEE'
    if hasattr(scene.eevee,'taa_render_samples'):
        scene.eevee.taa_render_samples=64
    if hasattr(scene.eevee,'use_raytracing'):
        scene.eevee.use_raytracing=True
    scene.render.resolution_x=1280
    scene.render.resolution_y=720
    scene.render.resolution_percentage=100
    scene.render.fps=motion.FPS
    scene.frame_start=1
    scene.frame_end=motion.FRAMES
    scene.render.image_settings.file_format='PNG'
    scene.render.image_settings.color_mode='RGB'
    scene.render.image_settings.color_depth='8'
    scene.render.image_settings.compression=20
    scene.render.film_transparent=False
    scene.render.use_motion_blur=False
    scene.view_settings.view_transform='AgX'
    scene.view_settings.look='AgX - Medium High Contrast'
    scene.view_settings.exposure=0
    scene['original_asset_policy']='Lamp regenerated from prior procedural source; lettering, set, choreography and Foley authored from scratch. No external model, font, texture, footage or audio samples.'
    scene['adaptation']='Springy cartoon revision: impulse recovery, volume-preserving squash/stretch, rebound hops and shade follow-through.'
    scene['timing_fps']=motion.FPS
    scene['letter_height_m']=motion.LETTER_HEIGHT
    # Expand editable UI ranges deliberately for character anticipation.
    controls.id_properties_ui('shoulder_deg').update(min=70,max=145)
    controls.id_properties_ui('elbow_bend_deg').update(min=20,max=165)
    return scene,controls,mover,gaze,title


def animate(scene,controls,mover,gaze,title):
    timing=[]
    previous=None
    light=bpy.data.lights['Task light · warm downward beam']
    diffuse=bpy.data.materials['06 · Warm opal LED diffuser'].node_tree.nodes.get('Principled BSDF')
    for frame in range(1,motion.FRAMES+1):
        scene.frame_set(frame)
        state=motion.state(frame)
        mover.location=state['position']
        mover.keyframe_insert('location',frame=frame,group='Ballistic travel and support')
        mover.scale=state['character_scale']
        mover.keyframe_insert('scale',frame=frame,group='Cartoon squash and stretch')
        for prop,key in [('shoulder_deg','shoulder'),('elbow_bend_deg','bend'),('yaw_deg','yaw'),('head_pitch_deg','pitch')]:
            controls[prop]=state[key]
            controls.keyframe_insert(data_path='["'+prop+'"]',frame=frame,group='Rigid-joint performance')
        title['I'].scale.z=state['letter_scale']
        title['I'].keyframe_insert('scale',frame=frame,index=2,group='Impact compression')
        controls.update_tag()
        bpy.context.view_layer.update()
        head=gaze.matrix_world.translation.copy()
        target=Vector(state['gaze']).lerp(scene.camera.location,state['look_camera'])
        direction=target-head
        # The full inverse also accounts for the nonuniform cartoon scale.
        local_direction=gaze.parent.matrix_world.to_3x3().inverted() @ direction
        q=local_direction.to_track_quat('-Z','Y')
        if previous is not None:
            if previous.dot(q)<0:
                q.negate()
            # Damped attention, rather than an instantaneous look-at snap.
            q=previous.slerp(q,.24 if frame<315 else .14)
        previous=q.copy()
        gaze.rotation_quaternion=q @ Quaternion((0,1,0),math.radians(state['head_wobble_deg']))
        gaze.keyframe_insert('rotation_quaternion',frame=frame,group='Attention and audience look')
        light.energy=state['lamp_power']
        light.keyframe_insert('energy',frame=frame)
        diffuse.inputs['Emission Strength'].default_value=state['lamp_power']*.6
        diffuse.inputs['Emission Strength'].keyframe_insert('default_value',frame=frame)
        timing.append(state)
    # Per-frame samples interpolate linearly, making subframes predictable.
    for action in bpy.data.actions:
        for layer in action.layers:
            for strip in layer.strips:
                for bag in strip.channelbags:
                    for curve in bag.fcurves:
                        for point in curve.keyframe_points:
                            point.interpolation='LINEAR'
    for frame,name in [(1,'Logo'),(28,'Entrance'),(126,'Notice the I'),(160,'First leap'),
                       (186,'First stamp'),(229,'Second stamp'),(274,'Final stamp'),
                       (314,'Look to audience'),(342,'Hold'),(366,'Editorial fade')]:
        scene.timeline_markers.new(name,frame=frame)
    scene.frame_set(342)
    return timing


def verify(scene,mover,title):
    """Check all stored frames, not just the authored formulas."""
    report={'frames':motion.FRAMES,'max_character_space_link_error_m':0.,'max_trajectory_error_m':0.,
            'max_support_error_m':0.,'min_shade_floor_clearance_m':1e9,
            'min_stretch':1e9,'max_stretch':0.,'max_volume_scale_error':0.,
            'rebound_frames':[],'min_support_clearance_m':1e9,
            'min_character_camera_margin':1e9,
            'min_foot_height_m':1e9,'max_foot_height_m':0.,'impact_frames':motion.LANDINGS,
            'scope':'Character-space link lengths, deliberate cartoon deformation, constant deformation volume, evaluated trajectory, support and rebound clearance at every frame. No continuous all-pairs collision or dynamics simulation.'}
    for frame in range(1,motion.FRAMES+1):
        scene.frame_set(frame)
        graph=bpy.context.evaluated_depsgraph_get()
        pivots=[bpy.data.objects[n].evaluated_get(graph).matrix_world.translation.copy() for n in
                ('Pivot 1 · shoulder','Pivot 2 · elbow','Pivot 3 · head tilt')]
        character_matrix=mover.evaluated_get(graph).matrix_world
        inverse=character_matrix.inverted()
        pivots=[inverse @ point for point in pivots]
        for i,key in enumerate(('lower_length','upper_length')):
            error=abs((pivots[i+1]-pivots[i]).length-lamp.DIMENSIONS[key])
            report['max_character_space_link_error_m']=max(report['max_character_space_link_error_m'],error)
            if error>1e-5:
                raise RuntimeError(('Arm length changed',frame,error))
        actual=mover.evaluated_get(graph).matrix_world.translation
        expected=Vector(motion.state(frame)['position'])
        error=(actual-expected).length
        report['max_trajectory_error_m']=max(report['max_trajectory_error_m'],error)
        if error>1e-5 or actual.z < -1e-6:
            raise RuntimeError(('Trajectory mismatch',frame,tuple(actual),tuple(expected)))
        report['min_foot_height_m']=min(report['min_foot_height_m'],actual.z)
        report['max_foot_height_m']=max(report['max_foot_height_m'],actual.z)
        state=motion.state(frame)
        stretch=character_matrix.to_scale().z/motion.SCALE
        report['min_stretch']=min(report['min_stretch'],stretch)
        report['max_stretch']=max(report['max_stretch'],stretch)
        volume_error=abs(character_matrix.to_3x3().determinant()-motion.SCALE**3)
        report['max_volume_scale_error']=max(report['max_volume_scale_error'],volume_error)
        if volume_error>1e-5:
            raise RuntimeError(('Squash/stretch changed volume',frame,volume_error))
        if frame>=186 and state['phase']!='stamp-flight':
            support=title['I'].evaluated_get(graph).matrix_world.to_scale().z*motion.LETTER_HEIGHT
            error=abs(actual.z-support-state['rebound_lift'])
            report['max_support_error_m']=max(report['max_support_error_m'],error)
            if error>1e-5:
                raise RuntimeError(('Foot lost the letter support',frame,error))
        if state['phase'] not in ('entry-flight','stamp-flight'):
            clearance=actual.z-state['support_height']
            report['min_support_clearance_m']=min(report['min_support_clearance_m'],clearance)
            if clearance < -1e-5:
                raise RuntimeError(('Foot penetrated its support',frame,clearance))
        if state['rebound_lift']>0:
            report['rebound_frames'].append(frame)
        shade=bpy.data.objects['Head · opal diffuser'].evaluated_get(graph)
        clearance=min((shade.matrix_world @ Vector(corner)).z for corner in shade.bound_box)
        report['min_shade_floor_clearance_m']=min(report['min_shade_floor_clearance_m'],clearance)
        if clearance<0:
            raise RuntimeError(('Shade intersects the floor',frame,clearance))
        if frame>=45:
            for name in ('Head · spun shade shell','Base · non-slip sole'):
                obj=bpy.data.objects.get(name)
                if obj is None:
                    raise RuntimeError(('Missing camera-check object',name))
                obj=obj.evaluated_get(graph)
                for corner in obj.bound_box:
                    p=world_to_camera_view(scene,scene.camera,obj.matrix_world @ Vector(corner))
                    margin=min(p.x,1-p.x,p.y,1-p.y)
                    report['min_character_camera_margin']=min(report['min_character_camera_margin'],margin)
                    if margin<0:
                        raise RuntimeError(('Character cropped',frame,name,tuple(p)))
        if not all(math.isfinite(v) for obj in (mover,title['I']) for row in obj.matrix_world for v in row):
            raise RuntimeError('Nonfinite transform')
    scene.frame_set(342)
    if not (report['min_stretch']<.7 and report['max_stretch']>1.2 and len(report['rebound_frames'])>30):
        raise RuntimeError('Springiness channels were not baked')
    report['native_action_count']=len(bpy.data.actions)
    report['driver_count']=sum(len(obj.animation_data.drivers) for obj in bpy.data.objects if obj.animation_data)
    return report


def main():
    argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--preview',default='1,55,136,176,198,239,294,342')
    parser.add_argument('--engine',choices=['BLENDER_EEVEE','CYCLES'],default='BLENDER_EEVEE')
    args=parser.parse_args(argv)
    out=args.output.resolve()
    out.mkdir(parents=True,exist_ok=False)
    if bpy.app.version!=(5,2,2) or bpy.app.build_hash.decode()!='d13f752e3b9c':
        raise RuntimeError('Blender baseline drift')
    scene,controls,mover,gaze,title=create_scene()
    scene.render.engine=args.engine
    if args.engine=='CYCLES':
        scene.cycles.device='CPU'
        scene.cycles.samples=24
        scene.cycles.use_denoising=True
    timing=animate(scene,controls,mover,gaze,title)
    (out/'timing.json').write_text(json.dumps(timing,indent=2))
    report=verify(scene,mover,title)
    (out/'geometry-checks.json').write_text(json.dumps(report,indent=2))
    for name in ('build_intro.py','motion.py','lamp_geometry.py'):
        source=Path(__file__).with_name(name).read_text()
        bpy.data.texts.new(name).write(source)
    bpy.data.texts.new('START HERE').write('AXIS lamp intro. Frames 1–384, 24 fps. Native baked keyframes and joint drivers. Play timeline; render camera. All assets procedurally authored. Source is embedded and delivered alongside the scene. Editorial fade and synthesized Foley are in the final MP4.\n')
    scene.render.filepath='//frames/frame_'
    scene.frame_set(342)
    result=bpy.ops.wm.save_as_mainfile(filepath=str(out/'lamp-intro.blend'),check_existing=False)
    if result!={'FINISHED'}:
        raise RuntimeError(result)
    preview_dir=out/'previews'
    preview_dir.mkdir()
    for frame in [int(x) for x in args.preview.split(',') if x]:
        scene.frame_set(frame)
        scene.render.resolution_percentage=60
        scene.render.filepath=str(preview_dir/f'frame-{frame:04}.png')
        before=time.monotonic()
        status=bpy.ops.render.render('EXEC_DEFAULT',write_still=True)
        if status!={'FINISHED'}:
            raise RuntimeError(status)
        print('PREVIEW',frame,round(time.monotonic()-before,3),flush=True)
    (out/'build-receipt.json').write_text(json.dumps({'blender':bpy.app.version_string,
        'build_hash':bpy.app.build_hash.decode(),'engine':args.engine,
        'scene_sha256':hashlib.sha256((out/'lamp-intro.blend').read_bytes()).hexdigest(),
        'source_sha256':{name:hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
                         for name in ('build_intro.py','motion.py','lamp_geometry.py')},
        'verification':report},indent=2))
    print('INTRO_BUILT',out,flush=True)


if __name__=='__main__':
    main()
