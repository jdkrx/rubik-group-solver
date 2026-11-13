import py5
from .uiElement import UIElement

# Colores topbar


class UITopBar(UIElement):
    def __init__(self, height, config):
        super().__init__(0, 0, 10002)
        self.barElements = []
        self.height = height
        self.color_relleno = config[0]
        self.color_trazo = config[1]
        self.grosor_trazo = config[2]
        pass
    def display(self):
        # Display propio
        py5.fill(self.color_relleno)
        py5.stroke(self.color_trazo)
        py5.stroke_weight(self.grosor_trazo)
        py5.rect(0, 0, py5.width, self.height)

        # display de los hijos
        xcounter = 0
        for x in self.barElements:
            x.display()
            xcounter += x.width
    def addBarElement(self, newelement):
        newelement.height = self.height
        self.barElements.append(newelement)
        xcounter = 0
        for x in self.barElements:
            x.x = xcounter
            xcounter += x.width
    def onClick(self):
        for x in self.barElements:
            x.onClick()
    def onReleased(self):
        for x in self.barElements:
            x.onReleased()
        pass