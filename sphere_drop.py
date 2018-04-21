# -*- coding: utf-8 -*-

# import
import bpy

# config
FRAME        = {"start": 0, "end": 200}
BLOCK_NUMBER = {"x": 6, "y": 6, "z": 30}
BLOCK_SIZE   = {"x": 0.5, "y": 0.5, "z": 1.5}

# color
START_COLOR  = {"r": 75,  "g": 0,   "b": 130}
END_COLOR    = {"r": 25,  "g": 25,  "b": 112}
FLOOR_COLOR  = {"r": 0,   "g": 250, "b": 154}
SPHERE_COLOR = {"r": 255, "g": 215, "b": 0}

# mass
BLOCK_MASS = 1000
SHERE_MASS = 100000

# const
FIELD_SIZE = {"x": BLOCK_NUMBER["x"] * BLOCK_SIZE["x"], "y": BLOCK_NUMBER["y"] * BLOCK_SIZE["y"], "z": BLOCK_NUMBER["z"] * BLOCK_SIZE["z"]}

def set_frame_size(start_frame, end_frame):
    bpy.context.scene.frame_start = start_frame
    bpy.context.scene.frame_end   = end_frame

def delete_all_objects():
    for item in bpy.context.scene.objects:
        bpy.context.scene.objects.unlink(item)

def create_cube(x, y, z):
    cube = create_primitive_cube(x, y, z)
    add_color_material(cube, x, y, z)

def create_primitive_cube(x, y, z):
    pos_x = x * BLOCK_SIZE["x"] - BLOCK_SIZE["x"] * 0.5
    pos_y = y * BLOCK_SIZE["y"] - BLOCK_SIZE["y"] * 0.5
    pos_z = z * BLOCK_SIZE["z"] * 0.98 + BLOCK_SIZE["z"] * 0.5 # 原因不明だが縦にわずかな隙間ができるので×0.98する
    bpy.ops.mesh.primitive_cube_add(location=(pos_x, pos_y, pos_z), rotation=(0,0,0))
    bpy.ops.rigidbody.object_add()
    obj = bpy.context.scene.objects.active
    obj.rigid_body.angular_damping = 0
    obj.rigid_body.mass = BLOCK_MASS
    obj.scale = (BLOCK_SIZE["x"] * 0.5, BLOCK_SIZE["y"] * 0.5, BLOCK_SIZE["z"] * 0.5)
    return obj

def add_color_material(obj, x, y, z):
    new_colors = {}
    for key in ["r", "g", "b"]:
        new_colors[key] = color_with_gradation(key, x, y, z)

    mat = bpy.data.materials.new('Cube')
    mat.diffuse_color = (new_colors["r"], new_colors["g"], new_colors["b"])
    obj.data.materials.append(mat)

def color_with_gradation(key, x, y, z):
    now_step = x + y + z
    max_step = BLOCK_NUMBER["x"] + BLOCK_NUMBER["y"] + BLOCK_NUMBER["z"]
    if max_step < 1:
        return START_COLOR[key]
    color_diff = END_COLOR[key] - START_COLOR[key]
    return (START_COLOR[key] + (color_diff / max_step) * now_step) / 255

def create_floor():
    pos_x = FIELD_SIZE["x"] * 0.5
    pos_y = FIELD_SIZE["y"] * 0.5
    pos_z = 0
    bpy.ops.mesh.primitive_plane_add(location=(pos_x, pos_y, pos_z))
    bpy.ops.rigidbody.object_add(type='PASSIVE')
    obj = bpy.context.scene.objects.active
    obj.scale = (FIELD_SIZE["x"] * 3, FIELD_SIZE["y"] * 3, 1)
    obj.rigid_body.collision_margin = 0
    mat = bpy.data.materials.new('Floor')
    mat.diffuse_color = (FLOOR_COLOR["r"] / 255, FLOOR_COLOR["g"] / 255, FLOOR_COLOR["b"] / 255)
    obj.data.materials.append(mat)

def create_sphere():
    pos_x = FIELD_SIZE["x"] * 0.5
    pos_y = FIELD_SIZE["y"] * 0.5
    pos_z = FIELD_SIZE["z"] + BLOCK_SIZE["z"] * 3
    bpy.ops.mesh.primitive_uv_sphere_add(location=(pos_x, pos_y, pos_z))

    bpy.ops.rigidbody.object_add()
    obj = bpy.context.scene.objects.active
    obj.rigid_body.angular_damping = 0
    obj.rigid_body.mass = SHERE_MASS
    obj.rigid_body.restitution = 1
    
    scale = BLOCK_NUMBER["x"] * 0.8
    obj.scale = (scale, scale, scale)
    mat = bpy.data.materials.new('Shpere')
    mat.diffuse_color = (SPHERE_COLOR["r"] / 255, SPHERE_COLOR["g"] / 255, SPHERE_COLOR["b"] / 255)
    obj.data.materials.append(mat)

def set_camera():
    camera_range = FIELD_SIZE["z"] * 1.2
    x_pos = camera_range
    y_pos = camera_range * -1
    z_pos = camera_range
    bpy.ops.object.camera_add(
        location=(x_pos, y_pos, z_pos),
        rotation=(1.2, 0, 0.75)
    )
    obj = bpy.context.scene.objects.active
    bpy.context.scene.camera = obj

def set_lamp():
    x_pos = 0
    y_pos = 0
    z_pos = 0
    bpy.ops.object.lamp_add(
        location=(x_pos, y_pos, z_pos),
        rotation=(0.79, 0, 0),
        type = "SUN"
    )

def create_blocks():
    for x in range(1, BLOCK_NUMBER["x"] + 1):
        for y in range(1, BLOCK_NUMBER["y"] + 1):
            # 外周のブロックだけ作る
            if x > 1 and x < BLOCK_NUMBER["x"] and y > 1 and y < BLOCK_NUMBER["y"]:
                continue
            for z in range(0, BLOCK_NUMBER["z"]):
                create_cube(x, y, z)

# main
set_frame_size(FRAME["start"], FRAME["end"])
delete_all_objects()
create_blocks()
create_sphere()
create_floor()
set_camera()
set_lamp()
