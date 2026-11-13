import py5
class UIManager:
    def __init__(self):
        self.elements = []
        pass
    def drawElements(self):
        py5.hint(py5.DISABLE_DEPTH_TEST)
        py5.push_matrix()      # <--- 1. Guarda la matriz del cubo
        py5.reset_matrix()     # <--- 2. Vuelve al origen (0,0) en 2D
        py5.camera()           
        py5.no_lights() 
        py5.text_size(20)
        for x in self.elements:
            x.display()

        py5.pop_matrix()       # <--- 3. Restaura la matriz para el próximo frame
        py5.hint(py5.ENABLE_DEPTH_TEST)

    def addElement(self, newelement):
        self.elements.append(newelement)
    def checkClicked(self):
        for x in self.elements:
            if(x.clickable):
                x.onClick()
    def checkReleased(self):
        for x in self.elements:
            if(x.clickable):
                x.onReleased()