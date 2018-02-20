# -*- coding: utf-8 -*-

import bpy
from numpy.random import *

# config
FIELD_X = 10
FIELD_Y = 10
START_FRAME = 0
CUBE_NUMBER = 100
CUBE_PER_FRAME = 2
END_FRAME = CUBE_NUMBER * CUBE_PER_FRAME + 30
CUBE_DEFAULT_Z = 20

# 全削除
for item in bpy.context.scene.objects:
    bpy.context.scene.objects.unlink(item)

# ブロック追加
def create_cube(i):
    pos_x = rand() * FIELD_X - FIELD_X / 2 + 0.5
    pos_y = rand() * FIELD_Y - FIELD_Y / 2 + 0.5
    pos_z = CUBE_DEFAULT_Z + i * 2
    bpy.ops.mesh.primitive_cube_add(location=(pos_x, pos_y, pos_z), rotation=(0,0,0))
    bpy.ops.rigidbody.object_add()
    obj = bpy.context.scene.objects.active
    obj.rigid_body.angular_damping = 0
    obj.rigid_body.mass = 0.05
    obj.rigid_body.restitution = 0.5
    obj.scale = (0.5, 0.5, 0.5)

    # color
    mat = bpy.data.materials.new('Cube')
    mat.diffuse_color = (rand(), rand(), rand())
    obj.data.materials.append(mat)

# camera
bpy.ops.object.camera_add(
    location=(19, -18, 20),
    rotation=(1, 0, 0.8)
)
obj = bpy.context.scene.objects.active
bpy.context.scene.camera = obj

# 照明
bpy.ops.object.lamp_add(
    location=(5, -60, 0),
    rotation=(0, 0, 0),
    type = "SUN"
)

# 平面作成
bpy.ops.mesh.primitive_plane_add(location=(0, 0, 0))
bpy.ops.rigidbody.object_add(type='PASSIVE')
obj = bpy.context.scene.objects.active
obj.scale = (FIELD_X / 2, FIELD_Y /2 , 1)
mat = bpy.data.materials.new('Plane')
mat.diffuse_color = (rand(), rand(), rand())
obj.data.materials.append(mat)

# frame
bpy.context.scene.frame_start = START_FRAME
bpy.context.scene.frame_end = END_FRAME

# main
for i in range(0, CUBE_NUMBER):
    create_cube(i)

