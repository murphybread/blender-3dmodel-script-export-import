import bpy
import math

# Function to create a simple house
def create_house(location):
    bpy.ops.mesh.primitive_cube_add(size=2, location=location)
    house = bpy.context.object
    house.scale[2] = 1.5
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value":(0, 0, 1)})
    bpy.ops.object.editmode_toggle()
    return house

# Function to create a palm tree
def create_palm_tree(location):
    # Create trunk
    bpy.ops.mesh.primitive_cylinder_add(radius=0.2, depth=5, location=location)
    trunk = bpy.context.object
    
    # Create leaves
    bpy.ops.mesh.primitive_plane_add(size=2, location=(location[0], location[1], location[2] + 2.5))
    leaf = bpy.context.object
    leaf.scale[1] = 0.2
    leaf.rotation_euler[0] = math.radians(45)
    
    # Duplicate leaves
    for i in range(1, 5):
        new_leaf = leaf.copy()
        new_leaf.data = leaf.data.copy()
        new_leaf.rotation_euler[2] = math.radians(72 * i)
        bpy.context.collection.objects.link(new_leaf)

    return trunk

# Create house at origin
create_house((0, 0, 1))

# Create two palm trees
create_palm_tree((3, 3, 2.5))
create_palm_tree((-3, 3, 2.5))
