# HISTORICAL SOURCE: use the release example for a fresh runnable demonstration.
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Julian Turner
"""AXIS / 02. Native Blender task lamp. Run with Blender --background --python.

All dimensions are metres. No add-ons, handlers or external assets are required.
The only custom geometry is an extruded capsule and surfaces of revolution:
the former describes machined arm profiles, the latter describes turned parts.
"""
import argparse
import hashlib
import json
import math
import platform
import sys
from pathlib import Path

import bpy
import bmesh
from mathutils import Vector

EXPECTED_VERSION = (5, 2, 2)
EXPECTED_HASH = 'd13f752e3b9c'
OWNER = 'axis02'

# Primary dimensional design parameters. Poses remain editable without rebuilding.
DIMENSIONS = dict(lower_length=.290, upper_length=.275, base_radius=.145,
                  shoulder_height=.090, head_offset=.150, shade_radius=.105)
POSES = {
    'working': dict(yaw_deg=0., shoulder_deg=110., elbow_bend_deg=88., head_pitch_deg=-8.),
    'reach': dict(yaw_deg=0., shoulder_deg=78., elbow_bend_deg=60., head_pitch_deg=0.),
    'upright': dict(yaw_deg=0., shoulder_deg=120., elbow_bend_deg=50., head_pitch_deg=-18.),
    'compact': dict(yaw_deg=0., shoulder_deg=126., elbow_bend_deg=115., head_pitch_deg=-10.),
    'turned': dict(yaw_deg=-45., shoulder_deg=105., elbow_bend_deg=80., head_pitch_deg=15.),
}
LIMITS = {'yaw_deg': (-180., 180.), 'shoulder_deg': (70., 130.),
          'elbow_bend_deg': (45., 115.), 'head_pitch_deg': (-25., 30.)}


def material(name, color, metallic=0., roughness=.4, emission=0.):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    p = m.node_tree.nodes.get('Principled BSDF')
    p.inputs['Base Color'].default_value = (*color, 1)
    p.inputs['Metallic'].default_value = metallic
    p.inputs['Roughness'].default_value = roughness
    if emission:
        p.inputs['Emission Color'].default_value = (*color, 1)
        p.inputs['Emission Strength'].default_value = emission
    m.diffuse_color = (*color, 1)
    return m


def link_obj(name, data, collection, parent=None, xyz=(0, 0, 0)):
    o = bpy.data.objects.new(name, data)
    collection.objects.link(o)
    o['owner'] = OWNER
    if parent:
        o.parent = parent
    o.location = xyz
    return o


def mesh_obj(name, verts, faces, mat, collection, parent=None, xyz=(0, 0, 0), bevel=0., smooth=False):
    me = bpy.data.meshes.new(name + ' · mesh')
    me.from_pydata(verts, [], faces)
    if me.validate(verbose=True):
        raise ValueError(name + ': invalid constructed mesh')
    me.update(calc_edges=True)
    o = link_obj(name, me, collection, parent, xyz)
    me.materials.append(mat)
    for f in me.polygons:
        f.use_smooth = smooth
    if bevel:
        b = o.modifiers.new('Machined edge radius', 'BEVEL')
        b.width = bevel
        b.segments = 3
        b.limit_method = 'ANGLE'
        b.angle_limit = math.radians(30)
        b.harden_normals = True
        n = o.modifiers.new('Face normals', 'WEIGHTED_NORMAL')
        n.keep_sharp = True
    return o


def revolved(name, profile, mat, collection, parent=None, xyz=(0, 0, 0), n=96, axis='Z'):
    """Closed cross-section in radius/height, revolved around the local Z or Y axis."""
    verts = []
    for r, z in profile:
        for i in range(n):
            t = 2 * math.pi * i / n
            v = (r * math.cos(t), r * math.sin(t), z)
            verts.append(v if axis == 'Z' else (v[0], -v[2], v[1]))
    faces = []
    for j in range(len(profile)):
        jj = (j + 1) % len(profile)
        for i in range(n):
            ii = (i + 1) % n
            faces.append((j*n+i, j*n+ii, jj*n+ii, jj*n+i))
    # Profile travels outwards along bottom, then upwards, then inward at the top.
    return mesh_obj(name, verts, faces, mat, collection, parent, xyz, smooth=True)


