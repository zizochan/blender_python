# -*- coding: utf-8 -*-

# import
import bpy

# config
FRAME  = {"start": 0, "end": 400}
BLOCK_NUMBER = {"x": 5, "y": 8, "z": 7}
BLOCK_SIZE   = {"x": 5, "y": 1, "z": 5}
BLOCK_MARGIN = {"x": 0, "y": 5, "z": 0}

# color
START_COLOR  = {"r": 255, "g": 0,   "b": 255}
END_COLOR    = {"r": 0,   "g": 127, "b": 255}
FLOOR_COLOR  = {"r": 173, "g": 255, "b": 47}
SPHERE_COLOR = {"r": 255, "g": 215, "b": 0}
SLOPE_COLOR  = {"r": 0,   "g": 100, "b": 0}
WORLD_COLOR  = {"r": 176, "g": 196, "b": 222}

# mass
BLOCK_MASS = 1000

# movie
MOVIE_NAME = "mymovie.avi"
MOVIE_RESOLUTION_X = 1920
MOVIE_RESOLUTION_Y = 1080
MOVIE_RESOLUTION_PERCENTAGE = 100

# camera
CAMERA_CLIP_END = 500
CAMERA_MARGIN = 1.5

# gravity
GRAVITY_MAGNIFICATION = 1

# const
SPHERE_MASS = BLOCK_MASS * 10000
BLOCK_SPACE = {"x": BLOCK_SIZE["x"] + BLOCK_MARGIN["x"], "y": BLOCK_SIZE["y"] + BLOCK_MARGIN["y"], "z": BLOCK_SIZE["z"] + BLOCK_MARGIN["z"]}
FIELD_SIZE  = {"x": BLOCK_NUMBER["x"] * BLOCK_SPACE["x"], "y": BLOCK_NUMBER["y"] * BLOCK_SPACE["y"], "z": BLOCK_NUMBER["z"] * BLOCK_SPACE["z"]}

def set_frame_size(start_frame, end_frame):
    bpy.context.scene.frame_start = start_frame
    bpy.context.scene.frame_end   = end_frame
    bpy.context.scene.rigidbody_world.point_cache.frame_end = end_frame

def delete_all_objects():
    for item in bpy.context.scene.objects:
        bpy.context.scene.objects.unlink(item)

def create_floor():
    pos_x = FIELD_SIZE["x"] * 0.5
    pos_y = FIELD_SIZE["y"] * 0.5
    pos_z = 0
    bpy.ops.mesh.primitive_plane_add(location=(pos_x, pos_y, pos_z))
    bpy.ops.rigidbody.object_add(type='PASSIVE')
    obj = bpy.context.scene.objects.active
    obj.scale = (FIELD_SIZE["x"] * 5, FIELD_SIZE["y"] * 2, 1)
    obj.rigid_body.collision_margin = 0
    mat = bpy.data.materials.new('Floor')
    mat.diffuse_color = get_color(FLOOR_COLOR)
    obj.data.materials.append(mat)

def create_cube(x, y, z):
    cube = create_primitive_cube(x, y, z)
    add_color_material(cube, x, y, z)

def create_primitive_cube(x, y, z):
    pos_x = x * BLOCK_SPACE["x"] * 2
    pos_y = y * BLOCK_SPACE["y"] * 2
    pos_z = z * BLOCK_SPACE["z"] * 2 + BLOCK_SIZE["z"]
    bpy.ops.mesh.primitive_cube_add(location=(pos_x, pos_y, pos_z), rotation=(0,0,0))
    bpy.ops.rigidbody.object_add()
    obj = bpy.context.scene.objects.active
    obj.rigid_body.collision_shape='BOX'
    obj.rigid_body.mass = BLOCK_MASS
    obj.rigid_body.friction = 1
    obj.rigid_body.restitution = 0
    obj.scale = BLOCK_SIZE["x"], BLOCK_SIZE["y"], BLOCK_SIZE["z"]
    return obj

def add_color_material(obj, x, y, z):
    new_colors = {}
    for key in ["r", "g", "b"]:
        new_colors[key] = color_with_gradation(key, x, y, z)

    mat = bpy.data.materials.new('Cube')
    mat.diffuse_color = get_color(new_colors)
    obj.data.materials.append(mat)

def color_with_gradation(key, x, y, z):
    now_step = y
    max_step = BLOCK_NUMBER["y"] - 1 # 初期値が0のため
    if max_step < 1:
        return START_COLOR[key]
    color_diff = END_COLOR[key] - START_COLOR[key]
    return (START_COLOR[key] + (now_step / max_step) * color_diff)

