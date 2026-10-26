# 07. Materials and rendered inspection

## Purpose and prerequisites

Specify repeatable visual feedback without mistaking an attractive image for geometric verification. Read [evaluation](03-context.md), [transforms](05-transforms.md) and [node graphs](06-nodes.md). References: [Material](https://docs.blender.org/api/5.2/bpy.types.Material.html), [Camera](https://docs.blender.org/api/5.2/bpy.types.Camera.html), [Light](https://docs.blender.org/api/5.2/bpy.types.Light.html), [World](https://docs.blender.org/api/5.2/bpy.types.World.html), [RenderSettings](https://docs.blender.org/api/5.2/bpy.types.RenderSettings.html), [color management](https://docs.blender.org/manual/en/5.2/render/color_management/index.html).

## Mental model and invariants

A render combines evaluated geometry, materials, lighting, camera, engine settings, view-layer filtering, color transforms and output encoding. A PNG is a projection of that combined state. It cannot establish dimensions, watertight topology, unseen back faces or editable structure. Use it alongside numeric inspection of the evaluated mesh and scene metadata. [C20 - C22](../CLAIMS.md#c20).

Cycles CPU is the reference device choice, not a benchmark conclusion. Fix the engine/device and important options explicitly; loaded files, startup settings and differing node defaults can change the result. Disable denoising for the initial geometric reference so its reconstruction cannot conceal a thin feature. This is an inspection policy, not a claim that denoising is always unsuitable.

## API contracts

### Materials and assignment

`bpy.data.materials.new(name)` creates a Material ID; pinned creation supplies default shader nodes. `material.node_tree` owns its graph. `Material.use_nodes` is deprecated compatibility surface in this series, not the switch to rely on. Inspect and build the intended tree. `Material.diffuse_color` is a viewport/display property and is not a substitute for the Principled BSDF Base Color.

```python
# UNEXECUTED: build a deliberately simple surface on a new material.
mat = bpy.data.materials.new('InspectionGray')
nt = mat.node_tree
nt.nodes.clear()
bsdf = nt.nodes.new('ShaderNodeBsdfPrincipled')
out = nt.nodes.new('ShaderNodeOutputMaterial')
out.is_active_output = True
bsdf.inputs['Base Color'].default_value = (0.35, 0.35, 0.35, 1.0)
bsdf.inputs['Metallic'].default_value = 0.0
bsdf.inputs['Roughness'].default_value = 0.65
bsdf.inputs['Alpha'].default_value = 1.0
nt.links.new(input=out.inputs['Surface'], output=bsdf.outputs['BSDF'])
obj.data.materials.append(mat)
```

`nodes.clear()` removes nodes and links in **this newly owned tree**; do not run it on an unrelated shared material. Principled's other lobe weights retain the pinned node's zero defaults in this new material; a reused material requires explicit reset or reconstruction. `obj.data.materials.append(mat)` adds a material slot; `MeshPolygon.material_index` chooses that slot, zero-based. `Object.material_slots[i].link='OBJECT'` can override the shared Mesh's slot at object level. A material list created by evaluated Geometry Nodes may differ from original slots; inspect evaluated material assignment when exporting.

Values entering shader colors are interpreted in the scene's working color space. A Python tuple is not tagged as an sRGB hex color. Decode display-encoded color values deliberately if that is the input contract. The example's neutral numeric value is a working-space choice, not a calibrated material measurement.

### Camera, lights and world

A Camera datablock defines projection; an Object places it. `bpy.data.cameras.new` returns the data; `bpy.data.objects.new(name, camera_data)` returns its Object; link it to the scene and set `scene.camera` to the **Object**. Camera local −Z looks forward and local +Y supplies up in the usual aiming recipe. `Camera.type='ORTHO'` removes perspective size variation; `ortho_scale` sets the projection span in scene units with image aspect involved. `PERSP` uses focal length (`lens`, millimeters) and sensor settings. `shift_x/shift_y` offset framing. `clip_start/clip_end` bound visible distances. DOF (`camera.dof.use_dof`) blurs depth and should be off for the initial inspection view.

`bpy.data.lights.new(name, type='AREA')` creates area-light data. `energy` is radiometric power under the documented light model, not the electrical rating of a lamp. `shape`, `size`, `size_y` and `normalize` change extent/intensity behavior; choose them explicitly. A larger area softens shadows and can conceal small gaps; a tiny light creates harsh shadows that can suggest false creases. Place and aim the Light Object rather than assigning location to the Light datablock. SUN lights use direction rather than point-source falloff and have different units; they are not used in the reference example.

`scene.world` points to a World ID. A World shader supplies environmental lighting/background; it can illuminate hidden-facing surfaces or wash out relief. The bounded world graph uses `ShaderNodeBackground` (Color and Strength → Background shader) linked to `ShaderNodeOutputWorld.Surface`, with the output active. These two necessary World dependencies were added to the manifest explicitly; they do not expand the material palette into a general shader survey. `World.color` alone is not the intended node-shader configuration.

[inspection.py](../examples/inspection.py) contains an unexecuted neutral material, orthographic camera, area light and constant world setup. Its numeric placements are illustrative, not an automatic framing algorithm for arbitrary scenes. A future job must calculate framing from evaluated bounds, set near/far clipping appropriately and choose multiple views where occlusion matters.

### Cycles and output settings

```python
# UNEXECUTED: configure a still; no render is launched by this fragment.
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.device = 'CPU'
scene.cycles.samples = 64
scene.cycles.use_denoising = False
scene.cycles.use_adaptive_sampling = False
scene.render.resolution_x = 768
scene.render.resolution_y = 768
scene.render.resolution_percentage = 100
scene.render.pixel_aspect_x = scene.render.pixel_aspect_y = 1.0
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGBA'
scene.render.image_settings.color_depth = '8'
scene.render.image_settings.compression = 15
scene.render.use_file_extension = True
scene.render.filepath = '/absolute/new-job/inspection.png'
```

`scene.cycles` is registered by Blender's bundled Cycles integration. `device='CPU'` chooses CPU path tracing; a command-line `--cycles-device` override can supersede scene/preferences, so don't supply one inconsistently. `samples=64` is an example budget, not a measured adequacy threshold. Adaptive sampling changes the number of samples by convergence; disabling it makes the requested sampling policy simpler. `use_denoising=False` also avoids a separate denoiser/device policy affecting inspection. CPU selection does not imply every application component avoids GPU/display libraries.

Resolution is width/height in pixels multiplied by `resolution_percentage`; pixel aspect affects image geometry. `ImageFormatSettings.file_format='PNG'` chooses output encoding, `RGBA` retains alpha, `color_depth='8'` is bits per channel, and PNG `compression` trades storage/encoding work without JPEG-style loss. Sixteen-bit PNG is available where desired; neither encoding restores clipped highlights or proves linear radiometric values. `use_file_extension` allows Blender to append the correct suffix. Use a full filename in a fresh directory and avoid path templates for the reference still.

A controlled still should also decide: `use_border=False`, `use_crop_to_border=False`, `use_sequencer=False`, `use_compositing=False`, `use_simplify=False`, `film_transparent=False`, motion blur off, depth of field off, material/world overrides absent, relevant objects not `hide_render`, appropriate ViewLayer inclusion, and matching modifier render settings. Some options are engine- or context-dependent; validate RNA on the fixed build rather than silently skipping a missing property.

### Color management and misleading appearance

The scene's working space, display device and view transform are different controls. `scene.display_settings.display_device='sRGB'` chooses a display target; `scene.view_settings.view_transform='AgX'` chooses a view transform; `look`, `exposure`, `gamma` and curves further alter display. AgX's highlight compression is useful for ordinary visualization but not linear numeric measurement. Exposure is measured in stops; gamma changes tonal response. Set exposure zero/gamma one and disable custom curves for the reference. Validate a look's exact enum against the effective OCIO configuration instead of guessing `'None'` versus `'NONE'`.

`scene.render.image_settings.color_management='FOLLOW_SCENE'` uses scene output color settings where supported. Image input color-space settings describe how external pixels are interpreted; a texture interpreted as color is different from non-color data. No external image textures are required here. `OCIO`/`BLENDER_OCIO` overrides and missing configurations can change available choices; record the actual names used. The review does not alter the installed color configuration.

Misleading signals include smooth shading on coarse topology, reflective materials exaggerating normal discontinuities, transparent/transmissive surfaces hiding thickness, clipping cutting off parts, orthographic projection hiding depth, compositing changing silhouettes, denoising removing thin structures, and low sample noise resembling roughness. No single preset removes every ambiguity; compare images with mesh counts, bounds, normals and expected topology.

### Execute and verify a still

`bpy.ops.render.render('EXEC_DEFAULT', animation=False, write_still=True)` runs the execute path synchronously. `write_still=True` requests disk output; merely obtaining a Render Result does not imply a PNG was saved. A missing camera, invalid image format, path error or cancellation can report failure. The operation's reports/status are necessary but insufficient evidence of a fresh correct output. Verify a fresh path, PNG signature/dimensions and job association after return. [Persistence](08-persistence.md), [recovery](09-revision.md).

Render handlers run around the operation and may affect lifecycle. A “render complete” handler is not a durable-output receipt. `scene.cycles.time_limit` bounds a rendering component, not total process runtime. `use_persistent_data` retains some data between renders in one process; it gives no interprocess state persistence.

## Implementation traces

`engine.py:1 - 140` passes process mode, parses Cycles overrides and creates/resets/renders/frees a native session. `properties.py:381 - 436,485 - 516` defines CPU, denoising and sample defaults. `render_internal.cc:236 - 355` checks scene/format, invokes synchronous rendering and maps cancellation. `pipeline.cc:1925 - 2009` controls still writing, path-template errors and callbacks; `2178 - 2248` invokes image writing and retains a success flag. Shader declarations establish socket types/defaults, not integrator correctness. [Pinned ranges](../SOURCE_TRACES.md).

## Failure modes and diagnosis

| Symptom | Inspect before changing geometry |
|---|---|
| Black image | Active camera, lights, world, material output, clipping, object/view-layer visibility |
| Unexpected crop/aspect | Border/crop, resolution percentage, pixel aspect, camera shift |
| Thin feature missing | Projection, sampling, denoising, shader alpha, near clip and topology |
| Render returned but no new PNG | `write_still`, filepath/suffix, reports, fresh output directory and actual file metadata |
| Pink/magenta or changed colors | Missing external resources/configuration and color-space mismatch |
| CPU policy appears ignored | Cycles CLI override or separate denoising configuration |

## Evidence and open questions

D/S support configuration and execute/write boundaries. I chooses the neutral inspection recipe. No sample count, framing adequacy, render time or pixel determinism was measured. [T08](../FUTURE_TESTS.md) must verify missing output, unwritable paths, failure status and stale-file rejection. PNG header checks alone do not validate visual correctness.
