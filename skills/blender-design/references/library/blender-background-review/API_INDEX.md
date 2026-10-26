# API index

Literal identifiers are searchable with `rg -F`. Each entry routes to an explanatory module and a captured complete reference unit (or explicitly selected operator entries). Inherited members used by the review are defined in `bpy_struct`, `ID`, `Node`, `Modifier` and collection documentation; their definitions were read once. This index does not turn unrelated members into recommended operations.

## Common operations

| Identifier | Contract |
|---|---|
| `bpy.app.binary_path` | [Module 01](modules/01-execution.md) |
| `bpy.path.abspath` | [Module 01](modules/01-execution.md) |
| `bpy.data.objects` | [Module 02](modules/02-data.md) |
| `bpy.data.meshes` | [Module 02](modules/02-data.md) |
| `Object.copy` | [Module 02](modules/02-data.md) |
| `ID.copy` | [Module 02](modules/02-data.md) |
| `Collection.objects.link` | [Module 02](modules/02-data.md) |
| `bpy.data.objects.remove` | [Module 02](modules/02-data.md) |
| `bpy.data.meshes.remove` | [Module 02](modules/02-data.md) |
| `Context.temp_override` | [Module 03](modules/03-context.md) |
| `Object.evaluated_get` | [Module 03](modules/03-context.md) |
| `Context.evaluated_depsgraph_get` | [Module 03](modules/03-context.md) |
| `Object.to_mesh` | [Module 03](modules/03-context.md) |
| `Object.to_mesh_clear` | [Module 03](modules/03-context.md) |
| `BlendDataMeshes.new_from_object` | [Module 03](modules/03-context.md) |
| `ViewLayer.update` | [Module 03](modules/03-context.md) |
| `Mesh.from_pydata` | [Module 04](modules/04-mesh.md) |
| `Mesh.validate` | [Module 04](modules/04-mesh.md) |
| `Mesh.update` | [Module 04](modules/04-mesh.md) |
| `bmesh.new` | [Module 04](modules/04-mesh.md) |
| `bmesh.from_edit_mesh` | [Module 04](modules/04-mesh.md) |
| `bmesh.update_edit_mesh` | [Module 04](modules/04-mesh.md) |
| `BMesh.to_mesh` | [Module 04](modules/04-mesh.md) |
| `BMesh.free` | [Module 04](modules/04-mesh.md) |
| `bmesh.ops.extrude_face_region` | [Module 04](modules/04-mesh.md) |
| `bmesh.ops.bevel` | [Module 04](modules/04-mesh.md) |
| `Object.dimensions` | [Module 05](modules/05-transforms.md) |
| `Object.matrix_world` | [Module 05](modules/05-transforms.md) |
| `Object.modifiers.new` | [Module 05](modules/05-transforms.md) |
| `Curve.splines.new` | [Module 05](modules/05-transforms.md) |
| `NodeTree.interface` | [Module 06](modules/06-nodes.md) |
| `NodeTreeInterface.new_socket` | [Module 06](modules/06-nodes.md) |
| `NodeLinks.new` | [Module 06](modules/06-nodes.md) |
| `NodesModifier.properties` | [Module 06](modules/06-nodes.md) |
| `Material.node_tree` | [Module 07](modules/07-render.md) |
| `bpy.ops.render.render` | [Module 07](modules/07-render.md) |
| `bpy.ops.wm.save_as_mainfile` | [Module 08](modules/08-persistence.md) |
| `bpy.ops.wm.open_mainfile` | [Module 08](modules/08-persistence.md) |
| `bpy.ops.wm.obj_export` | [Module 08](modules/08-persistence.md) |

## Complete reference units

