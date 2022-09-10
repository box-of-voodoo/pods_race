import pyglet
from pyglet.event import EVENT_HANDLED, EVENT_UNHANDLED


class Button(pyglet.event.EventDispatcher):
    def __init__(self, x, y, size, color,
                 window: pyglet.event.EventDispatcher,
                 batch: pyglet.graphics.Batch,
                 group: pyglet.graphics.OrderedGroup):
        window.push_handlers(self)
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.square = pyglet.shapes.Rectangle(
            x, y, size, size, color=self.color["bg"], batch=batch, group=group)
        self.square.opacity = 128
        self._pressed = False
        self.add_fg_shapes(batch, group)

    def add_fg_shapes(self, batch, group):
        self.fg_shapes = []

    def pressed(self):
        self._pressed = True
        self.square.color = self.color["bg_pressed"]
        for el in self.fg_shapes:
            el.color = self.color["fg_pressed"]

    def released(self):
        self._pressed = False
        self.square.color = self.color["bg"]
        for el in self.fg_shapes:
            el.color = self.color["fg"]

    def on_mouse_press(self, x, y, button, modifiers):
        if (pyglet.window.mouse.LEFT == button
                and (self.x <= x <= self.x+self.size)
                and (self.y <= y <= self.y + self.size)
            ):
            self.pressed()
            return EVENT_HANDLED
        return EVENT_UNHANDLED

    def on_mouse_release(self, x, y, button, modifiers):
        if self._pressed:
            self.released()
            if (pyglet.window.mouse.LEFT == button
                        and (self.x <= x <= self.x+self.size)
                        and (self.y <= y <= self.y + self.size)
                    ):
                self.dispatch_event('on_push')
                return EVENT_HANDLED
        return EVENT_UNHANDLED


Button.register_event_type('on_push')
