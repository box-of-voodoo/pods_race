import pyglet
import math as m


def add_angle(a, b):
    return (a+b) % (m.pi*2)


class Pod:
    def __init__(self, x, y, angle, id, colors, radius=400, divide_const=20, batch=None, group=None):
        self.id = id
        self.divide_const = divide_const
        self.radius = radius
        color_id = id % len(colors["pod_body"])
        keys = ["pod_radius", "pod_shield"]
        self.colors = {x: colors[x] for x in keys}

        self.x = x
        self.y = y
        self.a = angle
        body_p = self.calc_body()
        self.triangle = pyglet.shapes.Triangle(body_p[0][0]//self.divide_const, body_p[0][1]//self.divide_const,
                                               body_p[1][0]//self.divide_const, body_p[1][1]//self.divide_const,
                                               body_p[2][0]//self.divide_const, body_p[2][1]//self.divide_const,
                                               color=colors["pod_body"][color_id], batch=batch, group=group)
        self.circle = pyglet.shapes.Arc(
            self.x//self.divide_const,
            self.y//self.divide_const,
            self.radius//self.divide_const,
            color=colors["pod_radius"], batch=batch, group=group)

    def calc_body(self):
        point1 = (self.x+self.radius*m.cos(self.a),
                  self.y+self.radius*m.sin(self.a))
        point2 = (self.x+self.radius*m.cos(add_angle(self.a, m.pi*3/4)),
                  self.y+self.radius*m.sin(add_angle(self.a, m.pi*3/4)))
        point3 = (self.x+self.radius*m.cos(add_angle(self.a, m.pi*5/4)),
                  self.y+self.radius*m.sin(add_angle(self.a, m.pi*5/4)))
        return [point1, point2, point3]

    def update(self, x, y, angle, shield=False):
        self.x = x
        self.y = y
        self.a = angle
        self.triangle.position = tuple(j//self.divide_const for i in self.calc_body() for j in i)
        self.circle.position = (x//self.divide_const, y//self.divide_const)
        if shield:
            self.circle.color = self.colors["pod_shield"]
        else:
            self.circle.color = self.colors["pod_radius"]
