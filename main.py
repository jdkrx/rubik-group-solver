import py5  # Esta libreria la puse para que nos haga de render
from pathlib import Path
from math import pi as PI # hola necesito a pi
from py5ui import *
from scenes.inicio import ui2, load, getcheckload
from scenes.principal import ui, keyeventpress, keyeventrelease
from scenes._scenes_main import *
UIs = [ui2, ui]
fontsize = 20

resourcesstartedloading = False
def settings():
    ruta = Path(__file__).parent / "icon.png"
    py5.size(900, 600, py5.P3D)
    PJOGL = py5.JClass("processing.opengl.PJOGL")
    PJOGL.setIcon(str(ruta.resolve()))

def setup():
    py5.background(255, 206, 237)
    py5.window_resizable(True)
    py5.image_mode(py5.CENTER)
    py5.window_title("")
    

def draw():
    global resourcesstartedloading
    sceenemanager.display()
    if not resourcesstartedloading: # Cargar recursos despues de dibujar la escena
        font = py5.create_font("DejaVu Sans", fontsize) # Aca se cambia la tipografia
        py5.text_font(font) # Configuramos la letra
        #load()
        #archivos_config.start()
        resourcesstartedloading = True

def mouse_pressed():
    #if not getcheckload(): return
    for x in range(len(sceenemanager.scenes)):
        if sceenemanager.getScene() == x: UIs[x].checkClicked() # evaluar clicks de la ui
def mouse_released():
    #if not getcheckload(): return
    for x in range(len(sceenemanager.scenes)):
        if sceenemanager.getScene() == x: UIs[x].checkReleased() # evaluar clicks de la ui
def key_pressed():
    if sceenemanager.getScene() == PRINCIPAL:
        keyeventpress()
def key_released():
    if sceenemanager.getScene() == PRINCIPAL:
        keyeventrelease()
    
py5.run_sketch()



