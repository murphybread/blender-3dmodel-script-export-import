import bpy
import json
import os

def import_objects_from_json(file_path, image_dir, collection_name, scale_factor):
    with open(file_path, 'r') as f:
        objects_data = json.load(f)
    
    # Create or get the collection
    if collection_name in bpy.data.collections:
        collection = bpy.data.collections[collection_name]
    else:
        collection = bpy.data.collections.new(collection_name)
        bpy.context.scene.collection.children.link(collection)
    
    for obj_data in objects_data:
        obj = None  # Initialize obj variable

        if obj_data['type'] == 'MESH':
            # Create a new mesh object
            mesh = bpy.data.meshes.new(obj_data['name'])
            obj = bpy.data.objects.new(obj_data['name'], mesh)
            collection.objects.link(obj)
            bpy.context.view_layer.objects.active = obj
            obj.select_set(True)
            
            # Add vertices and faces
            vertices = [tuple(v) for v in obj_data['vertices']]
            faces = [tuple(face) for face in obj_data['faces']]
            edges = []
            mesh.from_pydata(vertices, edges, faces)
            mesh.update()

            # Add UV mapping
            if 'uvs' in obj_data:
                uv_layer = mesh.uv_layers.new(name="UVMap")
                for i, uv in enumerate(obj_data['uvs']):
                    uv_layer.data[i].uv = tuple(uv)

            # Add materials and textures
            for mat_data in obj_data.get('materials', []):
                mat = bpy.data.materials.get(mat_data['name'])
                if not mat:
                    mat = bpy.data.materials.new(name=mat_data['name'])
                    mat.use_nodes = True  # Ensure use_nodes is enabled
                
                obj.data.materials.append(mat)

                if mat.use_nodes:
                    bsdf = mat.node_tree.nodes.get("Principled BSDF")
                    if not bsdf:
                        bsdf = mat.node_tree.nodes.new(type="ShaderNodeBsdfPrincipled")
                    for tex_data in mat_data['textures']:
                        image_path = os.path.join(image_dir, tex_data['image'])
                        if not os.path.exists(image_path):
                            print(f"Image file not found: {image_path}")
                            continue
                        try:
                            tex_image = bpy.data.images.load(image_path)
                        except Exception as e:
                            print(f"Failed to load image {image_path}: {e}")
                            continue
                        tex_node = mat.node_tree.nodes.new(type="ShaderNodeTexImage")
                        tex_node.image = tex_image
                        mat.node_tree.links.new(tex_node.outputs['Color'], bsdf.inputs['Base Color'])

        elif obj_data['type'] == 'LIGHT':
            # Create a new light object
            light_data = bpy.data.lights.new(name=obj_data['name'], type='POINT')
            obj = bpy.data.objects.new(name=obj_data['name'], object_data=light_data)
            collection.objects.link(obj)

        # Set object properties if obj is not None
        if obj is not None:
            obj.location = obj_data['location']
            obj.scale = [s * scale_factor for s in obj_data['scale']]
            obj.rotation_euler = obj_data['rotation']
            obj.dimensions = obj_data['dimensions']

# Define the file path and image directory relative to the current Blender file
import_file_path = bpy.path.abspath("//exported_objects.json")
image_directory = bpy.path.abspath("//textures")

# Define the collection name and scale factor
collection_name = "ImportedObjects"
scale_factor = 1.0  # Example scale factor to customize the size

# Import objects from JSON and apply custom scale
import_objects_from_json(import_file_path, image_directory, collection_name, scale_factor)
print(f"Imported objects from {import_file_path} into collection '{collection_name}' with scale factor {scale_factor}")