def cylinder(name, radius, depth, mat, collection, parent=None, xyz=(0, 0, 0), axis='Z', bevel=.001, n=64):
    bm = bmesh.new()
    try:
        bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=n,
                             radius1=radius, radius2=radius, depth=depth)
        bm.normal_update()
        bm.verts.ensure_lookup_table()
        verts = [tuple(v.co) for v in bm.verts]
        faces = [tuple(v.index for v in f.verts) for f in bm.faces]
    finally:
        bm.free()
    o = mesh_obj(name, verts, faces, mat, collection, parent, xyz, bevel, smooth=True)
    if axis == 'Y':
        o.rotation_euler.x = math.pi / 2
    return o


def capsule(name, length, radius, depth, mat, collection, parent, xyz=(0, 0, 0), bevel=.001):
    """Extruded stadium profile: centres at x=0 and x=length, hinge axis Y."""
    outline = []
    for center, start in ((length, -math.pi/2), (0., math.pi/2)):
        for i in range(17):
            t = start + math.pi*i/16
            outline.append((center + radius*math.cos(t), radius*math.sin(t)))
    n = len(outline)
    verts = [(x, y, z) for y in (-depth/2, depth/2) for x, z in outline]
    faces = [tuple(range(n)), tuple(range(2*n-1, n-1, -1))]
    faces.extend((i, i+n, (i+1)%n+n, (i+1)%n) for i in range(n))
    return mesh_obj(name, verts, faces, mat, collection, parent, xyz, bevel)


def curve(name, points, radius, mat, collection, parent=None):
    c = bpy.data.curves.new(name + ' · path', 'CURVE')
    c.dimensions = '3D'
    c.resolution_u = 20
    c.bevel_depth = radius
    c.bevel_resolution = 4
    c.use_fill_caps = True
    s = c.splines.new('BEZIER')
    s.bezier_points.add(len(points)-1)
    for b, p in zip(s.bezier_points, points):
        b.co = p
        b.handle_left_type = b.handle_right_type = 'AUTO'
    o = link_obj(name, c, collection, parent)
    c.materials.append(mat)
    return o


def driven_rotation(o, axis, expression, controls, variables):
    f = o.driver_add('rotation_euler', axis)
    d = f.driver
    d.type = 'SCRIPTED'
    for short, prop in variables.items():
        v = d.variables.new()
        v.name = short
        v.type = 'SINGLE_PROP'
        v.targets[0].id = controls
        v.targets[0].data_path = '["' + prop + '"]'
    d.expression = expression


def set_pose(controls, pose):
    for k, v in pose.items():
        controls[k] = v
    controls.update_tag()
    bpy.context.view_layer.update()


def add_joint(name, parent, xyz, radius, width, green, rubber, metal, copper, col, grip=True):
    cylinder(name + ' · barrel', radius, width, green, col, parent, xyz, 'Y')
    for s in (-1, 1):
        p = (xyz[0], xyz[1] + s*(width/2+.0013), xyz[2])
        cylinder(name + f' · friction washer {s}', radius*.9, .0025, rubber, col, parent, p, 'Y', .0003)
        p = (xyz[0], xyz[1] + s*(width/2+.004), xyz[2])
        cylinder(name + f' · axle cap {s}', radius*.77, .004, metal, col, parent, p, 'Y', .0007)
    p = (xyz[0], xyz[1] - width/2-.009, xyz[2])
    knob = cylinder(name + ' · torque dial', radius*.72, .008, copper, col, parent, p, 'Y', .001)
    cylinder(name + ' · centre fastener', radius*.26, .0015, rubber, col, parent,
             (p[0], p[1]-.0046, p[2]), 'Y', .0003, n=6)
    if grip:
        # Repeated shallow ribs represent a tactile grip, not decorative noise.
        for i in range(28):
            t = 2*math.pi*i/28
            rr = radius*.718
            cylinder(name + f' · grip {i:02}', .00048, .0055, copper, col, parent,
                     (p[0]+rr*math.cos(t), p[1], p[2]+rr*math.sin(t)), 'Y', .00015, n=8)
    return knob


