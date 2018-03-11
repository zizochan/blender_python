# -*- coding: utf-8 -*-

# import
import bpy
from numpy.random import *
import random
import math

# config

## MAP
def create_map(map_data):
    map_lines = reversed(map_data.splitlines()) # 文字が反転しないようにreversedする
    map = []
    for x_str in map_lines:
        map.append(list(x_str))
    return map

map_data = """
0000000000000000000000000000000000
0111000110010001000100011100111010
0100101001011001001010010010100010
0100101001010101010001011100111010
0100101001010011011111010010100000
0111000110010001010001011100111010
0000000000000000000000000000000000
""".strip()
MAP = create_map(map_data)

## FIELD SIZE
FIELD_X = len(MAP[0]) # 全て同じ長さの前提
FIELD_Z = len(MAP)
FIELD_Y_SIZE = 300

## CUBE
CUBE_SIZE = 1
CUBE_MOVE_FRAME = 25
CUBE_MOVE_INTERVAL = 1
CUBE_COUNT = FIELD_X * FIELD_Z

## CAMERA
CAMERA_Y_DEPTH = 40

## lamp
LAMP_Y_DEPTH = 100

## COLOR
COLORS = [
    {"r": 0, "g": 0.5, "b": 0.3},
    {"r": 1, "g": 0, "b": 0}
]
COLOR_MARGIN = 5

## FRAME
REVERBERATION_FRAME = 30
START_FRAME = 0
END_FRAME = CUBE_COUNT * CUBE_MOVE_INTERVAL + CUBE_MOVE_FRAME + REVERBERATION_FRAME



def set_frame_size():
    bpy.context.scene.frame_start = START_FRAME
    bpy.context.scene.frame_end = END_FRAME

def delete_all_objects():
    for item in bpy.context.scene.objects:
        bpy.context.scene.objects.unlink(item)

def create_cubes():
    positions = decice_move_orders()
    i = 0
    for position in positions:
        x, z, color_number = position
        create_cube(x, z, color_number, i)
        i += 1

def decice_move_orders():
    positions = []
    for x in range(0, FIELD_X):
        for z in range(0, FIELD_Z):
            color_number = int(MAP[z][x])
            positions.append([x, z, color_number])
    random.shuffle(positions)
    return positions

def create_cube(x, z, color, i):
    cube = create_primitive_cube(x, z)
    add_color_material(cube, color, x, z)
    set_cube_frame(cube, i)

def create_primitive_cube(x, z):
    pos_x = x * CUBE_SIZE
    pos_y = FIELD_Y_SIZE
    pos_z = z * CUBE_SIZE
    bpy.ops.mesh.primitive_cube_add(location=(pos_x, pos_y, pos_z), rotation=(0,0,0))
    obj = bpy.context.scene.objects.active
    obj.scale = (0.5, 0.5, 0.5)
    return obj

def add_color_material(obj, color_number, x, z):
    base_colors = COLORS[color_number]
    new_colors = {}

    for key in ["r", "g", "b"]:
        if color_number == 0:
            new_colors[key] = color_with_gradation(base_colors[key], x, z)
        else:
            new_colors[key] = base_colors[key]

    mat = bpy.data.materials.new('Cube')
    mat.diffuse_color = (new_colors["r"], new_colors["g"], new_colors["b"])
    obj.data.materials.append(mat)

def color_with_gradation(color, x, z):
    step = x + z + COLOR_MARGIN # 初期値が0にならないように+marginしておく
    max_step = FIELD_X + FIELD_Z + COLOR_MARGIN
    return color * (step / max_step)

def set_cube_frame(obj, i):
    # default key frame
    bpy.context.scene.frame_set(0)
    obj.hide = 1
    obj.keyframe_insert( data_path='hide' )

    # move start key frame
    start_frame = START_FRAME + i * CUBE_MOVE_INTERVAL
    bpy.context.scene.frame_set(start_frame)
    obj.keyframe_insert( data_path='location' )
    obj.hide = 0
    obj.keyframe_insert( data_path='hide' )

    # move stop key frame
    bpy.context.scene.frame_set(start_frame + CUBE_MOVE_FRAME)
    obj.location = ( obj.location.x, 0, obj.location.z )
    obj.keyframe_insert( data_path='location' )

def set_camera():
    x_pos = FIELD_X * CUBE_SIZE / 2
    y_pos = CAMERA_Y_DEPTH * -1
    z_pos = FIELD_Z * CUBE_SIZE / 2
    bpy.ops.object.camera_add(
        location=(x_pos, y_pos, z_pos),
        rotation=(1.57, 0, 0)
    )
    obj = bpy.context.scene.objects.active
    bpy.context.scene.camera = obj

def set_lamp():
    x_pos = FIELD_X * CUBE_SIZE / 2
    y_pos = LAMP_Y_DEPTH * -1
    z_pos = FIELD_Z * CUBE_SIZE / 2
    bpy.ops.object.lamp_add(
        location=(x_pos, y_pos, z_pos),
        rotation=(0.79, 0, 0),
        type = "SUN"
    )

# main
set_frame_size()
delete_all_objects()
create_cubes()
set_camera()
set_lamp()
