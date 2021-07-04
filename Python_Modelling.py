import bpy
from math import *

#VARIABLES!!!
obj = bpy.ops.object

cam_loc_x = 0 #CAMERA'S 'X' LOCATION
cam_loc_y = -5 #CAMERA'S 'Y' LOCATION
cam_loc_z = 1 #CAMERA'S 'Z' LOCATION

cam_rot_x = radians(90) #CAMERA'S 'X' ROTATION
cam_rot_y = radians(0) #CAMERA'S 'Y' ROTATION
cam_rot_z = radians(0) #CAMERA'S 'Z' ROTATION

light_energy = 100

#Selects all the objects.
obj.select_all(action='SELECT')

#Deletes the selected objects
obj.delete(use_global=False)
#Adds a camera.
obj.camera_add(location = (cam_loc_x, cam_loc_y, cam_loc_z), rotation = (cam_rot_x, cam_rot_y, cam_rot_z))

#Sets the camera as an active camera.
for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        override = bpy.context.copy()
        override['area'] = area
        bpy.ops.view3d.object_as_camera(override)
        break
#MONKEY
#Adds a Monkey.
bpy.ops.mesh.primitive_monkey_add(location = (0, 0, 1))

#Adds a subsurf modifier to the monkey.
obj.modifier_add(type='SUBSURF')
bpy.context.object.modifiers["Subdivision"].render_levels = 3
bpy.context.object.modifiers["Subdivision"].levels = 3
obj.shade_smooth()


#Adds a texture to the monkey.
ob = bpy.context.active_object

# Get material
mat = bpy.data.materials.get("Material")
if mat is None:
    # create material
    mat = bpy.data.materials.new(name="Material")

# Assign it to object
if ob.data.materials:
    # assign to 1st material slot
    bpy.context.active_object.data.materials[0] = mat
else:
    # no slots
    bpy.context.active_object.data.materials.append(mat)

bpy.data.materials["Material"].node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.0324292, 0.8, 0.400046, 1)


#BG_Plane.
#Scale_Variable
plane_scale = 5

#Adds a plane.
bpy.ops.mesh.primitive_plane_add(location = (0, 3, 1), rotation = (radians(90), 0, 0))

#Scales the plane (by the variable 'plane_scale').
bpy.ops.transform.resize(value=(plane_scale, plane_scale, plane_scale), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)


#LIGHTING!!!
#Left lamp.
bpy.ops.object.light_add(type='POINT', align='WORLD', location=(-2, -2, 1), scale=(1, 1, 1))
bpy.context.object.data.energy = light_energy

bpy.ops.object.light_add(type='POINT', align='WORLD', location=(2, -2, 1), scale=(1, 1, 1))
bpy.context.object.data.energy = light_energy

bpy.ops.object.light_add(type='POINT', align='WORLD', location=(0, -2, 3), scale=(1, 1, 1))
bpy.context.object.data.energy = light_energy/2

bpy.ops.object.light_add(type='POINT', align='WORLD', location=(0, -2, -1), scale=(1, 1, 1))
bpy.context.object.data.energy = light_energy/2



#Changes the render engine to cycles.
bpy.context.scene.render.engine = 'CYCLES'

#Change the render resolution.
bpy.context.scene.render.resolution_x = 1920
bpy.context.scene.render.resolution_y = 1920


#Render!
bpy.ops.render.render('INVOKE_DEFAULT', animation=False, write_still=True, use_viewport=False, scene="scene")

