import pyglet
import math as m



class Stats:
    def __init__(self, x, y, width, height, batch, group):
        self.pods = {}
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.batch = batch
        self.group = group
        self.text_height = (height//16)*3
        self.font_size = self.text_height//2
        self.init_labels()

    def init_labels(self):
        pyglet.text.Label('Thurst',
                          font_size=self.font_size,
                          x=self.x+self.width//100, y=self.y-self.text_height*2,
                          anchor_x='left', anchor_y='baseline', batch=self.batch, group=self.group)
        pyglet.text.Label('Target',
                          font_size=self.font_size,
                          x=self.x+self.width//100, y=self.y-self.text_height*3,
                          anchor_x='left', anchor_y='baseline', batch=self.batch, group=self.group)
        pyglet.text.Label('Position',
                          font_size=self.font_size,
                          x=self.x+self.width//100, y=self.y-self.text_height*4,
                          anchor_x='left', anchor_y='baseline', batch=self.batch, group=self.group)
        pyglet.text.Label('Velocity',
                          font_size=self.font_size,
                          x=self.x+self.width//100, y=self.y-self.text_height*5,
                          anchor_x='left', anchor_y='baseline', batch=self.batch, group=self.group)

        self.cara = pyglet.shapes.Line(self.x, self.y-self.height, self.x+self.width, self.y-self.height,
                           width=2, batch=self.batch, group=self.group)

    def add_pod(self, pod_id):
        self.pods[pod_id] = PodStats(pod_id,
                                     self.width//8 +
                                     len(self.pods)*self.width//3.5,
                                     self.y,
                                     self.width,
                                     self.font_size,
                                     self.text_height,
                                     self.batch, self.group)

    def update(self, data):
        for pod_data in data:
            if pod_data["id"] in self.pods:
                self.pods[pod_data["id"]].update(pod_data)


class PodStats:
    def __init__(self, pod_id, x, y, full_width, font_size, text_height, batch, group):
        self.id = pod_id
        pyglet.text.Label('POD '+str(self.id),
                          font_size=font_size*(4/3),
                          x=x, y=y-text_height,
                          anchor_x='left', anchor_y='baseline', batch=batch, group=group)
        self.thurst = ThurstStat(x, y-2*text_height,
                                 full_width, font_size, batch, group)
        self.target = XYStat(x, y-3*text_height,
                             full_width, font_size, batch, group)
        self.position = XYfiStat(x, y-4*text_height,
                                 full_width, font_size, batch, group)
        self.velocity = XYStat(x, y-5*text_height,
                               full_width, font_size, batch, group)

    def update(self, data):
        self.thurst.update(data["thurst"])
        self.target.update(round(data["target_x"]), round(data["target_y"]))
        self.position.update(round(data["x"]), round(data["y"]), round(m.degrees(data["angle"])))
        self.velocity.update(data["speed_x"], data["speed_y"])


class ThurstStat:
    def __init__(self, x, y, full_width, font_size, batch, group):  # y=y-2*text_height
        pyglet.text.Label('v:',
                          font_size=font_size,
                          x=x, y=y,
                          anchor_x='left', anchor_y='baseline', batch=batch, group=group)

        self.value = pyglet.text.Label('SHIELD',
                                       font_size=font_size,
                                       x=x + full_width//8.88, y=y,
                                       anchor_x='right', anchor_y='baseline', batch=batch, group=group)

    def update(self, val):
        self.value.text = str(val)


class XYStat:
    def __init__(self, x, y, full_width,  font_size, batch, group):

        pyglet.text.Label('x:',
                          font_size=font_size,
                          x=x, y=y,
                          anchor_x='left', anchor_y='baseline', batch=batch, group=group)

        self.x = pyglet.text.Label('16000',
                                   font_size=font_size,
                                   x=x+full_width//10-full_width//200, y=y,
                                   anchor_x='right', anchor_y='baseline', batch=batch, group=group)

        pyglet.text.Label('y:',
                          font_size=font_size,
                          x=x+full_width//10, y=y,
                          anchor_x='left', anchor_y='baseline', batch=batch, group=group)

        self.y = pyglet.text.Label('9000',
                                   font_size=font_size,
                                   x=x+2*full_width//10-full_width//200, y=y,
                                   anchor_x='right', anchor_y='baseline', batch=batch, group=group)

    def update(self, val_x, val_y):
        self.x.text = str(val_x)
        self.y.text = str(val_y)


class XYfiStat(XYStat):
    def __init__(self, x, y, full_width,  font_size, batch, group):
        super().__init__(x, y, full_width, font_size, batch, group)
        pyglet.text.Label('fi:',
                          font_size=font_size,
                          x=x+2*full_width//10, y=y,
                          anchor_x='left', anchor_y='baseline', batch=batch, group=group)
        self.fi = pyglet.text.Label('360',
                                    font_size=font_size,
                                    x=x+2*full_width//10+full_width//13.33-full_width//200, y=y,
                                    anchor_x='right', anchor_y='baseline', batch=batch, group=group)

    def update(self, val_x, val_y, val_fi):
        super().update(val_x, val_y)
        self.fi.text = str(val_fi)
