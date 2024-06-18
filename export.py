import bpy
import json
import os
from datetime import datetime

def export_image(image, filepath):
    image.filepath_raw = filepath
    image.file_format = 'PNG'
    image.save()

def export_selected_objects_to_json(file_path, image_dir):
    selected_objects = bpy.context.selected_objects
    objects_data = []

    if not os.path.exists(image_dir):
        os.makedirs(image_dir)

    for obj in selected_objects:
        print(f"Processing object: {obj.name} of type {obj.type}")
        if obj is None:
            print("Skipping None object")
            continue  # Skip if obj is None
        if obj.type != 'MESH':
            print(f"Skipping object {obj.name} because it is not a MESH")
            continue  # Skip if obj is not a MESH
        if obj.data is None:
            print(f"Skipping object {obj.name} because it has no data")
            continue  # Skip if obj has no data

        obj_data = {
            'name': obj.name,
            'location': list(obj.location),
            'scale': list(obj.scale),
            'rotation': list(obj.rotation_euler),
            'type': obj.type,
            'dimensions': list(obj.dimensions),
        }

        # Save mesh-specific data
        mesh = obj.data
        vertices = [list(v.co) for v in mesh.vertices]
        faces = [list(face.vertices) for face in mesh.polygons]
        if mesh.uv_layers.active is not None:
            uvs = [list(uv.uv) for uv in mesh.uv_layers.active.data]
        else:
            uvs = []
        obj_data['vertices'] = vertices
        obj_data['faces'] = faces
        obj_data['uvs'] = uvs

        # Save material and texture data
        materials = []
        for mat_slot in obj.material_slots:
            if mat_slot.material:
                mat = mat_slot.material
                mat_data = {
                    'name': mat.name,
                    'use_nodes': mat.use_nodes,
                    'textures': []
                }
                if mat.use_nodes:
                    for node in mat.node_tree.nodes:
                        if node.type == 'TEX_IMAGE' and node.image:
                            image_name = f"{node.image.name}.png"
                            image_path = os.path.join(image_dir, image_name)
                            export_image(node.image, image_path)
                            tex_data = {
                                'name': node.name,
                                'type': node.type,
                                'image': image_name
                            }
                            mat_data['textures'].append(tex_data)
                materials.append(mat_data)
        obj_data['materials'] = materials

        objects_data.append(obj_data)
    
    with open(file_path, 'w') as f:
        json.dump(objects_data, f, indent=4)

# Define the file path and image directory
export_file_path = bpy.path.abspath("//exported_objects.json")
image_directory = bpy.path.abspath("//textures")

# Export selected objects to JSON
export_selected_objects_to_json(export_file_path, image_directory)
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(f"Exported selected objects to {export_file_path} at {current_time}")
