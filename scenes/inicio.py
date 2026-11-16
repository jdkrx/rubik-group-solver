import py5
from time import perf_counter as getTime
from .cubos.cubo3x3 import cola
from py5ui import *
from .styles import * 

ui2 = UIManager() # Creamos una interfaz para la ventana inicio
text = UIText(width / 2, height / 2 - 100, "CUBO DE RUBIK", 42, py5.color(0), "CENTER")
textid = ui2.addElement(text)
botonirprincipal = ui2.addElement(UIButton(width / 2 - 110, height / 2 + 10, 220, 60, "COMENZAR", 24, funcionvacia, funcionvacia, config_boton_inicio))
isReady = True
hasloaded = False
frames = []
counter = 0

checkload = ["testing"]

def inicio():
    global frames, counter, isReady, hasloaded, checkload
    counter = 7*getTime()

    ui2.elements[textid].x = py5.width/2
    ui2.elements[textid].y = py5.height/2 - 100
    ui2.elements[botonirprincipal].x = py5.width/2 - 110
    ui2.elements[botonirprincipal].y = py5.height/2 + 10
    py5.background(255, 206, 237)
    if len(checkload) == 0:
        if not hasloaded:
            isReady = True
            for x in frames:
                if not x.is_ready or len(frames) < 10: isReady = False

        if isReady and len(frames) == 10:
            hasloaded = True
            py5.image(frames[int(counter)%10].result, py5.width/2, py5.height/2)
    #else: ui2.drawElements()
    # if not cola.empty():
    #     checkload.append("listo")
    ui2.drawElements()

def load():
    global frames
    for x in range(10):
        frames.append(py5.request_image(f'carga/carga-{x}.png'))

def getcheckload():
    global checkload
    if len(checkload) == 0: return False
    else: return True