def aim(o, target):
    o.rotation_euler = (Vector(target)-o.location).to_track_quat('-Z', 'Y').to_euler()


def fit_camera(scene, direction, margin=1.22):
    """Frame the product's evaluated solid parts; the supply lead may leave frame."""
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get()
    points = []
    for o in bpy.data.collections['01 · LAMP | editable parts'].objects:
        if o.type == 'MESH':
            ev = o.evaluated_get(dg)
            points.extend(ev.matrix_world @ Vector(v) for v in ev.bound_box)
    direction = Vector(direction).normalized()
    rotation = (-direction).to_track_quat('-Z','Y')
    inverse = rotation.inverted()
    local = [inverse @ p for p in points]
    mins = Vector(tuple(min(p[i] for p in local) for i in range(3)))
    maxs = Vector(tuple(max(p[i] for p in local) for i in range(3)))
    target = rotation @ ((mins+maxs)*.5)
    camera = scene.camera
    camera.rotation_euler = rotation.to_euler()
    camera.location = target + direction*2.8
    camera.data.ortho_scale = max(maxs.x-mins.x,maxs.y-mins.y)*margin
    bpy.context.view_layer.update()


def build_scene(dims):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.name = 'AXIS / 02 · articulated task light'
    scene.unit_settings.system = 'METRIC'
    scene.unit_settings.length_unit = 'MILLIMETERS'
    scene.unit_settings.scale_length = 1.
    scene['construction'] = 'Rigid serial linkage; shoulder and elbow rotate around Y, base around Z. Head pitch is compensated to world elevation.'
    scene['dimensions_json'] = json.dumps(dims, sort_keys=True)
    scene['pose_presets_json'] = json.dumps(POSES, sort_keys=True)
    lamp = bpy.data.collections.new('01 · LAMP | editable parts')
    rig = bpy.data.collections.new('02 · PIVOTS | controls')
    stage = bpy.data.collections.new('03 · STUDIO')
    for c in (lamp, rig, stage):
        scene.collection.children.link(c)
    green = material('01 · Deep sage | powder coat', (.031, .093, .068), .20, .32)
    rubber = material('02 · Graphite | elastomer', (.017, .022, .023), .05, .58)
    metal = material('03 · Satin aluminium', (.51, .56, .55), .86, .24)
    copper = material('04 · Burnt copper | anodised dial', (.57, .205, .068), .72, .29)
    ivory = material('05 · Ceramic reflector', (.82, .79, .69), .02, .33)
    diffuser = material('06 · Warm opal LED diffuser', (1., .78, .48), .0, .42, 2.5)
    floor = material('07 · Warm mineral desk', (.30, .265, .223), .05, .54)

    # A weighted circular plinth, bottom gasket, and stationary cable outlet.
    cylinder('Base · non-slip sole', dims['base_radius']-.003, .005, rubber, lamp, xyz=(0,0,.0025), bevel=.002)
    r = dims['base_radius']
    revolved('Base · weighted cast plinth', [(.002,.004),(r-.005,.004),(r,.009),(r,.026),
             (r-.001,.030),(r-.005,.034),(.002,.034)], green, lamp)
    cylinder('Base · inset top', r-.010, .0012, green, lamp, xyz=(0,0,.0341), bevel=.0005)
    cylinder('Base · rotary dimmer bezel', .018, .002, rubber, lamp, xyz=(.080,-.047,.035))
    cylinder('Base · rotary dimmer', .0147, .008, copper, lamp, xyz=(.080,-.047,.039), bevel=.0015)
    cylinder('Base · dimmer indicator', .0007, .00035, ivory, lamp, xyz=(.080,-.056,.0432), bevel=.0001, n=16)
    # Thin concentric collar visually separates the rotating turret from the base.
    cylinder('Turret · bearing collar', .035, .004, metal, lamp, xyz=(0,0,.0365), bevel=.0007)
    control = link_obj('LAMP · ADJUST HERE', None, rig)
    control.empty_display_type = 'CIRCLE'
    control.empty_display_size = .18
    descriptions = {
        'yaw_deg': 'Base rotation in degrees about vertical Z.',
        'shoulder_deg': 'Lower arm elevation from the horizontal. Greater values lean rearward.',
        'elbow_bend_deg': 'Clockwise bend relative to lower arm; upper elevation = shoulder minus bend.',
        'head_pitch_deg': 'Absolute head elevation; 0 keeps the diffuser parallel to the desk.'}
    for k, v in POSES['working'].items():
        control[k] = v
        control.id_properties_ui(k).update(min=LIMITS[k][0], max=LIMITS[k][1],
            soft_min=LIMITS[k][0], soft_max=LIMITS[k][1], description=descriptions[k])
    root = link_obj('Pivot 0 · base yaw', None, rig)
    driven_rotation(root, 2, 'yaw*pi/180', control, {'yaw':'yaw_deg'})
    cylinder('Turret · rotating pedestal', .029, .032, green, lamp, root, (0,0,.055), bevel=.003)
    # A solid shoulder barrel joins the pedestal to the rotating lower spine.
    p0 = link_obj('Pivot 1 · shoulder', None, rig, root, (0,0,dims['shoulder_height']))
    driven_rotation(p0, 1, '-shoulder*pi/180', control, {'shoulder':'shoulder_deg'})
    L1, L2 = dims['lower_length'], dims['upper_length']
    lower = capsule('Lower arm · single spine', L1, .016, .027, green, lamp, p0, bevel=.0015)
    lower['segment_length'] = L1
    # Recess-colored trim remains a separate editable part following the rigid arm.
    for side in (-1, 1):
        capsule('Lower arm · satin inset ' + str(side), L1-.088, .004, .0008, metal, lamp, p0,
                (.044, side*.0138, 0), bevel=.0003)
    add_joint('Shoulder', p0, (0,0,0), .029, .065, green, rubber, metal, copper, lamp)
    p1 = link_obj('Pivot 2 · elbow', None, rig, p0, (L1,0,0))
    driven_rotation(p1, 1, 'bend*pi/180', control, {'bend':'elbow_bend_deg'})
    for side in (-1, 1):
        rail = capsule('Upper arm · fork rail ' + str(side), L2, .0125, .009, green, lamp, p1,
                       (0,side*.024,0), bevel=.0012)
        rail['segment_length'] = L2
    for x in (.048,L2-.043):
        cylinder('Upper arm · spacer ' + str(x), .006, .042, metal, lamp, p1, (x,0,0), 'Y', .001)
    add_joint('Elbow', p1, (0,0,0), .026, .058, green, rubber, metal, copper, lamp)
    p2 = link_obj('Pivot 3 · head tilt', None, rig, p1, (L2,0,0))
    driven_rotation(p2, 1, '(shoulder-bend-pitch)*pi/180', control,
                    {'shoulder':'shoulder_deg','bend':'elbow_bend_deg','pitch':'head_pitch_deg'})
    h = dims['head_offset']
    capsule('Head · cantilever neck', h, .010, .022, green, lamp, p2, bevel=.0012)
    add_joint('Wrist', p2, (0,0,0), .021, .058, green, rubber, metal, copper, lamp, grip=False)
    cylinder('Head · crown mount', .019, .016, metal, lamp, p2, (h,0,-.008), bevel=.002)
    sr = dims['shade_radius']
    # A physically readable shell: thickness 2.8–5 mm, rounded lip, open underside.
    profile = [(.016,-.018),(.048,-.018),(sr-.015,-.034),(sr-.003,-.045),
               (sr,-.049),(sr,-.054),(sr-.003,-.057),(sr-.008,-.057),
               (sr-.010,-.052),(sr-.017,-.040),(.047,-.023),(.016,-.023)]
    # This section runs clockwise; reverse for outward normals.
    shell = revolved('Head · spun shade shell', list(reversed(profile)), green, lamp, p2, (h,0,0), n=128)
    shell['wall_min_mm'] = 2.8
    # Reflector lip and flush luminous disc are separately editable pieces.
    revolved('Head · reflector lip', [(sr-.013,-.054),(sr-.007,-.054),(sr-.007,-.051),
              (sr-.013,-.050)], ivory, lamp, p2, (h,0,0), n=128)
    cylinder('Head · opal diffuser', sr-.013, .003, diffuser, lamp, p2, (h,0,-.052), bevel=.001, n=128)
    for rr in (.024,.031,.038):
        revolved('Head · cooling rib ' + str(rr), [(rr,-.018),(rr+.0018,-.018),
                  (rr+.0018,-.015),(rr,-.015)], green, lamp, p2, (h,0,0))
    light = bpy.data.lights.new('Task light · warm downward beam', 'AREA')
    light.energy = 7.
    light.color = (1., .79, .55)
    light.shape = 'DISK'
    light.size = .175
    link_obj('Task light · warm downward beam', light, lamp, p2, (h,0,-.055))
    # Power is routed through hollow pivots/arms; only the stationary supply is shown.
    curve('Supply cord · desk loop', [(-.132,.030,.016),(-.165,.034,.010),(-.20,.07,.004),
           (-.28,.075,.0033),(-.345,.035,.0033),(-.48,.055,.0033),(-.85,.10,.0033)], .0032, rubber, lamp)
    grommet = cylinder('Supply cord · strain relief', .006, .020, rubber, lamp,
                      xyz=(-.142,.032,.015), bevel=.001)
    grommet.rotation_euler.y = math.pi/2

    # Small, physically plausible etched maker's mark on the base top.
    txt = bpy.data.curves.new('AXIS 02 · lettering', 'FONT')
    txt.body = 'A X I S  /  0 2'
    txt.size = .006
    txt.extrude = .00002
    txt.align_x = 'CENTER'
    tx = link_obj('Base · maker mark', txt, lamp, xyz=(0,-.105,.0348))
    txt.materials.append(metal)

    # Fixed studio and framing. All lamp parts remain in their own collection.
    mesh_obj('Studio · desk', [(-200,-200,0),(200,-200,0),(200,200,0),(-200,200,0)],
             [(0,1,2,3)], floor, stage)
    world = bpy.data.worlds.new('Studio · soft ambient')
    world.use_nodes = True
    world.node_tree.nodes['Background'].inputs['Color'].default_value = (.36,.42,.48,1)
    world.node_tree.nodes['Background'].inputs['Strength'].default_value = .25
    scene.world = world
    for name, xyz, energy, size, color in (
        ('Key · softbox',(-.35,-.45,1.05),55.,.70,(1.,.90,.76)),
        ('Fill · window',(.55,.20,.8),35.,.55,(.77,.88,1.)),
        ('Rim · strip',(-.5,.4,.70),45.,.40,(1.,.94,.83))):
        ld = bpy.data.lights.new(name, 'AREA')
        ld.energy, ld.shape, ld.size, ld.color = energy, 'DISK', size, color
        lo = link_obj(name, ld, stage, xyz=xyz)
        aim(lo,(.03,0,.28))
    camera_data = bpy.data.cameras.new('Presentation · camera')
    camera_data.type = 'ORTHO'
    camera_data.ortho_scale = .88
    camera_data.lens = 70
    camera_data.clip_start = .01
    camera_data.clip_end = 100
    camera = link_obj('Presentation · camera', camera_data, stage, xyz=(.85,-1.3,.88))
    aim(camera,(.045,0,.285))
    scene.camera = camera
    scene.render.engine = 'CYCLES'
    scene.cycles.device = 'CPU'
    scene.cycles.samples = 64
    scene.cycles.use_denoising = True
    scene.cycles.use_adaptive_sampling = False
    scene.render.resolution_x = scene.render.resolution_y = 1200
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGBA'
    scene.render.image_settings.color_depth = '8'
    scene.render.use_file_extension = True
    scene.render.use_border = False
    scene.render.use_sequencer = False
    scene.render.use_compositing = False
    scene.render.film_transparent = False
    scene.view_settings.view_transform = 'AgX'
    scene.view_settings.look = 'AgX - Medium High Contrast'
    scene.view_settings.exposure = 0
    scene.view_settings.gamma = 1
    scene.render.threads_mode = 'FIXED'
    scene.render.threads = 8
    # Pose controls are selected when opening; native custom properties work without code.
    for o in bpy.context.selected_objects:
        o.select_set(False)
    control.select_set(True)
    bpy.context.view_layer.objects.active = control
    for screen in bpy.data.screens:
        for area in screen.areas:
            if area.type == 'VIEW_3D':
                area.spaces.active.region_3d.view_perspective = 'CAMERA'
            if area.type == 'PROPERTIES':
                area.spaces.active.context = 'OBJECT'
    set_pose(control, POSES['working'])
    fit_camera(scene,(.70,-1.3,.62),margin=1.27)
    return scene, control


