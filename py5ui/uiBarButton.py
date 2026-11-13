import py5
from .uiElement import UIElement

class UIBarButton(UIElement):
    def __init__(self, width, text, fontsize, click, press, config):
        super().__init__(0, 0, 10004)
        self.font = fontsize
        self.width = width
        self.text = text
        self.clickEvent = click
        self.pressEvent = press
        self.active = False
        self.encima = False
        self.height = 0
        self.color_relleno_1 = config[0]
        self.color_relleno_2 = config[1]
        self.color_relleno_3 = config[2]
        self.color_texto = config[3]
        self.color_trazo = config[4]
        self.grosor_trazo = config[5]
        self.radio = config[6]
        pass
    def display(self):
        if self.active:
            py5.fill(self.color_relleno_2)
        elif self.encima:
            py5.fill(self.color_relleno_3)
        else:
            py5.fill(self.color_relleno_1)
        py5.stroke(self.color_trazo)
        py5.stroke_weight(self.grosor_trazo)
        py5.translate(self.x, self.y)
        py5.rect(0, 0, self.width, self.height, self.radio)
        py5.fill(self.color_texto)
        py5.text_size(self.font)
        py5.text_align(py5.LEFT, py5.BASELINE)
        py5.text(self.text, self.width/2-py5.text_width(self.text)/2, self.height/2 + self.font/2-2)
        py5.translate(-self.x, -self.y)
        if py5.is_mouse_pressed and py5.mouse_button == py5.LEFT and self.active and self.x < py5.mouse_x < self.x + self.width and self.y < py5.mouse_y < self.y + self.height:
            self.pressEvent()
        else:
            self.active = False
        if self.x < py5.mouse_x < self.x + self.width and self.y < py5.mouse_y < self.y + self.height:
            self.encima = True
        else: self.encima = False
    def onClick(self):
        if (self.x < py5.mouse_x < self.x + self.width and self.y < py5.mouse_y < self.y + self.height):
            self.clickEvent()
            self.active = True
        pass
    def onReleased(self):
        self.active = False
        pass