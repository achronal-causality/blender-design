# HISTORICAL SOURCE: use the release example for a fresh runnable demonstration.
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Julian Turner
"""UNEXECUTED save/render/export and numeric-inspection patterns.

Not a production validator. Caller must supply an exclusively owned fresh directory,
expected geometry, source/parameter provenance and a later reopen/visual check.
"""
from pathlib import Path
import hashlib
import json
import struct
import bpy


def mesh_summary(obj):
    """Copy scalar counts and world bounds; requires realized mesh component."""
    dg = bpy.context.evaluated_depsgraph_get()
    evaluated = obj.evaluated_get(dg)
    mesh = evaluated.to_mesh(preserve_all_data_layers=True, depsgraph=dg)
    try:
        if mesh is None or len(mesh.vertices) == 0:
            raise ValueError('Expected nonempty evaluated mesh')
        matrix = evaluated.matrix_world.copy()
        points = [tuple(matrix @ v.co) for v in mesh.vertices]
        return {'vertices': len(points), 'edges': len(mesh.edges),
                'polygons': len(mesh.polygons),
                'min_world': [min(p[i] for p in points) for i in range(3)],
                'max_world': [max(p[i] for p in points) for i in range(3)]}
    finally:
        evaluated.to_mesh_clear()


def save_render_export(root, collection_name, obj, provenance):
    """Write named outputs and a completion claim last; fail on missing artifacts.

    `provenance` is caller-provided JSON-compatible source/parameter/input metadata.
    The receipt remains a script claim pending host digest/reopen/visual validation.
    """
    root = Path(root).resolve()
    paths = {k: root / n for k, n in [('blend', 'scene.blend'),
             ('png', 'inspection.png'), ('obj', 'geometry.obj'), ('mtl', 'geometry.mtl')]}
    receipt = root / 'complete.json'
    if not root.is_dir() or any(p.exists() for p in [*paths.values(), receipt]):
        raise RuntimeError('Expected existing fresh output directory')
    if bpy.app.version != (5, 2, 2) or not bpy.app.build_hash.decode().startswith('d13f752e3b9c'):
        raise RuntimeError('Blender baseline drift')
    bpy.context.scene.render.filepath = str(paths['png'])
    summary = mesh_summary(obj)
    result = bpy.ops.wm.save_as_mainfile('EXEC_DEFAULT', filepath=str(paths['blend']),
                check_existing=False, compress=False, relative_remap=True, copy=False)
    if result != {'FINISHED'}:
        raise RuntimeError(f'Save status: {result}')
    result = bpy.ops.render.render('EXEC_DEFAULT', animation=False, write_still=True)
    if result != {'FINISHED'}:
        raise RuntimeError(f'Render status: {result}')
    result = bpy.ops.wm.obj_export('EXEC_DEFAULT', filepath=str(paths['obj']),
                collection=collection_name, export_selected_objects=False,
                export_animation=False, apply_modifiers=True, apply_transform=True,
                export_eval_mode='DAG_EVAL_RENDER', forward_axis='NEGATIVE_Z', up_axis='Y',
                global_scale=1.0, export_uv=True, export_normals=True,
                export_materials=True, export_triangulated_mesh=False,
                export_curves_as_nurbs=False)
    if result != {'FINISHED'}:
        raise RuntimeError(f'Export status: {result}')
    for p in paths.values():
        if not p.is_file() or p.stat().st_size == 0:
            raise RuntimeError(f'Missing or empty output: {p.name}')
    png = paths['png'].read_bytes()
    if len(png) < 24 or png[:8] != b'\x89PNG\r\n\x1a\n' or png[12:16] != b'IHDR':
        raise RuntimeError('PNG header missing')
    width, height = struct.unpack('>II', png[16:24])
    if (width, height) != (768, 768):
        raise RuntimeError('Unexpected image dimensions for inspection recipe')
    # Header-only: this does not decode pixels, verify all PNG CRCs or judge the image.
    obj_text = paths['obj'].read_text(encoding='utf-8')
    if not any(line.startswith('v ') for line in obj_text.splitlines()):
        raise RuntimeError('OBJ has no vertex records')
    # This example requests materials; require the conventional MTL sidecar too.
    mtl = paths['mtl']
    if not mtl.is_file() or mtl.stat().st_size == 0:
        raise RuntimeError('Expected MTL sidecar missing')
    payload = {'status': 'script-complete-unverified', 'blender': bpy.app.version_string,
               'build_hash': bpy.app.build_hash.decode(), 'provenance': provenance,
               'summary': summary, 'outputs': {
                   key: {'name': p.name, 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
                   for key, p in paths.items()}}
    with receipt.open('x', encoding='utf-8') as stream:
        json.dump(payload, stream, indent=2)
    return payload