def validate(scene, controls, dims):
    """Check meaningful constraints in evaluated world geometry over five poses."""
    report = {'poses': {}, 'mesh_checks': {}, 'limitations': [
        'No simulation of friction torque, structural deflection, temperature or electrical safety.',
        'Five representative poses checked; the full Cartesian control range is not certified collision-free.',
        'The power path inside the arms and hollow pivots is represented by concealed routing, not internal wiring geometry.']}
    for name, pose in POSES.items():
        set_pose(controls, pose)
        dg = bpy.context.evaluated_depsgraph_get()
        p0 = bpy.data.objects['Pivot 1 · shoulder'].evaluated_get(dg)
        p1 = bpy.data.objects['Pivot 2 · elbow'].evaluated_get(dg)
        p2 = bpy.data.objects['Pivot 3 · head tilt'].evaluated_get(dg)
        q0,q1,q2 = [o.matrix_world.translation.copy() for o in (p0,p1,p2)]
        # Compare hierarchy positions with independent planar forward kinematics.
        a = math.radians(pose['shoulder_deg'])
        b = math.radians(pose['shoulder_deg']-pose['elbow_bend_deg'])
        yaw = math.radians(pose['yaw_deg'])
        planar = Vector((dims['lower_length']*math.cos(a)+dims['upper_length']*math.cos(b),0,
                         dims['shoulder_height']+dims['lower_length']*math.sin(a)+dims['upper_length']*math.sin(b)))
        expected = Vector((planar.x*math.cos(yaw),planar.x*math.sin(yaw),planar.z))
        error = (q2-expected).length
        lengths = [(q1-q0).length,(q2-q1).length]
        actual_axis = p2.matrix_world.to_3x3() @ Vector((1,0,0))
        pitch = math.radians(pose['head_pitch_deg'])
        expected_axis = Vector((math.cos(yaw)*math.cos(pitch),math.sin(yaw)*math.cos(pitch),math.sin(pitch)))
        pitch_error = (actual_axis-expected_axis).length
        minimum_z = float('inf')
        shade_points = []
        for o in bpy.data.collections['01 · LAMP | editable parts'].objects:
            if o.type != 'MESH':
                continue
            ev = o.evaluated_get(dg)
            me = ev.to_mesh()
            try:
                points = [ev.matrix_world @ v.co for v in me.vertices]
                assert all(math.isfinite(v) for p in points for v in p), o.name
                minimum_z = min(minimum_z,min(p.z for p in points))
                if o.name.startswith('Head ·'):
                    shade_points.extend(points)
            finally:
                ev.to_mesh_clear()
        head_clearance = min(p.z for p in shade_points)
        assert error < 1e-6, (name,error)
        assert pitch_error < 1e-6, (name,pitch_error)
        assert abs(lengths[0]-dims['lower_length']) < 1e-6
        assert abs(lengths[1]-dims['upper_length']) < 1e-6
        assert minimum_z > -1e-6, (name, minimum_z)
        assert head_clearance > .12, (name,head_clearance)
        report['poses'][name] = dict(pose=pose, lower_length_m=lengths[0],upper_length_m=lengths[1],
            wrist_error_m=error,head_axis_error=pitch_error,minimum_mesh_height_m=minimum_z,
            head_desk_clearance_m=head_clearance, wrist_world_m=list(q2))
    set_pose(controls,POSES['working'])
    manifold_bad = []
    inverted = []
    for o in bpy.data.collections['01 · LAMP | editable parts'].objects:
        if o.type != 'MESH':
            continue
        bm = bmesh.new()
        try:
            bm.from_mesh(o.data)
            if any(not e.is_manifold for e in bm.edges):
                manifold_bad.append(o.name)
            vol = bm.calc_volume(signed=True)
            if vol <= 0:
                inverted.append((o.name,vol))
        finally:
            bm.free()
    report['mesh_checks'] = dict(mesh_count=sum(o.type=='MESH' for o in bpy.data.collections['01 · LAMP | editable parts'].objects),
                                 non_manifold=manifold_bad,non_positive_signed_volume=inverted)
    assert not manifold_bad, manifold_bad
    assert not inverted, inverted
    drivers = [f for o in bpy.data.objects if o.animation_data for f in o.animation_data.drivers]
    assert len(drivers) == 4
    assert all(f.driver.is_valid for f in drivers)
    report['driver_count'] = len(drivers)
    return report


