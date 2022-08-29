from turtle import window_height, window_width
import pyglet
from pyglet import shapes
import json
import random
import draw_pod


def load_json(file_name):
    f = open(file_name, "r")
    data = json.load(f)
    f.close()
    return data


#CONSTANTS + COLORS
window_height = 600
window_width = 800
divide_const = 20
checkpoint_size = 600//divide_const

pod_colors = [tuple(random.randrange(0, 256, 16)
                    for _ in range(3)) for _ in range(5)]
colors = {
    "map_bg": (255, 255, 200),
    "check": (113, 213, 93),
    "pod_body": pod_colors,
    "pod_radius": (30, 140, 255),
    "pod_shield": (254, 27, 7),
    "check_numb": (0, 0, 0, 255)
}
font = {
    "check_size": 30
}

# LOAD JSON
file_name = "game_data/2022-08-06_12:04:38.json"
data = load_json(file_name)

# BATCH + RENDER GROUPS
batch = pyglet.graphics.Batch()
background = pyglet.graphics.OrderedGroup(0)
checkpoint_group = pyglet.graphics.OrderedGroup(1)
number_group = pyglet.graphics.OrderedGroup(2)
pods_group = pyglet.graphics.OrderedGroup(3)

# MAP
map_x, map_y = data["map"]["size"]
x = map_x//divide_const
y = map_y//divide_const
# map_background = shapes.BorderedRectangle(
#     0, 0, x, y, color=colors["map_bg"], batch=batch, group=background)

# CHECKPOINTS
checkpoints, check_numb = [], []
for i, check in enumerate(data["map"]["checkpoints"]):
    checkpoints.append(shapes.Circle(check["x"]//divide_const,
                                     check["y"]//divide_const,
                                     checkpoint_size,
                                     color=colors["check"],
                                     batch=batch, group=checkpoint_group))
    check_numb.append(pyglet.text.Label(str((i+1)),
                                        x=check["x"]//divide_const,
                                        y=check["y"]//divide_const,
                                        color=colors["check_numb"],
                                        font_size=font["check_size"], anchor_x="center", anchor_y="center",
                                        batch=batch, group=number_group))
check_numb[-1].text = "0"

# PODS
pod = draw_pod.Pod(4000, 4000, 3.1415/4, id=0,
                   radius=400, divide_const=divide_const,
                   colors=colors, batch=batch, group=pods_group)

#TODO: trajectory

# PARAMETERS
# x = 0-800, y = 450-600

# POD 1 
# THURST    v: ______
# TARGET    x: _____ y: _____
# POSITION: x: _____ y: _____ fi: ___ 
# VELOCITY: x: _____ y: _____
# ACCELER:  ?

label = pyglet.text.Label('POD 0',
                          font_size=20,
                          x=0, y=600-30,
                          anchor_x='left', anchor_y='baseline', batch=batch, group=number_group)

label = pyglet.text.Label('THURST    v: SHIELD',
                          font_size=15,
                          x=0, y=600-30-30,
                          anchor_x='left', anchor_y='baseline', batch=batch, group=number_group)
label = pyglet.text.Label('TARGET    x: 16000 y: _9000',
                          font_size=15,
                          x=0, y=600-30-30-30,
                          anchor_x='left', anchor_y='baseline', batch=batch, group=number_group)
label = pyglet.text.Label('POSITION: x: 16000 y: _9000 fi: 360',
                          font_size=15,
                          x=0, y=600-30-30-30-30,
                          anchor_x='left', anchor_y='baseline', batch=batch, group=number_group)
label = pyglet.text.Label('VELOCITY: x: 16000 y: _9000',
                          font_size=15,
                          x=0, y=600-30-30-30-30-30,
                          anchor_x='left', anchor_y='baseline', batch=batch, group=number_group)

cara = pyglet.shapes.Line(0,600-30-30-30-30-30-10,800,600-30-30-30-30-30-10,width=2,batch=batch,group=number_group)

# WINDOW
window = pyglet.window.Window(window_width, window_height)


@window.event
def on_draw():
    window.clear()
    batch.draw()


if __name__ == "__main__":
    pyglet.app.run()
