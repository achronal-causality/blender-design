# HISTORICAL SOURCE: use the release example for a fresh runnable demonstration.
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Julian Turner
"""UNEXECUTED Blender 5.2.2 Geometry Nodes example. Syntax checked only.

Caller supplies an original local mesh Object and owns any resulting IDs.
This demonstrates the graph program; it does not claim observed mesh counts.
"""
import math
import bpy


def socket_by_id(sockets, identifier):
    matches = [s for s in sockets if s.identifier == identifier]
    if len(matches) != 1:
        raise RuntimeError(f'Expected one socket {identifier!r}, got {len(matches)}')
    return matches[0]


def instance_graph(obj, count=5, spacing=1.0):
    if type(count) is not int or not 2 <= count <= 100:
        raise ValueError('This bounded example requires an integer count from 2 to 100')
    if not math.isfinite(spacing) or spacing <= 0:
        raise ValueError('spacing must be finite and positive')
    if obj.modifiers.get('Procedure') is not None:
        raise RuntimeError('Procedure already exists; choose a revision policy')
    tree = bpy.data.node_groups.new('RepeatedBlocks', 'GeometryNodeTree')
    tree.is_modifier = True  # Declare intended modifier usage on the concrete tree type.
    tree['review_owner'] = 'background-review-v1'
    tree.interface.new_socket(name='Geometry', in_out='INPUT',
                              socket_type='NodeSocketGeometry')
    out_interface = tree.interface.new_socket(name='Geometry', in_out='OUTPUT',
                                              socket_type='NodeSocketGeometry')
    spacing_interface = tree.interface.new_socket(name='Spacing', in_out='INPUT',
                                                  socket_type='NodeSocketFloat')
    spacing_interface.default_value = spacing
    group_in = tree.nodes.new('NodeGroupInput')
    group_out = tree.nodes.new('NodeGroupOutput')
    group_out.is_active_output = True
    line = tree.nodes.new('GeometryNodeMeshLine')
    line.mode = 'OFFSET'
    socket_by_id(line.inputs, 'Count').default_value = count
    scale = tree.nodes.new('ShaderNodeVectorMath')
    scale.operation = 'SCALE'
    socket_by_id(scale.inputs, 'Vector').default_value = (1.0, 0.0, 0.0)
    cube = tree.nodes.new('GeometryNodeMeshCube')
    socket_by_id(cube.inputs, 'Size').default_value = (0.35, 0.35, 0.35)
    for identifier in ('Vertices X', 'Vertices Y', 'Vertices Z'):
        socket_by_id(cube.inputs, identifier).default_value = 2
    instances = tree.nodes.new('GeometryNodeInstanceOnPoints')
    realize = tree.nodes.new('GeometryNodeRealizeInstances')
    socket_by_id(realize.inputs, 'Realize All').default_value = True
    # Keyword directions match NodeLinks.new's public parameter names.
    def link(source, source_id, target, target_id):
        result = tree.links.new(output=socket_by_id(source.outputs, source_id),
                                input=socket_by_id(target.inputs, target_id))
        if result is None:
            raise RuntimeError('Link construction failed')
    link(group_in, spacing_interface.identifier, scale, 'Scale')
    link(scale, 'Vector', line, 'Offset')
    link(line, 'Mesh', instances, 'Points')
    link(cube, 'Mesh', instances, 'Instance')
    link(instances, 'Instances', realize, 'Geometry')
    link(realize, 'Geometry', group_out, out_interface.identifier)
    modifier = obj.modifiers.new('Procedure', 'NODES')
    modifier.node_group = tree
    parameters = getattr(modifier.properties.inputs, spacing_interface.identifier)
    parameters.type = 'VALUE'
    parameters.value = spacing
    # Record semantic mapping; never infer a socket identifier from its ordinal position.
    obj['spacing_socket_identifier'] = spacing_interface.identifier
    return modifier, tree