def set_camera():
    camera_range = FIELD_SIZE["z"] * 1.8
    x_pos = camera_range * CAMERA_MARGIN
    y_pos = camera_range * CAMERA_MARGIN * -0.8
    z_pos = camera_range * CAMERA_MARGIN * 0.8
    bpy.ops.object.camera_add(
        location=(x_pos, y_pos, z_pos),
        rotation=(1.2, 0, 0.75)
    )
    obj = bpy.context.scene.objects.active
    bpy.context.scene.camera = obj
    obj.data.clip_end = CAMERA_CLIP_END

def set_lamp():
    x_pos = 0
    y_pos = 0
    z_pos = 0
    bpy.ops.object.lamp_add(
        location=(x_pos, y_pos, z_pos),
        rotation=(0.79, 0, 0),
        type = "SUN"
    )

def set_gravity():
    bpy.context.scene.gravity[2] = -9.81 * GRAVITY_MAGNIFICATION

def create_blocks():
    for x in range(0, BLOCK_NUMBER["x"]):
        for y in range(0, BLOCK_NUMBER["y"]):
            for z in range(0, BLOCK_NUMBER["z"]):
                create_cube(x, y, z)

def create_crasher():
    pos_x = BLOCK_SPACE["x"] * ((BLOCK_NUMBER["x"] - 1) / 2) * 2
    pos_y = BLOCK_SPACE["y"] * -2 - get_sphere_size() * 1.5
    pos_z = BLOCK_SPACE["z"] * BLOCK_NUMBER["z"]
    create_slope(pos_x, pos_y, pos_z)
    create_sphere(pos_x, pos_y, pos_z)

def create_slope(pos_x, pos_y, pos_z):
    bpy.ops.mesh.primitive_cube_add(location=(pos_x, pos_y, pos_z), rotation=(0.78,0,0))
    bpy.ops.rigidbody.object_add(type='PASSIVE')
    obj = bpy.context.scene.objects.active
    obj.scale = BLOCK_SIZE["x"] * BLOCK_NUMBER["x"], BLOCK_SIZE["y"], BLOCK_SIZE["z"] * BLOCK_NUMBER["z"] * 0.75
    obj.rigid_body.friction = 0.1
    obj.rigid_body.restitution = 0.9
    mat = bpy.data.materials.new('Slope')
    mat.diffuse_color = get_color(SLOPE_COLOR)
    obj.data.materials.append(mat)

def create_sphere(pos_x, pos_y, pos_z):
    pos_z = pos_z * 2.5
    bpy.ops.mesh.primitive_uv_sphere_add(location=(pos_x, pos_y, pos_z), rotation=(0,0,0))

    bpy.ops.rigidbody.object_add()
    obj = bpy.context.scene.objects.active
    obj.rigid_body.mass = SPHERE_MASS

    scale = get_sphere_size()
    obj.scale = (scale, scale, scale)
    obj.rigid_body.collision_shape='SPHERE'
    obj.rigid_body.friction = 0.1
    obj.rigid_body.restitution = 0.9
    mat = bpy.data.materials.new('Shpere')
    mat.diffuse_color = get_color(SPHERE_COLOR)
    obj.data.materials.append(mat)

def get_sphere_size():
    return BLOCK_SIZE["x"] * BLOCK_NUMBER["x"] * 0.7

def set_background_color():
    world = bpy.data.worlds["World"]
    world.horizon_color = get_color(WORLD_COLOR)

def get_color(color_data):
    return (color_data["r"] / 255, color_data["g"] / 255, color_data["b"] / 255)

def create_movie():
    bpy.ops.ptcache.bake_all()
    bpy.context.scene.render.resolution_x = MOVIE_RESOLUTION_X
    bpy.context.scene.render.resolution_y = MOVIE_RESOLUTION_Y
    bpy.context.scene.render.resolution_percentage = MOVIE_RESOLUTION_PERCENTAGE
    bpy.context.scene.render.image_settings.file_format = 'AVI_JPEG'
    bpy.data.scenes["Scene"].render.filepath = MOVIE_NAME
    bpy.context.scene.frame_start = FRAME["start"]
    bpy.context.scene.frame_end   = FRAME["end"]
    bpy.ops.render.render(animation=True)

# main
set_frame_size(FRAME["start"], FRAME["end"])
delete_all_objects()
create_floor()
create_blocks()
create_crasher()
set_camera()
set_lamp()
set_gravity()
set_background_color()
#create_movie()

