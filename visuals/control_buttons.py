import pyglet
from button import Button


class PauseButton(Button):
    def add_fg_shapes(self, batch, group):
        super().add_fg_shapes(batch, group)
        self.fg_shapes.append(pyglet.shapes.Rectangle(self.x+self.size//5, self.y+self.size//8,
                                                      self.size//5, self.size-self.size//4,
                                                      color=self.color["fg"],
                                                      batch=batch, group=group))
        self.fg_shapes.append(pyglet.shapes.Rectangle(self.x+self.size-2*self.size//5, self.y+self.size//8,
                                                      self.size//5, self.size-self.size//4,
                                                      color=self.color["fg"],
                                                      batch=batch, group=group))
