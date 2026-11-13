import py5
from .uiElement import UIElement
class UIText(UIElement):
    def __init__(self, x, y, text, textsize, color, mode):
        super().__init__(x, y, 10005)
        self.text = text
        self.textsize = textsize
        self.textcolor = color
        self.clickable = False
        self.mode = mode
        pass
    def display(self):
        py5.fill(self.textcolor)
        py5.text_size(self.textsize)
        if (self.mode == "CENTER"):
            py5.text_align(py5.CENTER, py5.CENTER)
        else: py5.text_align(py5.LEFT, py5.BASELINE)

        py5.text(self.text, self.x, self.y)