| Unit | Explanation | Captured reference |
|---|---|---|
| `AreaLight` | [Module 07](modules/07-render.md) | [reference](../../../../../docs/research-catalog.md#file-5bdd8473eb88e947) |
| `BlendDataCameras` | [Module 02](modules/02-data.md) | [reference](../../../../../docs/research-catalog.md#file-572c18d182f2ec09) |
| `BlendDataLights` | [Module 02](modules/02-data.md) | [reference](../../../../../docs/research-catalog.md#file-9ae6b6b1ae1db315) |
| `BlendDataNodeTrees` | [Module 02](modules/02-data.md) | [reference](../../../../../docs/research-catalog.md#file-8b86ea12c657209b) |
| `BlendDataWorlds` | [Module 02](modules/02-data.md) | [reference](../../../../../docs/research-catalog.md#file-887ad2b50ed22d44) |
| `CameraDOFSettings` | [Module 07](modules/07-render.md) | [reference](../../../../../docs/research-catalog.md#file-3da50b4186f0f759) |
| `CurveSplines` | [Module 05](modules/05-transforms.md) | [reference](../../../../../docs/research-catalog.md#file-96e68c9fecab2eb6) |
| `GeometryNodeTree` | [Module 06](modules/06-nodes.md) | [reference](../../../../../docs/research-catalog.md#file-215dd57d3071b380) |
| `IDMaterials` | [Module 02](modules/02-data.md) | [reference](../../../../../docs/research-catalog.md#file-13fe4dd2e80bf838) |
| `LayerCollection` | [Module 02](modules/02-data.md) | [reference](../../../../../docs/research-catalog.md#file-9df63c9a42318f17) |
| `LayerObjects` | [Module 02](modules/02-data.md) | [reference](../../../../../docs/research-catalog.md#file-40803488a798ec1d) |
| `MaterialSlot` | [Module 02](modules/02-data.md) | [reference](../../../../../docs/research-catalog.md#file-c22097c900d94cb8) |
| `NodeSocketColor` | [Module 06](modules/06-nodes.md) | [reference](../../../../../docs/research-catalog.md#file-a7bc459c8c8a4b92) |
| `NodeSocketFloat` | [Module 06](modules/06-nodes.md) | [reference](../../../../../docs/research-catalog.md#file-1cb00865f9a7b521) |
| `NodeSocketInt` | [Module 06](modules/06-nodes.md) | [reference](../../../../../docs/research-catalog.md#file-dda2e3403209e437) |
| `NodeSocketVector` | [Module 06](modules/06-nodes.md) | [reference](../../../../../docs/research-catalog.md#file-2f3b7c3f21e09935) |
| `NodeTreeInterfaceItem` | [Module 06](modules/06-nodes.md) | [reference](../../../../../docs/research-catalog.md#file-3f6b4086150d2ccd) |
| `NodeTreeInterfaceSocketFloat` | [Module 06](modules/06-nodes.md) | [reference](../../../../../docs/research-catalog.md#file-d91173602487c681) |
| `NodesModifierProperties` | [Module 06](modules/06-nodes.md) | [reference](../../../../../docs/research-catalog.md#file-96b93f7a6f0c4ee3) |
| `ShaderNodeBackground` | [Module 06](modules/06-nodes.md) | [reference](../../../../../docs/research-catalog.md#file-f2aeff8ddf15e054) |
| `ShaderNodeOutputWorld` | [Module 06](modules/06-nodes.md) | [reference](../../../../../docs/research-catalog.md#file-bb1a5cb4c981937a) |
| `ShaderNodeTree` | [Module 06](modules/06-nodes.md) | [reference](../../../../../docs/research-catalog.md#file-07087ee9040854ef) |
| `SplineBezierPoints` | [Module 05](modules/05-transforms.md) | [reference](../../../../../docs/research-catalog.md#file-b2e8eb784332280a) |
| `SplinePoints` | [Module 05](modules/05-transforms.md) | [reference](../../../../../docs/research-catalog.md#file-487596599f6b8dcc) |
| `bpy_prop_collection` | [Module 02](modules/02-data.md) | [reference](../../../../../docs/research-catalog.md#file-71e0b9e2bb26a2be) |
| `ArrayModifier` | [Module 05](modules/05-transforms.md) | [reference](../../../../../docs/research-catalog.md#file-cc2d6b6c6dcd4ca8) |
| `Attribute` | [Module 04](modules/04-mesh.md) | [reference](../../../../../docs/research-catalog.md#file-51623e7350d2b50f) |
| `AttributeGroupMesh` | [Module 04](modules/04-mesh.md) | [reference](../../../../../docs/research-catalog.md#file-2dcfd661b1255282) |
| `BevelModifier` | [Module 05](modules/05-transforms.md) | [reference](../../../../../docs/research-catalog.md#file-4133961281b9eaff) |
| `BezierSplinePoint` | [Module 05](modules/05-transforms.md) | [reference](../../../../../docs/research-catalog.md#file-3b4051a1f23de96c) |
| `BlendData` | [Module 02](modules/02-data.md) | [reference](../../../../../docs/research-catalog.md#file-682db53033405665) |
| `BlendDataCollections` | [Module 02](modules/02-data.md) | [reference](../../../../../docs/research-catalog.md#file-ccb5150c2e457bc6) |
| `BlendDataCurves` | [Module 02](modules/02-data.md) | [reference](../../../../../docs/research-catalog.md#file-b081ed6691e2c04c) |
| `BlendDataMaterials` | [Module 02](modules/02-data.md) | [reference](../../../../../docs/research-catalog.md#file-a7aabde4b0d94cb8) |
| `BlendDataMeshes` | [Module 02](modules/02-data.md) | [reference](../../../../../docs/research-catalog.md#file-763c1ec3cc36d59e) |
| `BlendDataObjects` | [Module 02](modules/02-data.md) | [reference](../../../../../docs/research-catalog.md#file-c3feb46e46344d7e) |
| `BooleanModifier` | [Module 05](modules/05-transforms.md) | [reference](../../../../../docs/research-catalog.md#file-35d3b2b7bfcb42c1) |
| `Camera` | [Module 07](modules/07-render.md) | [reference](../../../../../docs/research-catalog.md#file-76f5d9ef102d5446) |
| `Collection` | [Module 02](modules/02-data.md) | [reference](../../../../../docs/research-catalog.md#file-7d7604b22e5441d0) |
| `CollectionChildren` | [Module 02](modules/02-data.md) | [reference](../../../../../docs/research-catalog.md#file-e0203fa4e91561a6) |
| `CollectionObjects` | [Module 02](modules/02-data.md) | [reference](../../../../../docs/research-catalog.md#file-3f1f12d3030637f8) |
| `ColorManagedDisplaySettings` | [Module 07](modules/07-render.md) | [reference](../../../../../docs/research-catalog.md#file-ea1211a22110c0b4) |
| `ColorManagedInputColorspaceSettings` | [Module 07](modules/07-render.md) | [reference](../../../../../docs/research-catalog.md#file-8eb17548ceb9ff12) |
| `ColorManagedViewSettings` | [Module 07](modules/07-render.md) | [reference](../../../../../docs/research-catalog.md#file-9b87b26efbcf39fc) |
| `Context` | [Module 03](modules/03-context.md) | [reference](../../../../../docs/research-catalog.md#file-56c5733c108e652c) |
| `Curve` | [Module 05](modules/05-transforms.md) | [reference](../../../../../docs/research-catalog.md#file-9a62cc5d834ff864) |
| `Depsgraph` | [Module 03](modules/03-context.md) | [reference](../../../../../docs/research-catalog.md#file-ee183c213eefe2a2) |
| `GeometryNodeInputPosition` | [Module 06](modules/06-nodes.md) | [reference](../../../../../docs/research-catalog.md#file-b5de2051c66a20b8) |
| `GeometryNodeInstanceOnPoints` | [Module 06](modules/06-nodes.md) | [reference](../../../../../docs/research-catalog.md#file-2e405e91e18bc413) |
| `GeometryNodeJoinGeometry` | [Module 06](modules/06-nodes.md) | [reference](../../../../../docs/research-catalog.md#file-e1b5e0a683b7b32a) |
| `GeometryNodeMeshCube` | [Module 06](modules/06-nodes.md) | [reference](../../../../../docs/research-catalog.md#file-78d31fea9a2c4281) |
| `GeometryNodeMeshLine` | [Module 06](modules/06-nodes.md) | [reference](../../../../../docs/research-catalog.md#file-4ecc2236cfceb8aa) |
| `GeometryNodeRealizeInstances` | [Module 06](modules/06-nodes.md) | [reference](../../../../../docs/research-catalog.md#file-26de1c818aecafd5) |
| `GeometryNodeSetPosition` | [Module 06](modules/06-nodes.md) | [reference](../../../../../docs/research-catalog.md#file-bd1ebd7d15923501) |
| `GeometryNodeTransform` | [Module 06](modules/06-nodes.md) | [reference](../../../../../docs/research-catalog.md#file-294d50a1e41e237a) |
| `ID` | [Module 02](modules/02-data.md) | [reference](../../../../../docs/research-catalog.md#file-9ad9be19064ee9a5) |
| `ImageFormatSettings` | [Module 07](modules/07-render.md) | [reference](../../../../../docs/research-catalog.md#file-08f00250ecf94e43) |
| `Light` | [Module 07](modules/07-render.md) | [reference](../../../../../docs/research-catalog.md#file-0b684105f3d776e9) |
| `Material` | [Module 07](modules/07-render.md) | [reference](../../../../../docs/research-catalog.md#file-5e59f3dab6e57234) |
| `Mesh` | [Module 04](modules/04-mesh.md) | [reference](../../../../../docs/research-catalog.md#file-2e4b0dfc3ae778b2) |
| `MeshEdge` | [Module 04](modules/04-mesh.md) | [reference](../../../../../docs/research-catalog.md#file-59c032d5d33b8752) |
| `MeshLoop` | [Module 04](modules/04-mesh.md) | [reference](../../../../../docs/research-catalog.md#file-c0ca85f4bedd879b) |
| `MeshPolygon` | [Module 04](modules/04-mesh.md) | [reference](../../../../../docs/research-catalog.md#file-648feda98575f421) |
| `MeshVertex` | [Module 04](modules/04-mesh.md) | [reference](../../../../../docs/research-catalog.md#file-905e7cd7e94f8026) |
| `MirrorModifier` | [Module 05](modules/05-transforms.md) | [reference](../../../../../docs/research-catalog.md#file-95a4c3133a766d8d) |
| `Modifier` | [Module 05](modules/05-transforms.md) | [reference](../../../../../docs/research-catalog.md#file-986972b03854e62e) |
| `Node` | [Module 06](modules/06-nodes.md) | [reference](../../../../../docs/research-catalog.md#file-ffc6e82a993758b1) |
| `NodeGroupInput` | [Module 06](modules/06-nodes.md) | [reference](../../../../../docs/research-catalog.md#file-10c49cf21dcf5ab9) |
| `NodeGroupOutput` | [Module 06](modules/06-nodes.md) | [reference](../../../../../docs/research-catalog.md#file-adc28a6ddb6732c6) |
| `NodeLink` | [Module 06](modules/06-nodes.md) | [reference](../../../../../docs/research-catalog.md#file-c08926c26379a81a) |
| `NodeLinks` | [Module 06](modules/06-nodes.md) | [reference](../../../../../docs/research-catalog.md#file-ffb3e96911fd640c) |
| `NodeSocket` | [Module 06](modules/06-nodes.md) | [reference](../../../../../docs/research-catalog.md#file-1a742332d5f1a612) |
| `NodeTree` | [Module 06](modules/06-nodes.md) | [reference](../../../../../docs/research-catalog.md#file-d0b125abac722d4b) |
| `NodeTreeInterface` | [Module 06](modules/06-nodes.md) | [reference](../../../../../docs/research-catalog.md#file-2e3ce82a211c20ae) |
| `NodeTreeInterfaceSocket` | [Module 06](modules/06-nodes.md) | [reference](../../../../../docs/research-catalog.md#file-cc29303193b16c3f) |
| `Nodes` | [Module 06](modules/06-nodes.md) | [reference](../../../../../docs/research-catalog.md#file-e64d415eb123dd3d) |
| `NodesModifier` | [Module 06](modules/06-nodes.md) | [reference](../../../../../docs/research-catalog.md#file-8e674a73e4969632) |
| `Object` | [Module 02](modules/02-data.md) | [reference](../../../../../docs/research-catalog.md#file-d566af89da2d9296) |
| `ObjectModifiers` | [Module 05](modules/05-transforms.md) | [reference](../../../../../docs/research-catalog.md#file-8aea4639729b5a44) |
| `RenderSettings` | [Module 07](modules/07-render.md) | [reference](../../../../../docs/research-catalog.md#file-770fc1b010d5f670) |
| `Scene` | [Module 02](modules/02-data.md) | [reference](../../../../../docs/research-catalog.md#file-26dbde21973621c6) |
| `ShaderNodeBsdfPrincipled` | [Module 06](modules/06-nodes.md) | [reference](../../../../../docs/research-catalog.md#file-2629b81a079a1537) |
| `ShaderNodeMapping` | [Module 06](modules/06-nodes.md) | [reference](../../../../../docs/research-catalog.md#file-fae3528ab9bc106b) |
| `ShaderNodeMath` | [Module 06](modules/06-nodes.md) | [reference](../../../../../docs/research-catalog.md#file-2b34582bef3ddbab) |
| `ShaderNodeOutputMaterial` | [Module 06](modules/06-nodes.md) | [reference](../../../../../docs/research-catalog.md#file-9493e9900dcf8d66) |
| `ShaderNodeRGB` | [Module 06](modules/06-nodes.md) | [reference](../../../../../docs/research-catalog.md#file-7b16df7f22399f49) |
| `ShaderNodeTexCoord` | [Module 06](modules/06-nodes.md) | [reference](../../../../../docs/research-catalog.md#file-8b8037f3bf3e5b8d) |
| `ShaderNodeTexNoise` | [Module 06](modules/06-nodes.md) | [reference](../../../../../docs/research-catalog.md#file-c643051f81562725) |
| `ShaderNodeValue` | [Module 06](modules/06-nodes.md) | [reference](../../../../../docs/research-catalog.md#file-082bc796dae1a2d1) |
| `ShaderNodeVectorMath` | [Module 06](modules/06-nodes.md) | [reference](../../../../../docs/research-catalog.md#file-a1bed9188db5969f) |
| `SolidifyModifier` | [Module 05](modules/05-transforms.md) | [reference](../../../../../docs/research-catalog.md#file-c248042b0eddb337) |
| `Spline` | [Module 05](modules/05-transforms.md) | [reference](../../../../../docs/research-catalog.md#file-c57ada6039f6c734) |
| `SplinePoint` | [Module 05](modules/05-transforms.md) | [reference](../../../../../docs/research-catalog.md#file-ce44ed20c11ca24e) |
| `SubsurfModifier` | [Module 05](modules/05-transforms.md) | [reference](../../../../../docs/research-catalog.md#file-902d576757b680c8) |
| `ViewLayer` | [Module 02](modules/02-data.md) | [reference](../../../../../docs/research-catalog.md#file-33e85222ddb6d5b6) |
| `World` | [Module 07](modules/07-render.md) | [reference](../../../../../docs/research-catalog.md#file-073076078f432341) |
| `bpy_struct` | [Module 02](modules/02-data.md) | [reference](../../../../../docs/research-catalog.md#file-1429b2daf172dc8c) |
| `bmesh.geometry` | [Module 04](modules/04-mesh.md) | [reference](../../../../../docs/research-catalog.md#file-7e1052ae883fe94c) |
| `bmesh` | [Module 04](modules/04-mesh.md) | [reference](../../../../../docs/research-catalog.md#file-cb40ce9c39bbd834) |
| `bmesh.ops` | [Module 04](modules/04-mesh.md) | [reference](../../../../../docs/research-catalog.md#file-06186a240325b796) |
| `bmesh.types` | [Module 04](modules/04-mesh.md) | [reference](../../../../../docs/research-catalog.md#file-8029d1f8e77a2194) |
| `bmesh.utils` | [Module 04](modules/04-mesh.md) | [reference](../../../../../docs/research-catalog.md#file-dc2466ca83e10223) |
| `bpy.app` | [Module 01](modules/01-execution.md) | [reference](../../../../../docs/research-catalog.md#file-b46df65444a74d34) |
| `bpy.context` | [Module 03](modules/03-context.md) | [reference](../../../../../docs/research-catalog.md#file-c97f277e0432785e) |
| `bpy.data` | [Module 02](modules/02-data.md) | [reference](../../../../../docs/research-catalog.md#file-a3b1a2d4571ba905) |
| `bpy.path` | [Module 01](modules/01-execution.md) | [reference](../../../../../docs/research-catalog.md#file-545d81dcc0e38ec0) |
| `mathutils` | [Module 05](modules/05-transforms.md) | [reference](../../../../../docs/research-catalog.md#file-debdcad6d02325f9) |
| `bpy.ops.object` | [Module 03](modules/03-context.md) | [reference](../../../../../docs/research-catalog.md#file-7a5cca00939ced60) |
| `bpy.ops.render` | [Module 08](modules/08-persistence.md) | [reference](../../../../../docs/research-catalog.md#file-d28e244d7afcec4b) |
| `bpy.ops.wm` | [Module 08](modules/08-persistence.md) | [reference](../../../../../docs/research-catalog.md#file-91636dea1a4a8d6b) |