def render(scene, path, resolution, samples):
    if path.exists():
        raise FileExistsError(path)
    scene.render.filepath = str(path)
    scene.render.resolution_x = scene.render.resolution_y = resolution
    scene.cycles.samples = samples
    result = bpy.ops.render.render('EXEC_DEFAULT', write_still=True)
    assert result == {'FINISHED'}, result
    assert path.read_bytes()[:8] == b'\x89PNG\r\n\x1a\n'


def main():
    tail = sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
    p = argparse.ArgumentParser()
    p.add_argument('--output', required=True, type=Path)
    p.add_argument('--resolution', default=1200, type=int)
    p.add_argument('--samples', default=64, type=int)
    p.add_argument('--no-render', action='store_true')
    a = p.parse_args(tail)
    out = a.output.resolve()
    out.mkdir(parents=True, exist_ok=False)
    identity = dict(version=bpy.app.version_string,build_hash=bpy.app.build_hash.decode(),
                    python=sys.version,platform=platform.platform(),background=bpy.app.background)
    (out/'identity.json').write_text(json.dumps(identity,indent=2))
    assert bpy.app.version == EXPECTED_VERSION and identity['build_hash'] == EXPECTED_HASH, identity
    scene, control = build_scene(DIMENSIONS)
    report = validate(scene,control,DIMENSIONS)
    (out/'geometry-checks.json').write_text(json.dumps(report,indent=2))
    # Bundle source and read-me in native text datablocks as well as sidecar files.
    source_path = Path(__file__).resolve()
    source_text = source_path.read_text()
    (out/'build_lamp.py').write_text(source_text)
    bpy.data.texts.new('build_lamp.py').write(source_text)
    bpy.data.texts.new('START HERE.txt').write(
        'AXIS / 02\nSelect LAMP · ADJUST HERE and edit Object > Custom Properties.\n'
        'yaw_deg: turn the base. shoulder_deg: lower arm elevation.\n'
        'elbow_bend_deg: bend between arms. head_pitch_deg: absolute head angle.\n'
        'The head automatically compensates when the arm moves.\n'
        'No Python auto-run is needed: the four drivers use simple arithmetic.\n'
        'Dimensions and presets are in the bundled build_lamp.py and scene custom properties.\n'
        'Rebuilding intentionally creates a new scene. Preserve manual edits separately.\n')
    scene.render.resolution_x = scene.render.resolution_y = a.resolution
    scene.cycles.samples = a.samples
    scene.render.filepath = '//hero.png'
    blend_path = out/'axis-02.blend'
    assert not blend_path.exists()
    assert bpy.ops.wm.save_as_mainfile(filepath=str(blend_path),check_existing=False) == {'FINISHED'}
    if not a.no_render:
        render(scene,out/'hero.png',a.resolution,a.samples)
        # Side elevations deliberately reveal all hinge attachment relationships.
        cam = scene.camera
        for name in ('working','reach','upright','compact','turned'):
            set_pose(control,POSES[name])
            fit_camera(scene,(0,-1.,.15),margin=1.22)
            render(scene,out/('pose-'+name+'.png'),800,32)
        set_pose(control,POSES['working'])
        cam.location = (.55,-.9,.74)
        aim(cam,(.035,0,.352))
        cam.data.ortho_scale = .41
        render(scene,out/'joint-detail.png',1000,48)
    receipt = dict(identity=identity,source_sha256=hashlib.sha256(source_text.encode()).hexdigest(),
                   dimensions=DIMENSIONS,validation='geometry-checks.json',
                   files={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in out.iterdir() if f.is_file()})
    (out/'build-receipt.json').write_text(json.dumps(receipt,indent=2))
    print('AXIS02_BUILD_COMPLETE',out,flush=True)


if __name__ == '__main__':
    main()
