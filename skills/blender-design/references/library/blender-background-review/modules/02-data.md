# 02. Data ownership and scene structure

## Purpose and prerequisites

Determine what an object actually owns and which operations invalidate references. Read [execution](01-execution.md); then [evaluation](03-context.md). Core references: [bpy.data](https://docs.blender.org/api/5.2/bpy.data.html), [ID](https://docs.blender.org/api/5.2/bpy.types.ID.html), [Object](https://docs.blender.org/api/5.2/bpy.types.Object.html), [Collection](https://docs.blender.org/api/5.2/bpy.types.Collection.html), [Scene](https://docs.blender.org/api/5.2/bpy.types.Scene.html).

## Mental model and invariants

Blender's main database contains typed **ID datablocks**: objects, meshes, materials, scenes, collections, curves and node groups. Python variables are wrappers around Blender-owned data. Reference count in Python is not the datablock's Blender `users` count. Deleting a Python variable releases a wrapper; it does not perform `bpy.data.objects.remove`.

An Object provides placement, parenting, modifiers and object-specific settings. `Object.data` points to its geometry or other payload. Two Objects may point to the same Mesh. Collections link Objects; the same Object can belong to several Collections without being duplicated. A Scene's master Collection roots a hierarchy. A ViewLayer describes a view of that hierarchy, including exclusions and the active object. Membership in `bpy.data.objects` alone does not make an object visible in the active scene or render. [C04](../CLAIMS.md#c04).

A material may be shared by many meshes. A node group can be shared by modifiers. A mesh's material slots and face material indices are distinct: an index selects a slot, which holds a material reference. An object-level material override is another layer. An object's copy does not automatically recursively clone every referenced ID.

### Lifetime table

| Representation | Owner | Safe persistence boundary |
|---|---|---|
| Original ID in `bpy.data` | Blender's Main database | Survives Python function return; can persist in `.blend` if retained |
| Object's `modifiers`, curve splines, mesh vertices | Parent ID/container | Invalidated by removal or relevant container reallocation; not independently owned IDs |
| Evaluated Object/Mesh | Dependency graph | Temporary; reacquire after evaluation changes |
| `Object.to_mesh()` result | Object's temporary conversion slot | Until `to_mesh_clear`, another `to_mesh` on that Object, or owner invalidation |
| Owned `bmesh.new()` | Python caller's explicit allocation | Until `free`; write back first if needed |
| `bmesh.from_edit_mesh()` result | Blender's Edit Mode mesh | Do not free as a caller-owned BMesh |
| Copied tuple/`Vector.copy()` | Python | Independent numeric snapshot, not an editable scene link |

## API contracts

### Construct and link

```python
# UNEXECUTED: a datablock skeleton; no geometry is filled here.
import bpy

collection = bpy.data.collections.new('Procedure')
bpy.context.scene.collection.children.link(collection)
mesh = bpy.data.meshes.new('BodyMesh')
obj = bpy.data.objects.new('Body', mesh)
collection.objects.link(obj)
obj['review_owner'] = 'procedural-object-v1'
obj['part_key'] = 'body'
```

`BlendDataCollections.new(name)` creates a Collection ID; `CollectionChildren.link(collection)` links it into the scene's hierarchy. `BlendDataMeshes.new(name)` creates an empty Mesh ID. `BlendDataObjects.new(name, object_data)` makes an Object referencing an appropriate original datablock; `None` makes an Empty. `CollectionObjects.link(obj)` links an existing Object and increments relevant Blender usage. It does not copy the object or mesh. No active selection is required for these direct-data operations. Linking an already linked Object reports an error, so repeated construction needs a lookup policy.

The square-bracket assignments create ID custom properties, distinct from built-in RNA attributes. They are this example's application metadata, not Blender-recognized ownership enforcement. Names can be uniquified; inspect the returned ID and retain it, rather than assuming the requested name was granted. A name is useful for presentation, not immutable identity.

### Share or copy deliberately

```python
# UNEXECUTED: requires `obj` and `collection` above.
shared = obj.copy()
collection.objects.link(shared)
independent = obj.copy()
independent.data = obj.data.copy()
collection.objects.link(independent)
```

`ID.copy()` returns a new original ID in Main where supported. `Object.copy()` copies object-level state while referenced mesh data remains shared. Assigning `independent.data = obj.data.copy()` gives independent geometry but can still share referenced Materials. Node groups in copied modifiers may also be shared. Editing shared mesh vertex positions affects all object users; editing one Object's transform does not change the other Object's transform. Copy each required layer deliberately and make the choice part of the parameters. [C05](../CLAIMS.md#c05).

`ID.users` counts Blender users, not a proof that a datablock belongs exclusively to your job. `use_fake_user` retains otherwise unused data through file saving; it is a preservation flag, not semantic ownership. `ID.session_uid` is a session identity aid, not a stable cross-process application key. `ID.library`, `is_editable`, `is_evaluated` and `original` help distinguish linked, editable and evaluated data. The bounded recipes require original local editable IDs; linked library overrides are a separate workflow.

### Remove safely

`bpy.data.objects.remove(obj, do_unlink=True)` removes the Object and unlinks its uses. The Python wrapper becomes invalid. Its Mesh can remain in Main with zero users. `bpy.data.meshes.remove(mesh, do_unlink=True)` is more consequential: objects that require that mesh may also be deleted because their data pointer cannot remain null. Do not treat it as an interchangeable way to delete “only geometry.” `do_unlink=False` rejects removal while real users remain. The `do_id_user` and `do_ui_user` flags govern user accounting and UI references; leave them at the documented defaults rather than disabling safety bookkeeping. [C06](../CLAIMS.md#c06).

```python
# UNEXECUTED: only for a verified job-owned local mesh object.
mesh = obj.data
bpy.data.objects.remove(obj, do_unlink=True)
# Do not read obj.name or obj.data here: obj has been invalidated.
if mesh.users == 0 and mesh.get('review_owner') == 'procedural-object-v1':
    bpy.data.meshes.remove(mesh)
```

This cleanup deliberately requires a marker on the **mesh**, not merely its former object. The earlier skeleton did not mark its mesh, so this particular cleanup would preserve that mesh. A real constructor must mark each ID it intends to own. A `.get` result is not evidence against malicious or accidental marker duplication; the revision module requires ambiguity checks.

Avoid `ID.user_clear`, global orphan purges and unscoped `batch_remove` as routine cleanup. They can break users or remove unrelated zero-user assets. There is no reason to change user counts manually when typed collection removal performs the necessary bookkeeping.

### References and containers

`bpy_struct` supplies RNA introspection (`bl_rna`, `path_from_id`, `path_resolve`), ID-owner access (`id_data`), and custom-property operations on supported types. A path is a lookup expression inside current data, not a durable pointer. `bpy_prop_collection.get(name)` returns a member or a default; indexing a missing name raises `KeyError`. `find(name)` returns an index or `-1`; do not use `-1` as successful lookup. `foreach_get/foreach_set` bulk-transfer a named numeric property; they require the exact flattened length and supported basic type, not arbitrary Python objects.

Copy a collection to a Python list before removing or renaming its members, but remember that list items are still wrappers that can become invalid. Copy numeric vectors and matrices before changing their owning data. A live vector can wrap RNA memory; a snapshot should use `.copy()` or a tuple. Re-entering Edit Mode, growing a spline's point array, replacing Mesh geometry, deleting data, loading a file and factory-resetting can invalidate different layers of references. Reacquiring the top-level ID does not resurrect old vertex references.

## Implementation traces

`rna_main_api.cc:115 - 172` checks membership/users, calls deletion and invalidates RNA; `246 - 298` rejects evaluated IDs as new object data and increments usage. `lib_id_delete.cc:259 - 362` removes IDs from Main, remaps references and adds never-null users to the deletion set. This substantiates the mesh-removal cascade. `rna_collection.cc:134 - 178` reports duplicate/missing membership and tags dependency relationships. `rna_ID.cc:757 - 782` delegates evaluated lookup and copy. [Pinned ranges](../SOURCE_TRACES.md).

## Failure modes and diagnosis

- **`ReferenceError: StructRNA ... has been removed`:** the wrapper outlived its Blender data. Find the remove/reset/load boundary; do not catch and keep using it.
- **Silent edits to another object:** inspect `obj.data is other.data`, shared materials and node groups.
- **Object exists but is absent:** check scene Collection membership, ViewLayer exclusion, object/render visibility and active scene.
- **`.001` duplicates after rerun:** creation was unconditional or lookup used a mutable name.
- **Wrong ID edited after copy:** custom ownership keys were copied too. Assign a new part key to intentional duplicates or reject ambiguous matches.
- **Unlinking appears not to delete:** unlink removes one relationship; typed datablock removal deletes the ID.

## Evidence and open questions

D/S support ownership, reference invalidation and deletion behavior. I supplies the application marker and cleanup policy. No marker scheme was tested. [T03](../FUTURE_TESTS.md) covers repeated execution and shared/independent data; [T06](../FUTURE_TESTS.md) covers persistence. The precise invalidation point for every nested RNA array is not exhaustively audited; use the conservative rule of reacquiring after structural mutation.
