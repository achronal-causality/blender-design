# Consequential claim ledger

Each claim states its scope, documentation and pinned implementation, relevant reported experience, and what remains to test. **D** documented, **S** source-derived, **R** reported, **I** inference/recommended policy. No entry is a runtime capability result. Exact capture hashes/times and reading dispositions are in [coverage](coverage.json).

## C01

Background startup is a multipass application lifecycle; final actions run before background exit. Put script failure policy before the script and load input before mutation.

- **Documentation:** [bpy.app.html](../../../../../docs/research-catalog.md#file-b46df65444a74d34), [info_tips_and_tricks.rst](../../../../../docs/research-catalog.md#file-680ed8f0b5fcc47c).
- **Pinned source:** [creator:481 - 671](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/creator/creator.cc#L481-L671), [creator_args:2690 - 2897](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/creator/creator_args.cc#L2690-L2897).
- **Reported experience:** [R99755](EXPERIENCE.md#r99755).
- **Classification and limit:** D/S control flow; I command ordering policy. Exact observed return/status paths remain T01.

## C02

A fresh process resets in-memory Blender/Python state but not filesystem resources or ambient environment. Factory startup does not create an OS sandbox.

- **Documentation:** [info_overview.rst](../../../../../docs/research-catalog.md#file-225123b30a7f798e), [info_gotchas_file_paths_and_encoding.rst](../../../../../docs/research-catalog.md#file-06ed6ac8670ac587).
- **Pinned source:** [bpy_interface:368 - 597](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/python/intern/bpy_interface.cc#L368-L597), [wm_files:1323 - 1364](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/windowmanager/intern/wm_files.cc#L1323-L1364).
- **Reported experience:** [R72807](EXPERIENCE.md#r72807).
- **Classification and limit:** D/S mechanism; I isolation boundary. Relevant environment must be recorded, not assumed absent.

## C03

Use the Blender executable for embedded bpy, explicit absolute paths, and bundled-compatible dependencies. Python globals/import cache and .blend-relative paths are different namespaces.

- **Documentation:** [bpy.path.html](../../../../../docs/research-catalog.md#file-545d81dcc0e38ec0), [info_gotchas_threading.rst](../../../../../docs/research-catalog.md#file-dbecb96be2828f41).
- **Pinned source:** [py_capi_utils:1256 - 1271](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/python/generic/py_capi_utils.cc#L1256-L1271), [bpy_interface:368 - 597](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/python/intern/bpy_interface.cc#L368-L597).
- **Reported experience:** [R72807](EXPERIENCE.md#r72807), [R129657](EXPERIENCE.md#r129657).
- **Classification and limit:** D/S; no standalone bpy installation. Runtime import mismatches are diagnosed before adding packages.

## C04

Objects reference data, Collections link Objects, Scenes root collection hierarchies and ViewLayers filter them. A Python wrapper does not own an ID.

- **Documentation:** [api-ID.html](../../../../../docs/research-catalog.md#file-9ad9be19064ee9a5), [api-Object.html](../../../../../docs/research-catalog.md#file-d566af89da2d9296), [api-Collection.html](../../../../../docs/research-catalog.md#file-7d7604b22e5441d0).
- **Pinned source:** [rna_main_api:246 - 298](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/makesrna/intern/rna_main_api.cc#L246-L298), [rna_collection:134 - 178](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/makesrna/intern/rna_collection.cc#L134-L178).
- **Reported experience:** No selected firsthand report independently establishes this claim.
- **Classification and limit:** D/S; a valid ID can remain outside the active scene. T03/T06 verify intended membership.

## C05

Object.copy does not recursively clone mesh/material/node-group dependencies. Decide each layer of sharing explicitly.

- **Documentation:** [api-ID.html](../../../../../docs/research-catalog.md#file-9ad9be19064ee9a5), [api-Object.html](../../../../../docs/research-catalog.md#file-d566af89da2d9296).
- **Pinned source:** [rna_ID:757 - 782](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/makesrna/intern/rna_ID.cc#L757-L782), [lib_id:851 - 876](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/blenkernel/intern/lib_id.cc#L851-L876).
- **Reported experience:** No selected firsthand report independently establishes this claim.
- **Classification and limit:** D contract; S copy delegation/remapping; I explicit sharing policy. T03 must compare actual users and changes.

## C06

Deleting mesh data with unlinking may also delete never-null Object users. Remove the intended Object first and clean only owned zero-user data; never use user_clear as routine cleanup.

- **Documentation:** [api-BlendDataMeshes.html](../../../../../docs/research-catalog.md#file-763c1ec3cc36d59e), [api-ID.html](../../../../../docs/research-catalog.md#file-9ad9be19064ee9a5), [info_gotchas_internal_data_and_python_objects.rst](../../../../../docs/research-catalog.md#file-43c072a122e05dc0).
- **Pinned source:** [rna_main_api:115 - 172](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/makesrna/intern/rna_main_api.cc#L115-L172), [lib_id_delete:259 - 362](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/blenkernel/intern/lib_id_delete.cc#L259-L362).
- **Reported experience:** No selected firsthand report independently establishes this claim.
- **Classification and limit:** D/S removal cascade; I conservative cleanup. T02/T03 must preserve unrelated IDs.

## C07

Operator context and temporary overrides have real preconditions. EXEC_DEFAULT is the synchronous reference; override restoration is not scene rollback or fabrication of UI state.

- **Documentation:** [api-Context.html](../../../../../docs/research-catalog.md#file-56c5733c108e652c), [info_gotchas_operators.rst](../../../../../docs/research-catalog.md#file-2f168c4fdf484e6d).
- **Pinned source:** [bpy_operator_function:115 - 435](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/python/intern/bpy_operator_function.cc#L115-L435), [bpy_rna_context:180 - 520](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/python/intern/bpy_rna_context.cc#L180-L520), [wm_event_system:2002 - 2024](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/windowmanager/intern/wm_event_system.cc#L2002-L2024).
- **Reported experience:** [R6101](EXPERIENCE.md#r6101), [R119202](EXPERIENCE.md#r119202).
- **Classification and limit:** D/S dispatch and context; I avoid modal/UI dependencies. T04 tests the bounded operator setup.

## C08

Object.evaluated_get is lookup, not refresh. Establish evaluation after edits and reacquire evaluated references after updates.

- **Documentation:** [api-ID.html](../../../../../docs/research-catalog.md#file-9ad9be19064ee9a5), [api-Depsgraph.html](../../../../../docs/research-catalog.md#file-ee183c213eefe2a2), [api-Context.html](../../../../../docs/research-catalog.md#file-56c5733c108e652c).
- **Pinned source:** [rna_ID:757 - 782](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/makesrna/intern/rna_ID.cc#L757-L782), [context:1752 - 1762](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/blenkernel/intern/context.cc#L1752-L1762), [scene:2749 - 2835](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/blenkernel/intern/scene.cc#L2749-L2835).
- **Reported experience:** [R323805](EXPERIENCE.md#r323805).
- **Classification and limit:** D/S; a writable ordinary script context is assumed. T05 checks graph mode and refresh.

## C09

to_mesh data is temporary and tied to its Object; repeated conversion clears the old result. new_from_object creates Main data and removes anonymous attributes.

- **Documentation:** [api-Object.html](../../../../../docs/research-catalog.md#file-d566af89da2d9296), [api-BlendDataMeshes.html](../../../../../docs/research-catalog.md#file-763c1ec3cc36d59e).
- **Pinned source:** [rna_object_api:426 - 451](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/makesrna/intern/rna_object_api.cc#L426-L451), [object:5601 - 5622](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/blenkernel/intern/object.cc#L5601-L5622), [mesh_convert:860 - 1055](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/blenkernel/intern/mesh_convert.cc#L860-L1055).
- **Reported experience:** [R96721](EXPERIENCE.md#r96721).
- **Classification and limit:** D/S; unsupported-type documentation inconsistency resolved by RNA guard. T05/T06 cover empty results/layers/cleanup.

## C10

Mesh arrays and BMesh connectivity are different representations. Own/free bmesh.new; borrow/update from_edit_mesh without freeing Blender data.

- **Documentation:** [bmesh.html](../../../../../docs/research-catalog.md#file-cb40ce9c39bbd834), [bmesh.types.html](../../../../../docs/research-catalog.md#file-8029d1f8e77a2194), [info_gotchas_meshes.rst](../../../../../docs/research-catalog.md#file-88e9c31e75513541).
- **Pinned source:** [bmesh_py_api:38 - 161](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/python/bmesh/bmesh_py_api.cc#L38-L161), [bmesh_py_types:1319 - 1408](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/python/bmesh/bmesh_py_types.cc#L1319-L1408).
- **Reported experience:** [R105715](EXPERIENCE.md#r105715).
- **Classification and limit:** D/S ownership. T07 checks documented mode and write-back paths, without deliberately dereferencing freed data.

## C11

Mesh.validate returning True means repair occurred; storage validation does not establish watertightness or self-intersection-free geometry.

- **Documentation:** [api-Mesh.html](../../../../../docs/research-catalog.md#file-2e4b0dfc3ae778b2).
- **Pinned source:** [rna_mesh_api:198 - 258](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/makesrna/intern/rna_mesh_api.cc#L198-L258), [mesh_validate:852 - 951](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/blenkernel/intern/mesh_validate.cc#L852-L951).
- **Reported experience:** No selected firsthand report independently establishes this claim.
- **Classification and limit:** D/S return contract; I reject unexpected repair. Numerical/geometric certification excluded; T07.

## C12

Corner attributes/normals and smoothing affect appearance separately from topology. Copy transient numeric values and verify domain/type/length before bulk access.

- **Documentation:** [api-Mesh.html](../../../../../docs/research-catalog.md#file-2e4b0dfc3ae778b2), [api-Attribute.html](../../../../../docs/research-catalog.md#file-51623e7350d2b50f), [api-AttributeGroupMesh.html](../../../../../docs/research-catalog.md#file-2dcfd661b1255282).
- **Pinned source:** [rna_mesh:400 - 474](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/makesrna/intern/rna_mesh.cc#L400-L474), [rna_mesh:1686 - 1786](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/makesrna/intern/rna_mesh.cc#L1686-L1786).
- **Reported experience:** [R144340](EXPERIENCE.md#r144340).
- **Classification and limit:** D/S representation; no blanket claim that custom normals are safe for every modifier path. T07.

## C13

BMesh operations mutate before error conversion; extrusion needs explicit displacement, bevel affects eligible geometry and normalizes some parameters.

- **Documentation:** [bmesh.ops.html](../../../../../docs/research-catalog.md#file-06186a240325b796).
- **Pinned source:** [bmesh_py_ops_call:760 - 870](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/python/bmesh/bmesh_py_ops_call.cc#L760-L870), [bmo_extrude:319 - 632](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/bmesh/operators/bmo_extrude.cc#L319-L632), [bmo_bevel:1 - 96](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/bmesh/operators/bmo_bevel.cc#L1-L96), [bmesh_bevel:8239 - 8322](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/bmesh/tools/bmesh_bevel.cc#L8239-L8322).
- **Reported experience:** No selected firsthand report independently establishes this claim.
- **Classification and limit:** D/S selected control flow; not a full bevel/intersection kernel audit. T02/T07.

## C14

Points, directions and normals use different affine transforms; singular and nonuniform parent transforms require explicit handling.

- **Documentation:** [mathutils.html](../../../../../docs/research-catalog.md#file-debdcad6d02325f9), [api-Object.html](../../../../../docs/research-catalog.md#file-d566af89da2d9296).
- **Pinned source:** [mesh_mirror:118 - 200](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/blenkernel/intern/mesh_mirror.cc#L118-L200), [obj_export_mesh:149 - 176](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/io/wavefront_obj/exporter/obj_export_mesh.cc#L149-L176).
- **Reported experience:** No selected firsthand report independently establishes this claim.
- **Classification and limit:** D plus standard affine algebra; S selected production use. Arbitrary shear/TRS roundtrip is not guaranteed; T07.

## C15

Object.dimensions assignment uses cached bounds to change scale. It is not intrinsic geometry redesign or world-axis-aligned size.

- **Documentation:** [api-Object.html](../../../../../docs/research-catalog.md#file-d566af89da2d9296).
- **Pinned source:** [rna_object:1217 - 1232](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/makesrna/intern/rna_object.cc#L1217-L1232), [object:3763 - 3807](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/blenkernel/intern/object.cc#L3763-L3807).
- **Reported experience:** No selected firsthand report independently establishes this claim.
- **Classification and limit:** D/S; zero axes and repeated assignments need explicit evaluation/measurement. T05/T07.

## C16

Modifier order and viewport/render settings are part of procedural output. Applying a non-first modifier is not a full-stack bake; verify stack/output after the operator.

- **Documentation:** [api-Modifier.html](../../../../../docs/research-catalog.md#file-986972b03854e62e), [api-SubsurfModifier.html](../../../../../docs/research-catalog.md#file-902d576757b680c8).
- **Pinned source:** [object_modifier:1257 - 1345](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/editors/object/object_modifier.cc#L1257-L1345), [object_modifier:1991 - 2078](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/editors/object/object_modifier.cc#L1991-L2078), [MOD_subsurf:192 - 278](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/modifiers/intern/MOD_subsurf.cc#L192-L278).
- **Reported experience:** No selected firsthand report independently establishes this claim.
- **Classification and limit:** D/S; apply can retain failure evidence and delayed subdivision needs materialization. T04/T05/T07.

## C17

Node interfaces, internal sockets and per-modifier values are separate. Linking can remove prior links when limits are enforced.

- **Documentation:** [api-NodeTreeInterface.html](../../../../../docs/research-catalog.md#file-2e3ce82a211c20ae), [api-NodeLinks.html](../../../../../docs/research-catalog.md#file-ffb3e96911fd640c).
- **Pinned source:** [rna_node_tree_interface:729 - 774](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/makesrna/intern/rna_node_tree_interface.cc#L729-L774), [rna_nodetree:1425 - 1532](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/makesrna/intern/rna_nodetree.cc#L1425-L1532), [node_common:964 - 1032](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/nodes/intern/node_common.cc#L964-L1032).
- **Reported experience:** No selected firsthand report independently establishes this claim.
- **Classification and limit:** D/S; identifiers must survive deliberate revision. T10 verifies schema changes.

## C18

Blender 5.2 consumes typed modifier inputs under properties.inputs.<interface identifier>.value or supported attribute fields. Legacy ID-property writes are not this contract.

- **Documentation:** [api-NodesModifier.html](../../../../../docs/research-catalog.md#file-8e674a73e4969632).
- **Pinned source:** [rna_modifier:1875 - 1983](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/makesrna/intern/rna_modifier.cc#L1875-L1983), [geometry_nodes_srna:75 - 127](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/nodes/intern/geometry_nodes_srna.cc#L75-L127), [geometry_nodes_srna:198 - 227](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/nodes/intern/geometry_nodes_srna.cc#L198-L227), [node_socket:1512 - 1546](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/nodes/intern/node_socket.cc#L1512-L1546), [geometry_nodes_execute:126 - 232](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/nodes/intern/geometry_nodes_execute.cc#L126-L232).
- **Reported experience:** No selected firsthand report independently establishes this claim.
- **Classification and limit:** D migration notes and S resolve competing intermediate example. Whether a legacy write is inert or fails is a T10 runtime observation.

## C19

Graph construction does not guarantee evaluated geometry. Missing/wrong output can clear geometry; instances and joined/realized meshes retain distinct semantics.

- **Documentation:** [api-NodeTree.html](../../../../../docs/research-catalog.md#file-d0b125abac722d4b), [api-GeometryNodeRealizeInstances.html](../../../../../docs/research-catalog.md#file-26de1c818aecafd5).
- **Pinned source:** [MOD_nodes:1760 - 1905](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/modifiers/intern/MOD_nodes.cc#L1760-L1905), [node_geo_instance_on_points:198 - 285](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/nodes/geometry/nodes/node_geo_instance_on_points.cc#L198-L285), [node_geo_realize_instances:50 - 107](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/nodes/geometry/nodes/node_geo_realize_instances.cc#L50-L107), [node_geo_join_geometry:11 - 35](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/nodes/geometry/nodes/node_geo_join_geometry.cc#L11-L35).
- **Reported experience:** No selected firsthand report independently establishes this claim.
- **Classification and limit:** D/S entry behavior; detailed realization kernel not audited. T05 checks mesh/instance counts and attributes.

## C20

A neutral material and controlled camera/light/world reduce visual ambiguity; PNG inspection must be paired with geometry metrics.

- **Documentation:** [api-Material.html](../../../../../docs/research-catalog.md#file-5e59f3dab6e57234), [api-Camera.html](../../../../../docs/research-catalog.md#file-76f5d9ef102d5446), [api-Light.html](../../../../../docs/research-catalog.md#file-0b684105f3d776e9), [api-World.html](../../../../../docs/research-catalog.md#file-073076078f432341).
- **Pinned source:** [node_shader_bsdf_principled:22 - 326](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/nodes/shader/nodes/node_shader_bsdf_principled.cc#L22-L326), [rna_material:272 - 285](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/makesrna/intern/rna_material.cc#L272-L285), [rna_world:94 - 107](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/makesrna/intern/rna_world.cc#L94-L107).
- **Reported experience:** No selected firsthand report independently establishes this claim.
- **Classification and limit:** D/S settings, I inspection design. No framing or quality adequacy was demonstrated; T08.

## C21

Cycles CPU and explicit sampling/denoising policy are configuration choices; they are not measured performance or pixel reproducibility guarantees.

- **Documentation:** [api-RenderSettings.html](../../../../../docs/research-catalog.md#file-770fc1b010d5f670).
- **Pinned source:** [engine.py:1 - 140](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/intern/cycles/blender/addon/engine.py#L1-L140), [properties.py:381 - 436](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/intern/cycles/blender/addon/properties.py#L381-L436), [properties.py:485 - 516](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/intern/cycles/blender/addon/properties.py#L485-L516).
- **Reported experience:** [R99755](EXPERIENCE.md#r99755).
- **Classification and limit:** D/S configuration, I reference preset. No benchmark/integrator audit; T08.

## C22

Synchronous render execution, Render Result, render callbacks and saved PNG are separate observations. Check write_still, reports and actual fresh artifacts.

- **Documentation:** [ops-render.html](../../../../../docs/research-catalog.md#file-d28e244d7afcec4b), [api-ImageFormatSettings.html](../../../../../docs/research-catalog.md#file-08f00250ecf94e43).
- **Pinned source:** [render_internal:236 - 355](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/editors/render/render_internal.cc#L236-L355), [pipeline:1925 - 2009](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/render/intern/pipeline.cc#L1925-L2009), [pipeline:2178 - 2248](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/render/intern/pipeline.cc#L2178-L2248).
- **Reported experience:** No selected firsthand report independently establishes this claim.
- **Classification and limit:** D/S write boundary, I artifact checks. T08 verifies failure/status/output interaction.

## C23

A .blend preserves retained original data/settings, not external generator execution state or every resource. Reopen invalidates old references.

- **Documentation:** [api-BlendData.html](../../../../../docs/research-catalog.md#file-682db53033405665), [info_gotchas_internal_data_and_python_objects.rst](../../../../../docs/research-catalog.md#file-43c072a122e05dc0), [info_gotchas_file_paths_and_encoding.rst](../../../../../docs/research-catalog.md#file-06ed6ac8670ac587).
- **Pinned source:** [wm_files:1430 - 1466](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/windowmanager/intern/wm_files.cc#L1430-L1466), [wm_files:3965 - 4090](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/windowmanager/intern/wm_files.cc#L3965-L4090).
- **Reported experience:** [R160212](EXPERIENCE.md#r160212).
- **Classification and limit:** D/S; external resource and compatibility limits remain. T06 tests actual retained content.

## C24

Saving uses temporary @ output and backup/rename handling, but does not make all file/resource mutations a transaction.

- **Documentation:** [ops-wm.html](../../../../../docs/research-catalog.md#file-91636dea1a4a8d6b).
- **Pinned source:** [wm_files:2190 - 2248](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/windowmanager/intern/wm_files.cc#L2190-L2248), [writefile:1889 - 2086](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/blenloader/intern/writefile.cc#L1889-L2086).
- **Reported experience:** No selected firsthand report independently establishes this claim.
- **Classification and limit:** S; I stable fresh output root. No filesystem crash-consistency guarantee. T06/T08.

## C25

OBJ preserves bounded static geometry/limited materials, not the procedural program. Warning-only empty export can return FINISHED without writing an OBJ.

- **Documentation:** [ops-wm.html](../../../../../docs/research-catalog.md#file-91636dea1a4a8d6b).
- **Pinned source:** [io_obj:89 - 138](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/editors/io/io_obj.cc#L89-L138), [obj_exporter:280 - 422](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/io/wavefront_obj/exporter/obj_exporter.cc#L280-L422), [obj_export_mesh:38 - 176](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/io/wavefront_obj/exporter/obj_export_mesh.cc#L38-L176).
- **Reported experience:** [R96721](EXPERIENCE.md#r96721).
- **Classification and limit:** D/S export boundary; receiver/MTL equivalence unverified. T09 tests explicit loss/axes/scale.

## C26

Semantic owner/part keys, explicit sharing and parameter/source records make revisions reviewable; a mutable name or index alone is insufficient identity.

- **Documentation:** [api-ID.html](../../../../../docs/research-catalog.md#file-9ad9be19064ee9a5), [api-Object.html](../../../../../docs/research-catalog.md#file-d566af89da2d9296), [info_gotchas_internal_data_and_python_objects.rst](../../../../../docs/research-catalog.md#file-43c072a122e05dc0).
- **Pinned source:** [rna_main_api:246 - 298](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/makesrna/intern/rna_main_api.cc#L246-L298).
- **Reported experience:** No selected firsthand report independently establishes this claim.
- **Classification and limit:** I policy grounded in D/S identity/lifetime. Not a Blender-enforced ownership system. T03/T06.

## C27

Preserve partial failures, use a fresh process/output root, and accept only verified artifacts with provenance. A zero exit code or script-written receipt alone does not prove modeling success.

- **Documentation:** [info_gotchas_crashes.rst](../../../../../docs/research-catalog.md#file-f61fa3d4b7a5b7d6), [info_best_practice.rst](../../../../../docs/research-catalog.md#file-dc757be147dab819).
- **Pinned source:** [bpy_operator_function:115 - 435](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/python/intern/bpy_operator_function.cc#L115-L435), [bmesh_py_ops_call:760 - 870](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/python/bmesh/bmesh_py_ops_call.cc#L760-L870), [obj_exporter:351 - 361](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/io/wavefront_obj/exporter/obj_exporter.cc#L351-L361).
- **Reported experience:** [R129657](EXPERIENCE.md#r129657).
- **Classification and limit:** I acceptance policy from S failure mechanisms. T01/T02/T03/T08; all examples remain unexecuted.

