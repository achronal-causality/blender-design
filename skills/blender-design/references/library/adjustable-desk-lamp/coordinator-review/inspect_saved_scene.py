# HISTORICAL SOURCE: use the release example for a fresh runnable demonstration.
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Julian Turner
"""Independent readback of the AXIS / 02 candidate; never saves the scene."""
import hashlib
import json
import math
import sys
from pathlib import Path
import bpy
from mathutils import Vector


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


target = Path(sys.argv[sys.argv.index('--') + 1]).resolve()
require(not target.exists(), 'Refusing to reuse an inspection receipt')
require(bpy.app.version == (5, 2, 2), 'Unexpected Blender version')
require(bpy.app.build_hash.decode() == 'd13f752e3b9c', 'Unexpected build hash')
scene = bpy.context.scene
require(scene.camera is not None, 'Saved scene has no camera')
require(scene.render.engine == 'CYCLES' and scene.cycles.device == 'CPU', 'Unexpected renderer')
ctl = bpy.data.objects['LAMP · ADJUST HERE']
dimensions = json.loads(scene['dimensions_json'])
parts = bpy.data.collections['01 · LAMP | editable parts']
joints = [bpy.data.objects[name] for name in (
    'Pivot 1 · shoulder', 'Pivot 2 · elbow', 'Pivot 3 · head tilt')]
pose_keys = ('yaw_deg', 'shoulder_deg', 'elbow_bend_deg', 'head_pitch_deg')
initial_values = {key: float(ctl[key]) for key in pose_keys}
counts_before = {key: len(getattr(bpy.data, key)) for key in ('objects', 'meshes', 'materials')}
drivers = [fc for obj in bpy.data.objects if obj.animation_data for fc in obj.animation_data.drivers]
require(len(drivers) == 4, 'Expected four adjustment drivers')
require(not bpy.app.autoexec_fail, 'Saved scene requires blocked Python auto-execution')
require(not bpy.data.libraries, 'Unexpected external linked library')
external_images = [im.filepath for im in bpy.data.images if im.source == 'FILE' and not im.packed_file]
require(not external_images, 'Unpacked external image dependency')
source_text = bpy.data.texts['build_lamp.py'].as_string()
require(bool(bpy.data.texts['START HERE.txt'].as_string()), 'Missing embedded instructions')
tests = [('saved', initial_values),
         ('independent_asymmetric', dict(zip(pose_keys, (37., 99., 73., 7.)))),
         ('independent_counterturned', dict(zip(pose_keys, (-62., 118., 91., -12.))))]
results = []
try:
    for name, values in tests:
        for key, value in values.items():
            ctl[key] = value
        ctl.update_tag()
        bpy.context.view_layer.update()
        graph = bpy.context.evaluated_depsgraph_get()
        evaluated = [obj.evaluated_get(graph) for obj in joints]
        centers = [obj.matrix_world.translation.copy() for obj in evaluated]
        lengths = [(centers[i+1]-centers[i]).length for i in (0, 1)]
        require(abs(lengths[0]-dimensions['lower_length']) < 1e-6, 'Lower arm length changed')
        require(abs(lengths[1]-dimensions['upper_length']) < 1e-6, 'Upper arm length changed')
        yaw, shoulder, bend, pitch = [math.radians(values[key]) for key in pose_keys]
        # Independently derive each endpoint from the semantic angle convention.
        radial = Vector((math.cos(yaw), math.sin(yaw), 0))
        vertical = Vector((0, 0, 1))
        base = Vector((0, 0, dimensions['shoulder_height']))
        elbow = base + dimensions['lower_length'] * (math.cos(shoulder)*radial + math.sin(shoulder)*vertical)
        wrist = elbow + dimensions['upper_length'] * (math.cos(shoulder-bend)*radial + math.sin(shoulder-bend)*vertical)
        position_error = max((centers[0]-base).length, (centers[1]-elbow).length, (centers[2]-wrist).length)
        expected_head_axis = math.cos(pitch)*radial + math.sin(pitch)*vertical
        head_axis = evaluated[2].matrix_world.to_3x3() @ Vector((1, 0, 0))
        axis_error = (head_axis-expected_head_axis).length
        require(position_error < 1e-6 and axis_error < 1e-6, 'Adjustment violates joint/head relationship')
        require(all(fc.driver.is_valid for fc in drivers), 'Invalid driver after adjustment')
        points = []
        for obj in parts.objects:
            if obj.type != 'MESH':
                continue
            eo = obj.evaluated_get(graph)
            mesh = eo.to_mesh()
            try:
                require(mesh is not None and len(mesh.vertices) > 0, 'Empty evaluated mesh: '+obj.name)
                for vertex in mesh.vertices:
                    p = eo.matrix_world @ vertex.co
                    require(all(math.isfinite(float(v)) for v in p), 'Nonfinite evaluated coordinate')
                    points.append(tuple(p))
            finally:
                eo.to_mesh_clear()
        require(min(p[2] for p in points) >= -1e-6, 'Lamp mesh penetrates desk plane')
        results.append(dict(name=name, values=values, segment_lengths_m=lengths,
                            maximum_joint_position_error_m=position_error, head_axis_error=axis_error,
                            wrist_world_m=list(centers[2]), evaluated_vertex_count=len(points)))
finally:
    for key, value in initial_values.items():
        ctl[key] = value
    ctl.update_tag()
    bpy.context.view_layer.update()
counts_after = {key: len(getattr(bpy.data, key)) for key in counts_before}
require(counts_before == counts_after, 'Pose adjustment changed datablock counts')
payload = dict(status='PASS', scene_file=bpy.data.filepath, blender=bpy.app.version_string,
               build_hash=bpy.app.build_hash.decode(), controls=initial_values, counts=counts_after,
               embedded_source_sha256=hashlib.sha256(source_text.encode()).hexdigest(),
               tests=results, external_images=external_images, autoexec_fail=bpy.app.autoexec_fail,
               scene_saved_by_this_check=False,
               limits=['No friction/load/thermal/electrical certification',
                       'Pose checks do not prove the entire control range collision-free'])
with target.open('x', encoding='utf-8') as stream:
    json.dump(payload, stream, indent=2)
print('AXIS02_INDEPENDENT_INSPECTION_PASS', target, flush=True)
