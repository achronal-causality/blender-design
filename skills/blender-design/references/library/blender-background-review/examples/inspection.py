# HISTORICAL SOURCE: use the release example for a fresh runnable demonstration.
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Julian Turner
"""UNEXECUTED Blender 5.2.2 inspection configuration. Syntax checked only.

Illustrative view for small geometry near the origin; caller must frame arbitrary
objects from evaluated bounds. Functions mutate only when explicitly called.
"""
from pathlib import Path
import bpy
from mathutils import Vector


def aim(obj, target):
    """Aim local -Z at world target with local Y as up; no parent/constraints."""
    direction = Vector(target) - obj.location
    if direction.length == 0:
        raise ValueError('Camera/light cannot aim at its own origin')
    obj.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()


def configure(scene, collection, geometry_object, png_path):
    """Fresh scene/owned IDs only. Repeated calls intentionally require cleanup policy."""
    png_path = Path(png_path)
    if not png_path.is_absolute():
        raise ValueError('PNG path must be absolute')
    mat = bpy.data.materials.new('InspectionGray')
    mat['review_owner'] = 'background-review-v1'
    nt = mat.node_tree
    if nt is None:
        raise RuntimeError('Expected 5.2 material node tree')
    nt.nodes.clear()
    bsdf = nt.nodes.new('ShaderNodeBsdfPrincipled')
    output = nt.nodes.new('ShaderNodeOutputMaterial')
    output.is_active_output = True
    for name, value in [('Base Color', (0.35, 0.35, 0.35, 1.0)), ('Metallic', 0.0),
                        ('Roughness', 0.65), ('Alpha', 1.0), ('Transmission Weight', 0.0),
                        ('Subsurface Weight', 0.0), ('Coat Weight', 0.0),
                        ('Sheen Weight', 0.0), ('Emission Strength', 0.0)]:
        bsdf.inputs[name].default_value = value
    nt.links.new(input=output.inputs['Surface'], output=bsdf.outputs['BSDF'])
    # This fresh-object recipe replaces material slots deliberately.
    geometry_object.data.materials.clear()
    geometry_object.data.materials.append(mat)
    for polygon in geometry_object.data.polygons:
        polygon.material_index = 0

    world = bpy.data.worlds.new('InspectionWorld')
    world['review_owner'] = 'background-review-v1'
    scene.world = world
    wn = world.node_tree
    if wn is None:
        raise RuntimeError('Expected 5.2 world node tree')
    wn.nodes.clear()
    background = wn.nodes.new('ShaderNodeBackground')
    background.inputs['Color'].default_value = (0.15, 0.15, 0.15, 1.0)
    background.inputs['Strength'].default_value = 0.3
    wo = wn.nodes.new('ShaderNodeOutputWorld')
    wo.is_active_output = True
    wn.links.new(input=wo.inputs['Surface'], output=background.outputs['Background'])

    camera_data = bpy.data.cameras.new('InspectionCamera')
    camera_data.type = 'ORTHO'
    camera_data.ortho_scale = 5.0
    camera_data.clip_start, camera_data.clip_end = 0.01, 100.0
    camera_data.dof.use_dof = False
    camera = bpy.data.objects.new('InspectionCamera', camera_data)
    collection.objects.link(camera)
    camera.location = (4.0, -6.0, 4.0)
    aim(camera, (0.0, 0.0, 0.0))
    scene.camera = camera

    light_data = bpy.data.lights.new('InspectionKey', type='AREA')
    light_data.energy = 500.0
    light_data.normalize = True
    light_data.shape = 'DISK'
    light_data.size = 4.0
    light = bpy.data.objects.new('InspectionKey', light_data)
    collection.objects.link(light)
    light.location = (3.0, -4.0, 5.0)
    aim(light, (0.0, 0.0, 0.0))

    scene.render.engine = 'CYCLES'
    scene.cycles.device = 'CPU'
    scene.cycles.samples = 64
    scene.cycles.seed = 0
    scene.cycles.use_animated_seed = False
    scene.cycles.use_adaptive_sampling = False
    scene.cycles.use_denoising = False
    scene.render.resolution_x = scene.render.resolution_y = 768
    scene.render.resolution_percentage = 100
    scene.render.pixel_aspect_x = scene.render.pixel_aspect_y = 1.0
    for name in ('use_border', 'use_crop_to_border', 'use_sequencer', 'use_compositing',
                 'use_simplify', 'use_motion_blur', 'film_transparent'):
        setattr(scene.render, name, False)
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGBA'
    scene.render.image_settings.color_depth = '8'
    scene.render.image_settings.compression = 15
    scene.render.image_settings.color_management = 'FOLLOW_SCENE'
    scene.render.use_file_extension = True
    scene.render.filepath = str(png_path)
    scene.display_settings.display_device = 'sRGB'
    scene.view_settings.view_transform = 'AgX'
    scene.view_settings.look = 'NONE'  # Documented 5.2 identifier; fail if effective OCIO differs.
    scene.view_settings.exposure = 0.0
    scene.view_settings.gamma = 1.0
    scene.view_settings.use_curve_mapping = False
    return camera, light, mat, world
