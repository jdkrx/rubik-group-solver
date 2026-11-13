import py5  # Esta libreria la puse para que nos haga de render
from math import pi as PI # hola necesito a pi
from py5ui import *
from scenes.inicio import ui2
from scenes.principal import ui
from scenes._scenes_main import sceenemanager

fontsize = 20

def setup():
    py5.size(800, 600, py5.P3D)
    font = py5.create_font("DejaVu Sans", fontsize) # Aca se cambia la tipografia
    py5.text_font(font) # Configuramos la letra
def draw():
    sceenemanager.display()
def mouse_pressed():
    if sceenemanager.getScene() == 1: ui.checkClicked() # evaluar clicks de la ui
    elif sceenemanager.getScene() == 0: ui2.checkClicked()
def mouse_released():
    if sceenemanager.getScene() == 1: ui.checkReleased() # evaluar clicks de la ui
    elif sceenemanager.getScene() == 0: ui2.checkReleased()


py5.run_sketch()



