# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Julian Turner
"""Native .blend collection import; import this module inside Blender only."""
from pathlib import Path
import json
import bpy
from polyhaven import verify


def _asset(directory):
    root = Path(directory).expanduser().resolve()
    receipt = verify(root)
    source = root / receipt['main_file']
    if source.suffix.lower() != '.blend':
        raise ValueError('This helper appends .blend collections; use native APIs for other formats')
    return root, receipt, source


def list_datablocks(directory):
    """Verify downloaded bytes; list source collection/object names without appending."""
    _, receipt, source = _asset(directory)
    with bpy.data.libraries.load(str(source), link=False) as (available, requested):
        result = {'asset_id':receipt['asset_id'], 'collections':list(available.collections),
                  'objects':list(available.objects), 'materials':list(available.materials)}
    return result


def append_collection(directory, name, *, pack_images=True):
    """Append one named collection, retain provenance, optionally pack its new images.

    Runs synchronously in Blender. Returns the new Collection; does not save/render.
    Repeated calls append new data. An exception may follow partial scene mutation.
    Automatic script execution should be disabled by the calling Blender command.
    """
    root, receipt, source = _asset(directory)
    old_images = {image.as_pointer() for image in bpy.data.images}
    with bpy.data.libraries.load(str(source), link=False) as (available, requested):
        if name not in available.collections:
            raise ValueError(f'No collection {name!r}; available: {list(available.collections)}')
        requested.collections = [name]
    collection = requested.collections[0]
    if collection is None: raise RuntimeError('Blender did not append the selected collection')
    bpy.context.scene.collection.children.link(collection)
    collection['polyhaven_asset_id'] = receipt['asset_id']
    collection['polyhaven_asset_page'] = receipt['asset_page']
    collection['polyhaven_license'] = receipt['license']
    collection['polyhaven_variant'] = receipt['variant']
    text = bpy.data.texts.new('PolyHaven/' + receipt['asset_id'] + '/provenance.json')
    text.from_string(json.dumps(receipt, indent=2))
    collection['polyhaven_provenance_text'] = text.name
    if pack_images:
        for image in bpy.data.images:
            if image.as_pointer() not in old_images and image.source == 'FILE':
                path = Path(bpy.path.abspath(image.filepath, library=image.library)).resolve()
                if not path.is_relative_to(root) or not path.is_file():
                    raise ValueError(f'Image outside verified acquisition: {image.name}: {path}')
                allowed = {str((root / e['path']).resolve()) for e in receipt['files']}
                if str(path) not in allowed:
                    raise ValueError(f'Undeclared image dependency: {path}')
                image.pack()
                if not image.packed_file:
                    raise RuntimeError(f'Image did not pack: {image.name}')
    bpy.context.view_layer.update()
    return collection
