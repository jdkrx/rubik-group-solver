import py5
from .uiElement import UIElement


class UIBarMenu(UIElement):
    def __init__(self, width, height, text, fontsize, config):
        super().__init__(0, 0, 10003)
        self.font = fontsize
        self.width = width
        self.text = text
        self.active = False
        self.clicked = False
        self.height = height
        self.encima = False
        self.elements = []
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
        py5.rect(self.x, self.y, self.width, self.height, self.radio)
        py5.text_size(self.font)
        py5.fill(self.color_texto)
        py5.text_align(py5.LEFT, py5.BASELINE)
        py5.text(self.text, self.x + self.width/2-py5.text_width(self.text)/2, self.height/2 + self.font/2 - 2)
        
        if py5.is_mouse_pressed and py5.mouse_button == py5.LEFT and self.active and self.x < py5.mouse_x < self.x + self.width and self.y < py5.mouse_y < self.y + self.height:
            pass 
        else:
            self.active = False
        if self.x < py5.mouse_x < self.x + self.width and self.y < py5.mouse_y < self.y + self.height:
            self.encima = True
        else: self.encima = False

        if self.clicked:
            maxx = self.width
            maxy = 0
            for x in self.elements:
                if maxx < x.width:
                    maxx = x.width
                maxy += x.height
            #py5.rect(0, self.height, maxx, maxy)
            for x in self.elements:
                x.width = maxx
                x.display()
            


    def onClick(self):
        ycounter = self.height
        for x in self.elements:
            x.y = ycounter
            ycounter += x.height
            x.height = self.height
            x.x = self.x
        maxx = 0
        maxy = 0
        for x in self.elements:
            if maxx < x.width:
                maxx = x.width
            maxy += x.height
        if (self.x < py5.mouse_x < self.x + self.width and self.y < py5.mouse_y < self.y + self.height):
            self.clicked = not self.clicked
            self.active = True
        elif (self.clicked and self.x < py5.mouse_x < self.x + maxx and self.y + self.height < py5.mouse_y < self.y + self.height + maxy):   
            for x in self.elements:
                x.onClick()
        else:
            self.clicked = False
        pass
    def onReleased(self):
        self.active = False
        pass
    def addElement(self, newelement):
        self.elements.append(newelement)
        ycounter = self.height
        for x in self.elements:
            x.y = ycounter
            ycounter += x.height
            x.height = self.height
            x.x = self.x