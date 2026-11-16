import py5
from .uiElement import UIElement
class UITextBox(UIElement):
    def __init__(self, x, y, width, height, text, textsize, color, mode):
        super().__init__(x, y, 10005)
        self.text = text
        self.textsize = textsize
        self.textcolor = color
        self.clickable = False
        self.mode = mode
        self.width = width
        self.height = height
    def display(self):
        py5.fill(self.textcolor)
        py5.text_size(self.textsize)
        if (self.mode == "CENTER"):
            py5.text_align(py5.CENTER, py5.CENTER)
            py5.text(self.text, self.x, self.y, self.width, self.height)
        else:
            py5.text_align(py5.LEFT, py5.BASELINE)
            py5.text(self.text, self.x, self.y, self.width, self.height)