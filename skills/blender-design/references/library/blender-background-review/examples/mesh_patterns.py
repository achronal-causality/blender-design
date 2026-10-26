# HISTORICAL SOURCE: use the release example for a fresh runnable demonstration.
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Julian Turner
"""UNEXECUTED reference functions for Blender 5.2.2. Syntax checked only.

Importing this file defines functions; it does not construct a scene.
Caller owns the destination Collection and chooses a fresh build or revision.
"""
import math
import bpy
import bmesh

OWNER = 'background-review-v1'  # Application metadata, not a Blender security boundary.


def new_collection(scene, name='Procedure'):
    """Fresh-build only: create/link a Collection ID; return that ID."""
    collection = bpy.data.collections.new(name)
    collection['review_owner'] = OWNER
    scene.collection.children.link(collection)
    return collection


def box_mesh(size):
    """Return a new original Mesh. size=(x,y,z) local full extents, all positive.

    This allocates in Main but creates no Object. A validation repair is failure.
    Geometry is a boundary mesh, not a volumetric CAD/manufacturing certificate.
    """
    if len(size) != 3 or not all(math.isfinite(v) and v > 0 for v in size):
        raise ValueError('size must contain three finite positive lengths')
    x, y, z = (v / 2 for v in size)
    verts = [(-x, -y, -z), (x, -y, -z), (x, y, -z), (-x, y, -z),
             (-x, -y, z), (x, -y, z), (x, y, z), (-x, y, z)]
    faces = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4),
             (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    mesh = bpy.data.meshes.new('BodyMesh')
    mesh['review_owner'] = OWNER
    try:
        mesh.from_pydata(verts, [], faces, shade_flat=True)
        if mesh.validate(verbose=True):
            raise ValueError('box topology required repair')
        mesh.update(calc_edges=True)
        return mesh
    except Exception:
        if mesh.users == 0:
            bpy.data.meshes.remove(mesh)
        raise


def replace_body(collection, size):
    """Rebuild one owned body; reject ambiguous or shared/uneditable input.

    Preserves the Object's transform/modifier stack. Mesh replacement discards
    prior intrinsic geometry/material slots; use only when that is intended.
    Does not claim transactionality after the candidate is assigned.
    """
    hits = [o for o in collection.objects
            if o.get('review_owner') == OWNER and o.get('part_key') == 'body']
    if len(hits) > 1:
        raise RuntimeError('Ambiguous owned part: body')
    obj = hits[0] if hits else None
    if obj and (obj.type != 'MESH' or not obj.is_editable or obj.mode != 'OBJECT'
                or obj.data.users != 1 or obj.data.get('review_owner') != OWNER):
        raise RuntimeError('Expected independent owned local Object Mode mesh')
    candidate = box_mesh(size)
    old = None
    try:
        if obj is None:
            obj = bpy.data.objects.new('Body', candidate)
            obj['review_owner'] = OWNER
            obj['part_key'] = 'body'
            collection.objects.link(obj)
        else:
            old = obj.data
            obj.data = candidate
        obj['size_parameters'] = list(size)
        bpy.context.view_layer.update()
    except Exception:
        # Keep any linked/assigned candidate as failure evidence; no broad purge.
        if candidate.users == 0:
            bpy.data.meshes.remove(candidate)
        raise
    # Application-specific evaluated acceptance belongs before deleting `old`.
    # This reference intentionally retains it for possible recovery.
    return obj, old


def extrude_top(mesh, height):
    """Object Mode mesh only; deliberately choose all upward-facing faces.

    Region eligibility is example-specific. Caller must choose a stricter region
    predicate for other shapes. Write-back changes the supplied Mesh and all users.
    """
    if mesh.is_editmode or not math.isfinite(height) or height <= 0:
        raise ValueError('Expected Object Mode mesh and finite positive height')
    bm = bmesh.new(use_operators=True)
    try:
        bm.from_mesh(mesh)
        bm.normal_update()
        faces = [f for f in bm.faces if f.normal.z > 0.999]
        if not faces:
            raise ValueError('No upward region found')
        result = bmesh.ops.extrude_face_region(bm, geom=faces)
        new_verts = [g for g in result['geom'] if isinstance(g, bmesh.types.BMVert)]
        bmesh.ops.translate(bm, verts=new_verts, vec=(0.0, 0.0, height))
        bm.normal_update()
        bm.to_mesh(mesh)
    finally:
        bm.free()
    if mesh.validate(verbose=True):
        raise ValueError('Extrusion produced geometry requiring repair')
    mesh.update()


def copy_object(obj, collection, part_key, independent_geometry):
    """Copy Object, optionally Mesh, but retain shared referenced Materials."""
    copy = obj.copy()
    copy['part_key'] = part_key  # Never leave the source semantic key on a new part.
    if independent_geometry:
        copy.data = obj.data.copy()
    collection.objects.link(copy)
    return copy


def curve_object(collection):
    """Fresh-build example: three-point 3D polyline, beveled and capped."""
    data = bpy.data.curves.new('BentPath', type='CURVE')
    data['review_owner'] = OWNER
    data.dimensions = '3D'
    data.resolution_u = data.render_resolution_u = 12
    data.bevel_depth = 0.05
    data.bevel_resolution = 3
    data.use_fill_caps = True
    spline = data.splines.new('POLY')
    points = [(0, 0, 0), (1, 0, 0.5), (1.5, 1, 0.5)]
    spline.points.add(len(points) - 1)
    for p, xyz in zip(spline.points, points):
        p.co = (*xyz, 1.0)
    obj = bpy.data.objects.new('BentPath', data)
    obj['review_owner'] = OWNER
    obj['part_key'] = 'path'
    collection.objects.link(obj)
    return obj


def add_bevel(obj):
    """Fresh-construction fragment; reject duplicate modifier name on rerun."""
    if obj.modifiers.get('EdgeRound') is not None:
        raise RuntimeError('EdgeRound already exists; revise it explicitly')
    modifier = obj.modifiers.new('EdgeRound', 'BEVEL')
    modifier.width = 0.03
    modifier.segments = 3
    modifier.limit_method = 'ANGLE'
    modifier.angle_limit = math.radians(30)
    modifier.use_clamp_overlap = True
    return modifier
