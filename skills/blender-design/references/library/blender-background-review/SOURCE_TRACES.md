# Pinned implementation traces

All source below is captured at `d13f752e3b9c4f8c261cda552b1021f8bcc0382c`. **Only the listed ranges were read.** Callees are followed where needed to substantiate observable execution, validation, ownership, cleanup or error behavior; unrelated UI and numerical kernels are not implicitly audited. [Claim ledger](CLAIMS.md), [coverage](coverage.json).

## source/blender/blenkernel/intern/context.cc

[Local captured file](../../../../../docs/research-catalog.md#file-6481cad98f284898) · [receipt](../../../../../docs/research-catalog.md#file-8fcf03b3fb036dd1)

| Inspected lines | Behavior |
|---|---|
| [1752 - 1775](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/blenkernel/intern/context.cc#L1752-L1775) | Evaluated graph access and write check |

## source/blender/blenkernel/intern/curve.cc

[Local captured file](../../../../../docs/research-catalog.md#file-b10873831e257c20) · [receipt](../../../../../docs/research-catalog.md#file-9b1c3697fa2bc3a3)

| Inspected lines | Behavior |
|---|---|
| [885 - 921](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/blenkernel/intern/curve.cc#L885-L921) | Spline array reallocation |

## source/blender/blenkernel/intern/lib_id.cc

[Local captured file](../../../../../docs/research-catalog.md#file-bedf847976a2bdc8) · [receipt](../../../../../docs/research-catalog.md#file-ad61917d82a24998)

| Inspected lines | Behavior |
|---|---|
| [851 - 903](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/blenkernel/intern/lib_id.cc#L851-L903) | Copy references remapped to originals |

## source/blender/blenkernel/intern/lib_id_delete.cc

[Local captured file](../../../../../docs/research-catalog.md#file-c689420977c22f70) · [receipt](../../../../../docs/research-catalog.md#file-96baeffe16a6e2bf)

| Inspected lines | Behavior |
|---|---|
| [259 - 362](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/blenkernel/intern/lib_id_delete.cc#L259-L362) | Recursive deletion of never-null users |

## source/blender/blenkernel/intern/mesh_convert.cc

[Local captured file](../../../../../docs/research-catalog.md#file-05d3a2c877927c9c) · [receipt](../../../../../docs/research-catalog.md#file-b19cb6e465edb085)

| Inspected lines | Behavior |
|---|---|
| [860 - 1055](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/blenkernel/intern/mesh_convert.cc#L860-L1055) | Conversion ownership, Main transfer and anonymous attributes |

## source/blender/blenkernel/intern/mesh_mirror.cc

[Local captured file](../../../../../docs/research-catalog.md#file-db762c15ce88fa7c) · [receipt](../../../../../docs/research-catalog.md#file-6e46b24fccfc52cf)

| Inspected lines | Behavior |
|---|---|
| [118 - 200](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/blenkernel/intern/mesh_mirror.cc#L118-L200) | Coordinate conversion and mirrored allocation |

## source/blender/blenkernel/intern/object.cc

[Local captured file](../../../../../docs/research-catalog.md#file-072d31707d029c31) · [receipt](../../../../../docs/research-catalog.md#file-cb9f089bea492ea3)

| Inspected lines | Behavior |
|---|---|
| [3763 - 3807](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/blenkernel/intern/object.cc#L3763-L3807) | Cached dimensions and scale setting |
| [5601 - 5622](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/blenkernel/intern/object.cc#L5601-L5622) | Repeated temporary conversion and cleanup |

## source/blender/blenkernel/intern/scene.cc

[Local captured file](../../../../../docs/research-catalog.md#file-898c3288d81fac9c) · [receipt](../../../../../docs/research-catalog.md#file-ed1ffc63eb6a1903)

| Inspected lines | Behavior |
|---|---|
| [2749 - 2858](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/blenkernel/intern/scene.cc#L2749-L2858) | Evaluation refresh boundary and callbacks |

## source/blender/blenloader/intern/writefile.cc

[Local captured file](../../../../../docs/research-catalog.md#file-621524bf291f8eca) · [receipt](../../../../../docs/research-catalog.md#file-965dacd24346d3d1)

| Inspected lines | Behavior |
|---|---|
| [1889 - 2152](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/blenloader/intern/writefile.cc#L1889-L2152) | Save temporary file remapping backup rename and wrapper |

## source/blender/bmesh/tools/bmesh_bevel.cc

[Local captured file](../../../../../docs/research-catalog.md#file-916c2c571669f496) · [receipt](../../../../../docs/research-catalog.md#file-b7231e5d79036535)

| Inspected lines | Behavior |
|---|---|
| [8239 - 8322](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/bmesh/tools/bmesh_bevel.cc#L8239-L8322) | Bevel parameter normalization and early return |

## source/blender/depsgraph/intern/depsgraph_query.cc

[Local captured file](../../../../../docs/research-catalog.md#file-54da82f825977c4c) · [receipt](../../../../../docs/research-catalog.md#file-a1df6d91b8f0d8b5)

| Inspected lines | Behavior |
|---|---|
| [180 - 230](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/depsgraph/intern/depsgraph_query.cc#L180-L230) | Evaluated ID lookup delegation |

## source/blender/editors/io/io_obj.cc

[Local captured file](../../../../../docs/research-catalog.md#file-15a57cff3e1b1394) · [receipt](../../../../../docs/research-catalog.md#file-8d02204344aa2849)

| Inspected lines | Behavior |
|---|---|
| [89 - 165](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/editors/io/io_obj.cc#L89-L165) | OBJ operator parameters and report-based status |

## source/blender/editors/object/object_modifier.cc

[Local captured file](../../../../../docs/research-catalog.md#file-b8bfb3474604824c) · [receipt](../../../../../docs/research-catalog.md#file-1b7556fe840a5248)

| Inspected lines | Behavior |
|---|---|
| [1257 - 1362](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/editors/object/object_modifier.cc#L1257-L1362) | Modifier apply mode ownership and partial success behavior |
| [1991 - 2078](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/editors/object/object_modifier.cc#L1991-L2078) | Modifier apply iteration and return |

## source/blender/io/wavefront_obj/exporter/obj_export_mesh.cc

[Local captured file](../../../../../docs/research-catalog.md#file-2be9060354acebae) · [receipt](../../../../../docs/research-catalog.md#file-a5fed90bdf37f6ee)

| Inspected lines | Behavior |
|---|---|
| [25 - 176](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/io/wavefront_obj/exporter/obj_export_mesh.cc#L25-L176) | Evaluated mesh ownership materials transforms and normals |

## source/blender/makesrna/intern/rna_collection.cc

[Local captured file](../../../../../docs/research-catalog.md#file-a4901f29101c5d6a) · [receipt](../../../../../docs/research-catalog.md#file-19258472fdd4fd67)

| Inspected lines | Behavior |
|---|---|
| [134 - 178](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/makesrna/intern/rna_collection.cc#L134-L178) | Link unlink and dependency tags |

## source/blender/makesrna/intern/rna_context.cc

[Local captured file](../../../../../docs/research-catalog.md#file-7a7b88b9fed9f5fd) · [receipt](../../../../../docs/research-catalog.md#file-9891b072d155274e)

| Inspected lines | Behavior |
|---|---|
| [226 - 243](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/makesrna/intern/rna_context.cc#L226-L243) | Evaluated graph entry |

## source/blender/makesrna/intern/rna_light.cc

[Local captured file](../../../../../docs/research-catalog.md#file-9a3284b4a0dbff67) · [receipt](../../../../../docs/research-catalog.md#file-72fafa21efa26abf)

| Inspected lines | Behavior |
|---|---|
| [170 - 205](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/makesrna/intern/rna_light.cc#L170-L205) | Light color and temperature properties |

## source/blender/makesrna/intern/rna_material.cc

[Local captured file](../../../../../docs/research-catalog.md#file-32163af8ca80f59e) · [receipt](../../../../../docs/research-catalog.md#file-b1a2359189d24341)

| Inspected lines | Behavior |
|---|---|
| [272 - 285](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/makesrna/intern/rna_material.cc#L272-L285) | Deprecated use_nodes no-op |

## source/blender/makesrna/intern/rna_node_tree_interface.cc

[Local captured file](../../../../../docs/research-catalog.md#file-4af4ffe411731d37) · [receipt](../../../../../docs/research-catalog.md#file-1c58dd6c65154136)

| Inspected lines | Behavior |
|---|---|
| [729 - 774](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/makesrna/intern/rna_node_tree_interface.cc#L729-L774) | Interface socket type and parent checks |

## source/blender/makesrna/intern/rna_object.cc

[Local captured file](../../../../../docs/research-catalog.md#file-aca05866b75b5180) · [receipt](../../../../../docs/research-catalog.md#file-2d119264a94c825e)

| Inspected lines | Behavior |
|---|---|
| [1217 - 1232](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/makesrna/intern/rna_object.cc#L1217-L1232) | Dimensions getter/setter binding |

## source/blender/makesrna/intern/rna_world.cc

[Local captured file](../../../../../docs/research-catalog.md#file-4c7f1fddcc404100) · [receipt](../../../../../docs/research-catalog.md#file-e6a0192c34d35823)

| Inspected lines | Behavior |
|---|---|
| [94 - 107](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/makesrna/intern/rna_world.cc#L94-L107) | Deprecated use_nodes no-op |

## source/blender/modifiers/intern/MOD_solidify_extrude.cc

[Local captured file](../../../../../docs/research-catalog.md#file-57741c4b4d4788dc) · [receipt](../../../../../docs/research-catalog.md#file-07fee6f817574959)

| Inspected lines | Behavior |
|---|---|
| [80 - 140](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/modifiers/intern/MOD_solidify_extrude.cc#L80-L140) | Nonmanifold edge guard |
| [150 - 203](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/modifiers/intern/MOD_solidify_extrude.cc#L150-L203) | Shell settings |

## source/blender/modifiers/intern/MOD_solidify_nonmanifold.cc

[Local captured file](../../../../../docs/research-catalog.md#file-c79c16196ebeb268) · [receipt](../../../../../docs/research-catalog.md#file-253d9d76f6f563e7)

| Inspected lines | Behavior |
|---|---|
| [138 - 178](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/modifiers/intern/MOD_solidify_nonmanifold.cc#L138-L178) | Complex mode early return and thickness parameters |

## source/blender/nodes/intern/geometry_nodes_execute.cc

[Local captured file](../../../../../docs/research-catalog.md#file-4beefd47fb6cd39c) · [receipt](../../../../../docs/research-catalog.md#file-6da7b095cac7fe17)

| Inspected lines | Behavior |
|---|---|
| [126 - 232](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/nodes/intern/geometry_nodes_execute.cc#L126-L232) | Typed scalar vector color and field input consumption |
| [554 - 656](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/nodes/intern/geometry_nodes_execute.cc#L554-L656) | Lazy graph execution inputs outputs and cleanup |

## source/blender/nodes/intern/geometry_nodes_srna.cc

[Local captured file](../../../../../docs/research-catalog.md#file-4f0ea3be00d1c5ca) · [receipt](../../../../../docs/research-catalog.md#file-315f655f0b120e61)

| Inspected lines | Behavior |
|---|---|
| [75 - 127](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/nodes/intern/geometry_nodes_srna.cc#L75-L127) | Input identifiers and generated structures |
| [198 - 227](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/nodes/intern/geometry_nodes_srna.cc#L198-L227) | Per-modifier properties structure |

## source/blender/nodes/intern/node_common.cc

[Local captured file](../../../../../docs/research-catalog.md#file-39085c3a06ffe488) · [receipt](../../../../../docs/research-catalog.md#file-721a55c0598b64c4)

| Inspected lines | Behavior |
|---|---|
| [964 - 1032](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/nodes/intern/node_common.cc#L964-L1032) | Group interface socket declarations |

## source/blender/nodes/intern/node_socket.cc

[Local captured file](../../../../../docs/research-catalog.md#file-40157a890375e9e3) · [receipt](../../../../../docs/research-catalog.md#file-d1154dd58f6e0375)

| Inspected lines | Behavior |
|---|---|
| [1270 - 1345](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/nodes/intern/node_socket.cc#L1270-L1345) | Input property construction |
| [1512 - 1555](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/nodes/intern/node_socket.cc#L1512-L1555) | Float value RNA and evaluation tagging |

## source/blender/nodes/shader/nodes/node_shader_background.cc

[Local captured file](../../../../../docs/research-catalog.md#file-8bd4c98095095911) · [receipt](../../../../../docs/research-catalog.md#file-1e7b5c13d55a5f5e)

| Inspected lines | Behavior |
|---|---|
| [1 - 35](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/nodes/shader/nodes/node_shader_background.cc#L1-L35) | World shader declaration |

## source/blender/nodes/shader/nodes/node_shader_output_world.cc

[Local captured file](../../../../../docs/research-catalog.md#file-abff2b6353e7dd29) · [receipt](../../../../../docs/research-catalog.md#file-18800a80dca0c149)

| Inspected lines | Behavior |
|---|---|
| [1 - 35](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/nodes/shader/nodes/node_shader_output_world.cc#L1-L35) | World output declaration and shader links |

## source/blender/python/generic/py_capi_utils.cc

[Local captured file](../../../../../docs/research-catalog.md#file-19ae5487e0dfca6c) · [receipt](../../../../../docs/research-catalog.md#file-0707d644658e4dec)

| Inspected lines | Behavior |
|---|---|
| [966 - 1038](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/python/generic/py_capi_utils.cc#L966-L1038) | SystemExit handling |
| [1256 - 1287](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/python/generic/py_capi_utils.cc#L1256-L1287) | Script namespace |

## source/blender/python/intern/bpy_interface.cc

[Local captured file](../../../../../docs/research-catalog.md#file-f8d48697e4da8de3) · [receipt](../../../../../docs/research-catalog.md#file-46510fb7beffbb1a)

| Inspected lines | Behavior |
|---|---|
| [368 - 597](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/python/intern/bpy_interface.cc#L368-L597) | Embedded Python isolation and bundled executable |

## source/blender/render/intern/pipeline.cc

[Local captured file](../../../../../docs/research-catalog.md#file-274396b749c805d0) · [receipt](../../../../../docs/research-catalog.md#file-bf757582e7f306e8)

| Inspected lines | Behavior |
|---|---|
| [1925 - 2025](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/render/intern/pipeline.cc#L1925-L2025) | Still render pipeline and write/callback timing |
| [2178 - 2248](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/render/intern/pipeline.cc#L2178-L2248) | Image output dispatch |

## source/blender/windowmanager/intern/wm_event_system.cc

[Local captured file](../../../../../docs/research-catalog.md#file-ec8382a84009c625) · [receipt](../../../../../docs/research-catalog.md#file-7e8d80287df6e9fa)

| Inspected lines | Behavior |
|---|---|
| [2002 - 2045](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/windowmanager/intern/wm_event_system.cc#L2002-L2045) | Python operator dispatch and undo depth |

## source/blender/windowmanager/intern/wm_init_exit.cc

[Local captured file](../../../../../docs/research-catalog.md#file-76934b088a5cf15f) · [receipt](../../../../../docs/research-catalog.md#file-9c7517dbd82f805d)

| Inspected lines | Behavior |
|---|---|
| [710 - 741](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/windowmanager/intern/wm_init_exit.cc#L710-L741) | Process cleanup and explicit exit |

## intern/cycles/blender/addon/engine.py

[Local captured file](../../../../../docs/research-catalog.md#file-913b06fbaae4ff90) · [receipt](../../../../../docs/research-catalog.md#file-5daba2c03f324de1)

| Inspected lines | Behavior |
|---|---|
| [1 - 140](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/intern/cycles/blender/addon/engine.py#L1-L140) | Cycles configuration session and synchronous native render call |

## intern/cycles/blender/addon/properties.py

[Local captured file](../../../../../docs/research-catalog.md#file-9f900bbe64bbcb61) · [receipt](../../../../../docs/research-catalog.md#file-a7a5e73d7523081f)

| Inspected lines | Behavior |
|---|---|
| [381 - 436](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/intern/cycles/blender/addon/properties.py#L381-L436) | CPU and denoising defaults |
| [485 - 516](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/intern/cycles/blender/addon/properties.py#L485-L516) | Sample defaults and subset |

## scripts/modules/bpy/ops.py

[Local captured file](../../../../../docs/research-catalog.md#file-acb93dc7488dace7) · [receipt](../../../../../docs/research-catalog.md#file-b130a8e86550bb35)

| Inspected lines | Behavior |
|---|---|
| [1 - 65](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/scripts/modules/bpy/ops.py#L1-L65) | Native operator callable dispatch |

## source/blender/blenkernel/intern/mesh_validate.cc

[Local captured file](../../../../../docs/research-catalog.md#file-02e583f9e35f79ec) · [receipt](../../../../../docs/research-catalog.md#file-4aad9be3826fae2c)

| Inspected lines | Behavior |
|---|---|
| [852 - 951](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/blenkernel/intern/mesh_validate.cc#L852-L951) | Validation pipeline and repair bookkeeping |

## source/blender/bmesh/operators/bmo_bevel.cc

[Local captured file](../../../../../docs/research-catalog.md#file-e84fbb46d242702a) · [receipt](../../../../../docs/research-catalog.md#file-410adf64d6e1eb96)

| Inspected lines | Behavior |
|---|---|
| [1 - 96](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/bmesh/operators/bmo_bevel.cc#L1-L96) | Bevel wrapper complete file |

## source/blender/bmesh/operators/bmo_extrude.cc

[Local captured file](../../../../../docs/research-catalog.md#file-a500f605092299ea) · [receipt](../../../../../docs/research-catalog.md#file-43be24286b6b3338)

| Inspected lines | Behavior |
|---|---|
| [319 - 465](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/bmesh/operators/bmo_extrude.cc#L319-L465) | Region extrusion duplication deletion and output |
| [465 - 627](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/bmesh/operators/bmo_extrude.cc#L465-L627) | Extrusion sides attributes and cleanup |
| [627 - 632](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/bmesh/operators/bmo_extrude.cc#L627-L632) | Extrusion operation cleanup |

## source/blender/editors/render/render_internal.cc

[Local captured file](../../../../../docs/research-catalog.md#file-b27bda6b088251a2) · [receipt](../../../../../docs/research-catalog.md#file-4382819724ec0ecd)

| Inspected lines | Behavior |
|---|---|
| [236 - 367](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/editors/render/render_internal.cc#L236-L367) | Synchronous render execution and status |

## source/blender/io/wavefront_obj/exporter/obj_exporter.cc

[Local captured file](../../../../../docs/research-catalog.md#file-973552807c036a2f) · [receipt](../../../../../docs/research-catalog.md#file-49cc64e390fdfd99)

| Inspected lines | Behavior |
|---|---|
| [280 - 422](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/io/wavefront_obj/exporter/obj_exporter.cc#L280-L422) | File writer failure and warning-only empty output |

## source/blender/makesrna/intern/rna_ID.cc

[Local captured file](../../../../../docs/research-catalog.md#file-75b086e20dbfb830) · [receipt](../../../../../docs/research-catalog.md#file-3f591acc366b5f7f)

| Inspected lines | Behavior |
|---|---|
| [757 - 782](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/makesrna/intern/rna_ID.cc#L757-L782) | Evaluated get and copy |

## source/blender/makesrna/intern/rna_curve.cc

[Local captured file](../../../../../docs/research-catalog.md#file-396443914fcd18c1) · [receipt](../../../../../docs/research-catalog.md#file-0af5137c19a12ec2)

| Inspected lines | Behavior |
|---|---|
| [604 - 760](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/makesrna/intern/rna_curve.cc#L604-L760) | Spline point creation and mutation |

## source/blender/makesrna/intern/rna_depsgraph.cc

[Local captured file](../../../../../docs/research-catalog.md#file-a1f9627889c555ea) · [receipt](../../../../../docs/research-catalog.md#file-533c8f8ae672a406)

| Inspected lines | Behavior |
|---|---|
| [285 - 321](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/makesrna/intern/rna_depsgraph.cc#L285-L321) | Evaluation update and reentrancy guard |

## source/blender/makesrna/intern/rna_main_api.cc

[Local captured file](../../../../../docs/research-catalog.md#file-4d0a543da989a30a) · [receipt](../../../../../docs/research-catalog.md#file-ca4bd34e8b06fdf3)

| Inspected lines | Behavior |
|---|---|
| [115 - 172](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/makesrna/intern/rna_main_api.cc#L115-L172) | Remove ID and invalidate wrapper |
| [246 - 298](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/makesrna/intern/rna_main_api.cc#L246-L298) | Object and material creation |
| [324 - 381](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/makesrna/intern/rna_main_api.cc#L324-L381) | Node tree and mesh creation |
| [558 - 570](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/makesrna/intern/rna_main_api.cc#L558-L570) | World default node creation |

## source/blender/makesrna/intern/rna_mesh.cc

[Local captured file](../../../../../docs/research-catalog.md#file-a474a6f028e9c694) · [receipt](../../../../../docs/research-catalog.md#file-f094630b01d92fdf)

| Inspected lines | Behavior |
|---|---|
| [400 - 474](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/makesrna/intern/rna_mesh.cc#L400-L474) | Coordinates selection attributes and loop indices |
| [1686 - 1786](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/makesrna/intern/rna_mesh.cc#L1686-L1786) | Lazy normal access |

## source/blender/makesrna/intern/rna_mesh_api.cc

[Local captured file](../../../../../docs/research-catalog.md#file-4a83ac0fb7b14b59) · [receipt](../../../../../docs/research-catalog.md#file-324c70baa944f2e4)

| Inspected lines | Behavior |
|---|---|
| [198 - 258](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/makesrna/intern/rna_mesh_api.cc#L198-L258) | Mesh update clear and validation return |

## source/blender/makesrna/intern/rna_modifier.cc

[Local captured file](../../../../../docs/research-catalog.md#file-2cd0824310cfeaf1) · [receipt](../../../../../docs/research-catalog.md#file-690050a227f9b53e)

| Inspected lines | Behavior |
|---|---|
| [1875 - 1983](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/makesrna/intern/rna_modifier.cc#L1875-L1983) | Geometry node group and dynamic property RNA |

## source/blender/makesrna/intern/rna_nodetree.cc

[Local captured file](../../../../../docs/research-catalog.md#file-76ecc0f0128fde57) · [receipt](../../../../../docs/research-catalog.md#file-674e35e34a99ac8a)

| Inspected lines | Behavior |
|---|---|
| [1259 - 1325](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/makesrna/intern/rna_nodetree.cc#L1259-L1325) | Node creation validation |
| [1425 - 1532](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/makesrna/intern/rna_nodetree.cc#L1425-L1532) | Link direction limits removal and invalidation |

## source/blender/makesrna/intern/rna_object_api.cc

[Local captured file](../../../../../docs/research-catalog.md#file-ed414f7a7bf0d9af) · [receipt](../../../../../docs/research-catalog.md#file-151daf67251264e1)

| Inspected lines | Behavior |
|---|---|
| [426 - 451](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/makesrna/intern/rna_object_api.cc#L426-L451) | Temporary mesh entry and cleanup |

## source/blender/modifiers/intern/MOD_array.cc

[Local captured file](../../../../../docs/research-catalog.md#file-f0c8933bc8b6eda8) · [receipt](../../../../../docs/research-catalog.md#file-769b6d1d559bfe68)

| Inspected lines | Behavior |
|---|---|
| [450 - 551](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/modifiers/intern/MOD_array.cc#L450-L551) | Offset calculation and copy count limits |
| [867 - 881](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/modifiers/intern/MOD_array.cc#L867-L881) | Modifier entry |

## source/blender/modifiers/intern/MOD_bevel.cc

[Local captured file](../../../../../docs/research-catalog.md#file-a16e88f2c6db58da) · [receipt](../../../../../docs/research-catalog.md#file-83a0a2c3a797e20a)

| Inspected lines | Behavior |
|---|---|
| [111 - 261](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/modifiers/intern/MOD_bevel.cc#L111-L261) | Selection eligibility and kernel arguments |
| [262 - 290](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/modifiers/intern/MOD_bevel.cc#L262-L290) | BMesh output conversion and cleanup |

## source/blender/modifiers/intern/MOD_boolean.cc

[Local captured file](../../../../../docs/research-catalog.md#file-8491eff8505e4d79) · [receipt](../../../../../docs/research-catalog.md#file-774fe420dcad04e0)

| Inspected lines | Behavior |
|---|---|
| [159 - 218](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/modifiers/intern/MOD_boolean.cc#L159-L218) | Error checks and handedness |
| [527 - 612](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/modifiers/intern/MOD_boolean.cc#L527-L612) | Evaluated operands and failure paths |

## source/blender/modifiers/intern/MOD_mirror.cc

[Local captured file](../../../../../docs/research-catalog.md#file-6cba06ae6f449f63) · [receipt](../../../../../docs/research-catalog.md#file-ba188062ccd37698)

| Inspected lines | Behavior |
|---|---|
| [67 - 149](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/modifiers/intern/MOD_mirror.cc#L67-L149) | Axis composition and cleanup |

## source/blender/modifiers/intern/MOD_nodes.cc

[Local captured file](../../../../../docs/research-catalog.md#file-2ed6f5053e68a325) · [receipt](../../../../../docs/research-catalog.md#file-577ba2523f74fc56)

| Inspected lines | Behavior |
|---|---|
| [1760 - 1905](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/modifiers/intern/MOD_nodes.cc#L1760-L1905) | Graph output checks and evaluation boundary |

## source/blender/modifiers/intern/MOD_solidify.cc

[Local captured file](../../../../../docs/research-catalog.md#file-1c5cd05618d25ed2) · [receipt](../../../../../docs/research-catalog.md#file-909c61624f72bde6)

| Inspected lines | Behavior |
|---|---|
| [56 - 85](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/modifiers/intern/MOD_solidify.cc#L56-L85) | Algorithm dispatch |

## source/blender/modifiers/intern/MOD_subsurf.cc

[Local captured file](../../../../../docs/research-catalog.md#file-89e36dbb1f73e2a6) · [receipt](../../../../../docs/research-catalog.md#file-31d3142b3bd0e003)

| Inspected lines | Behavior |
|---|---|
| [192 - 278](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/modifiers/intern/MOD_subsurf.cc#L192-L278) | Lazy tessellation and mode handling |

## source/blender/nodes/geometry/nodes/node_geo_input_position.cc

[Local captured file](../../../../../docs/research-catalog.md#file-166a7b154f778a70) · [receipt](../../../../../docs/research-catalog.md#file-07005ddcfe56c93d)

| Inspected lines | Behavior |
|---|---|
| [9 - 12](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/nodes/geometry/nodes/node_geo_input_position.cc#L9-L12) | Node declaration or execution entry |
| [14 - 17](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/nodes/geometry/nodes/node_geo_input_position.cc#L14-L17) | Node declaration or execution entry |

## source/blender/nodes/geometry/nodes/node_geo_instance_on_points.cc

[Local captured file](../../../../../docs/research-catalog.md#file-c1d0469a7fc85b87) · [receipt](../../../../../docs/research-catalog.md#file-b866ff673fda8dd0)

| Inspected lines | Behavior |
|---|---|
| [21 - 51](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/nodes/geometry/nodes/node_geo_instance_on_points.cc#L21-L51) | Node declaration or execution entry |
| [198 - 285](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/nodes/geometry/nodes/node_geo_instance_on_points.cc#L198-L285) | Node declaration or execution entry |

## source/blender/nodes/geometry/nodes/node_geo_join_geometry.cc

[Local captured file](../../../../../docs/research-catalog.md#file-56a03a70fb61192a) · [receipt](../../../../../docs/research-catalog.md#file-44bd7e84c019e2ee)

| Inspected lines | Behavior |
|---|---|
| [11 - 19](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/nodes/geometry/nodes/node_geo_join_geometry.cc#L11-L19) | Node declaration or execution entry |
| [11 - 35](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/nodes/geometry/nodes/node_geo_join_geometry.cc#L11-L35) | Declaration and full join dispatch through output assignment |
| [21 - 35](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/nodes/geometry/nodes/node_geo_join_geometry.cc#L21-L35) | Node declaration or execution entry |

## source/blender/nodes/geometry/nodes/node_geo_mesh_primitive_cube.cc

[Local captured file](../../../../../docs/research-catalog.md#file-6e8b4a14f239bc55) · [receipt](../../../../../docs/research-catalog.md#file-5a956199479a8f65)

| Inspected lines | Behavior |
|---|---|
| [21 - 45](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/nodes/geometry/nodes/node_geo_mesh_primitive_cube.cc#L21-L45) | Node declaration or execution entry |
| [95 - 114](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/nodes/geometry/nodes/node_geo_mesh_primitive_cube.cc#L95-L114) | Node declaration or execution entry |

## source/blender/nodes/geometry/nodes/node_geo_mesh_primitive_line.cc

[Local captured file](../../../../../docs/research-catalog.md#file-f6885fadd4526090) · [receipt](../../../../../docs/research-catalog.md#file-61e185969df67184)

| Inspected lines | Behavior |
|---|---|
| [26 - 54](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/nodes/geometry/nodes/node_geo_mesh_primitive_line.cc#L26-L54) | Node declaration or execution entry |
| [66 - 74](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/nodes/geometry/nodes/node_geo_mesh_primitive_line.cc#L66-L74) | Node declaration or execution entry |
| [132 - 175](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/nodes/geometry/nodes/node_geo_mesh_primitive_line.cc#L132-L175) | Node declaration or execution entry |

## source/blender/nodes/geometry/nodes/node_geo_realize_instances.cc

[Local captured file](../../../../../docs/research-catalog.md#file-3b9ad5ac9f4f322d) · [receipt](../../../../../docs/research-catalog.md#file-46309ef9dffc24a5)

| Inspected lines | Behavior |
|---|---|
| [20 - 43](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/nodes/geometry/nodes/node_geo_realize_instances.cc#L20-L43) | Node declaration or execution entry |
| [50 - 107](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/nodes/geometry/nodes/node_geo_realize_instances.cc#L50-L107) | Node declaration or execution entry |

## source/blender/nodes/geometry/nodes/node_geo_set_position.cc

[Local captured file](../../../../../docs/research-catalog.md#file-849c97b0936e39a0) · [receipt](../../../../../docs/research-catalog.md#file-01f74f2bcb5abfa4)

| Inspected lines | Behavior |
|---|---|
| [18 - 32](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/nodes/geometry/nodes/node_geo_set_position.cc#L18-L32) | Node declaration or execution entry |
| [128 - 164](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/nodes/geometry/nodes/node_geo_set_position.cc#L128-L164) | Node declaration or execution entry |

## source/blender/nodes/geometry/nodes/node_geo_transform_geometry.cc

[Local captured file](../../../../../docs/research-catalog.md#file-8c43f2b9e05a66cc) · [receipt](../../../../../docs/research-catalog.md#file-eadac4cae985bb44)

| Inspected lines | Behavior |
|---|---|
| [25 - 48](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/nodes/geometry/nodes/node_geo_transform_geometry.cc#L25-L48) | Node declaration or execution entry |
| [76 - 106](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/nodes/geometry/nodes/node_geo_transform_geometry.cc#L76-L106) | Node declaration or execution entry |

## source/blender/nodes/shader/nodes/node_shader_bsdf_principled.cc

[Local captured file](../../../../../docs/research-catalog.md#file-f019cee67a111b6f) · [receipt](../../../../../docs/research-catalog.md#file-a583dcd118a4344e)

| Inspected lines | Behavior |
|---|---|
| [22 - 326](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/nodes/shader/nodes/node_shader_bsdf_principled.cc#L22-L326) | Node declaration or execution entry |
| [328 - 332](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/nodes/shader/nodes/node_shader_bsdf_principled.cc#L328-L332) | Node declaration or execution entry |

## source/blender/nodes/shader/nodes/node_shader_mapping.cc

[Local captured file](../../../../../docs/research-catalog.md#file-642db98b82fb918b) · [receipt](../../../../../docs/research-catalog.md#file-f74b031718a95fcf)

| Inspected lines | Behavior |
|---|---|
| [18 - 44](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/nodes/shader/nodes/node_shader_mapping.cc#L18-L44) | Node declaration or execution entry |

## source/blender/nodes/shader/nodes/node_shader_math.cc

[Local captured file](../../../../../docs/research-catalog.md#file-fe1d85f2fab0082f) · [receipt](../../../../../docs/research-catalog.md#file-760c649de309ca71)

| Inspected lines | Behavior |
|---|---|
| [27 - 91](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/nodes/shader/nodes/node_shader_math.cc#L27-L91) | Node declaration or execution entry |

## source/blender/nodes/shader/nodes/node_shader_output_material.cc

[Local captured file](../../../../../docs/research-catalog.md#file-6c513060c8b2e90c) · [receipt](../../../../../docs/research-catalog.md#file-6dca0190c8f3b0b4)

| Inspected lines | Behavior |
|---|---|
| [11 - 17](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/nodes/shader/nodes/node_shader_output_material.cc#L11-L17) | Node declaration or execution entry |

## source/blender/nodes/shader/nodes/node_shader_rgb.cc

[Local captured file](../../../../../docs/research-catalog.md#file-faebddcc5247aa15) · [receipt](../../../../../docs/research-catalog.md#file-df815f23630c222b)

| Inspected lines | Behavior |
|---|---|
| [19 - 30](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/nodes/shader/nodes/node_shader_rgb.cc#L19-L30) | Node declaration or execution entry |

## source/blender/nodes/shader/nodes/node_shader_tex_coord.cc

[Local captured file](../../../../../docs/research-catalog.md#file-ab26ae8c0eb184e6) · [receipt](../../../../../docs/research-catalog.md#file-b8db5e79188bc445)

| Inspected lines | Behavior |
|---|---|
| [16 - 25](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/nodes/shader/nodes/node_shader_tex_coord.cc#L16-L25) | Node declaration or execution entry |

## source/blender/nodes/shader/nodes/node_shader_tex_noise.cc

[Local captured file](../../../../../docs/research-catalog.md#file-f92868b4425d67b7) · [receipt](../../../../../docs/research-catalog.md#file-1fe57d8f2995bff3)

| Inspected lines | Behavior |
|---|---|
| [25 - 103](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/nodes/shader/nodes/node_shader_tex_noise.cc#L25-L103) | Node declaration or execution entry |
| [114 - 124](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/nodes/shader/nodes/node_shader_tex_noise.cc#L114-L124) | Node declaration or execution entry |

## source/blender/nodes/shader/nodes/node_shader_value.cc

[Local captured file](../../../../../docs/research-catalog.md#file-ff1e323241270d39) · [receipt](../../../../../docs/research-catalog.md#file-d25cc5e6a0e68892)

| Inspected lines | Behavior |
|---|---|
| [23 - 33](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/nodes/shader/nodes/node_shader_value.cc#L23-L33) | Node declaration or execution entry |

## source/blender/nodes/shader/nodes/node_shader_vector_math.cc

[Local captured file](../../../../../docs/research-catalog.md#file-2aa6770e7b7264d5) · [receipt](../../../../../docs/research-catalog.md#file-5ac6018bb24d8675)

| Inspected lines | Behavior |
|---|---|
| [31 - 94](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/nodes/shader/nodes/node_shader_vector_math.cc#L31-L94) | Node declaration or execution entry |

## source/blender/python/bmesh/bmesh_py_api.cc

[Local captured file](../../../../../docs/research-catalog.md#file-ba6cbec7ec63b37f) · [receipt](../../../../../docs/research-catalog.md#file-fcdbd9085199efaa)

| Inspected lines | Behavior |
|---|---|
| [38 - 161](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/python/bmesh/bmesh_py_api.cc#L38-L161) | Owned and Edit Mode BMesh entry |

## source/blender/python/bmesh/bmesh_py_ops_call.cc

[Local captured file](../../../../../docs/research-catalog.md#file-f1b1d993245b7e10) · [receipt](../../../../../docs/research-catalog.md#file-f2b7093135b9d5d0)

| Inspected lines | Behavior |
|---|---|
| [760 - 870](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/python/bmesh/bmesh_py_ops_call.cc#L760-L870) | Slot validation execution errors and cleanup |

## source/blender/python/bmesh/bmesh_py_types.cc

[Local captured file](../../../../../docs/research-catalog.md#file-11fafa7fd2eb4874) · [receipt](../../../../../docs/research-catalog.md#file-7a3ac2380791449c)

| Inspected lines | Behavior |
|---|---|
| [1319 - 1408](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/python/bmesh/bmesh_py_types.cc#L1319-L1408) | Free and to_mesh ownership |
| [1513 - 1592](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/python/bmesh/bmesh_py_types.cc#L1513-L1592) | from_mesh import semantics |

## source/blender/python/intern/bpy_interface_run.cc

[Local captured file](../../../../../docs/research-catalog.md#file-4ec14fe6bca60188) · [receipt](../../../../../docs/research-catalog.md#file-bf9d02cd0865401f)

| Inspected lines | Behavior |
|---|---|
| [70 - 252](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/python/intern/bpy_interface_run.cc#L70-L252) | Script namespace, exceptions, cleanup |

## source/blender/python/intern/bpy_operator_function.cc

[Local captured file](../../../../../docs/research-catalog.md#file-e16a3196443db0b2) · [receipt](../../../../../docs/research-catalog.md#file-2abeed9b1ba0126b)

| Inspected lines | Behavior |
|---|---|
| [115 - 435](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/python/intern/bpy_operator_function.cc#L115-L435) | Argument parsing, poll, reports, view-layer updates |

## source/blender/python/intern/bpy_operator_wrap.cc

[Local captured file](../../../../../docs/research-catalog.md#file-69dfa0419593ca6f) · [receipt](../../../../../docs/research-catalog.md#file-9016d7fa83b0b04f)

| Inspected lines | Behavior |
|---|---|
| [29 - 120](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/python/intern/bpy_operator_wrap.cc#L29-L120) | Registration and deferred properties |

## source/blender/python/intern/bpy_rna_context.cc

[Local captured file](../../../../../docs/research-catalog.md#file-35ffc80a57e3bfef) · [receipt](../../../../../docs/research-catalog.md#file-7c995caf0222d2ee)

| Inspected lines | Behavior |
|---|---|
| [180 - 520](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/python/intern/bpy_rna_context.cc#L180-L520) | Context membership and restoration |

## source/blender/windowmanager/intern/wm_files.cc

[Local captured file](../../../../../docs/research-catalog.md#file-9fd2034fa6ae958b) · [receipt](../../../../../docs/research-catalog.md#file-3a4038472df4b27c)

| Inspected lines | Behavior |
|---|---|
| [1323 - 1364](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/windowmanager/intern/wm_files.cc#L1323-L1364) | Factory preferences selection |
| [1430 - 1466](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/windowmanager/intern/wm_files.cc#L1430-L1466) | Factory startup Main replacement and empty data |
| [2190 - 2248](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/windowmanager/intern/wm_files.cc#L2190-L2248) | Save implementation call and current filepath |
| [3965 - 4090](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/blender/windowmanager/intern/wm_files.cc#L3965-L4090) | Save options and operation result |

## source/creator/creator.cc

[Local captured file](../../../../../docs/research-catalog.md#file-c1250a405f351b26) · [receipt](../../../../../docs/research-catalog.md#file-0b7bb43a61d215fc)

| Inspected lines | Behavior |
|---|---|
| [481 - 671](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/creator/creator.cc#L481-L671) | Initialization passes and background exit |

## source/creator/creator_args.cc

[Local captured file](../../../../../docs/research-catalog.md#file-3df99636ced03481) · [receipt](../../../../../docs/research-catalog.md#file-7c0f549d24afc19f)

| Inspected lines | Behavior |
|---|---|
| [2690 - 2897](https://github.com/blender/blender/blob/d13f752e3b9c4f8c261cda552b1021f8bcc0382c/source/creator/creator_args.cc#L2690-L2897) | Script dispatch, exit code and Python environment flags |

