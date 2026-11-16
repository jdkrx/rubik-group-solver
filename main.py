import py5  # Esta libreria la puse para que nos haga de render
from math import pi as PI # hola necesito a pi
from py5ui import *
from scenes.inicio import ui2
from scenes.principal import ui, keyeventpress, keyeventrelease
from scenes._scenes_main import *
UIs = [ui2, ui]
fontsize = 20

def setup():
    py5.size(800, 600, py5.P3D)
    font = py5.create_font("DejaVu Sans", fontsize) # Aca se cambia la tipografia
    py5.text_font(font) # Configuramos la letra
    py5.window_resizable(True)
def draw():
    sceenemanager.display()
def mouse_pressed():
    for x in range(len(sceenemanager.scenes)):
        if sceenemanager.getScene() == x: UIs[x].checkClicked() # evaluar clicks de la ui
def mouse_released():
    for x in range(len(sceenemanager.scenes)):
        if sceenemanager.getScene() == x: UIs[x].checkReleased() # evaluar clicks de la ui
def key_pressed():
    pressed_key = py5.key
    if sceenemanager.getScene() == PRINCIPAL:
        keyeventpress(pressed_key)
def key_released():
    released_key = py5.key
    if sceenemanager.getScene() == PRINCIPAL:
        keyeventrelease(released_key)
    
py5.run_sketch()



