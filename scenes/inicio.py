import py5
from py5ui import *
from .styles import * 

ui2 = UIManager() # Creamos una interfaz para la ventana inicio
ui2.addElement(UIText(width / 2, height / 2 - 100, "CUBO DE RUBIK", 42, py5.color(0), "CENTER"))
botonirprincipal = ui2.addElement(UIButton(width / 2 - 110, height / 2 + 10, 220, 60, "COMENZAR", 24, funcionvacia, funcionvacia, config_boton_inicio))

def inicio():
    py5.background(255, 206, 237)
    ui2.drawElements()