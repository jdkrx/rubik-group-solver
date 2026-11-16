from py5ui import SceneManager
import threading
import queue
import time
from .cubos.cubo3x3 import configurararchivos, cola
from scenes.inicio import inicio, ui2, botonirprincipal
from scenes.principal import principal, ui, barrasuperior, botonvolverinicio, settheta0

dict_reps1 = []
dict_reps2 = []
dict_reps3 = []
dict_reps4 = []
hasloaded = False
archivos_config = threading.Thread(target=configurararchivos, args=(cola,))

sceenemanager = SceneManager()
INICIO = sceenemanager.addScene(inicio)
PRINCIPAL = sceenemanager.addScene(principal)

def cambiaventanaclick():
    global dict_reps1, dict_reps2, dict_reps3, dict_reps4, hasloaded, checkload
    settheta0()
    if sceenemanager.getScene() == INICIO: sceenemanager.sceneGoTo(PRINCIPAL)
    elif sceenemanager.getScene() == PRINCIPAL: sceenemanager.sceneGoTo(INICIO)

# la funcion de cambiar ventana la debemos añadir despues pues en el archivo de la escena
# aun no estan creadas las otras escenas y no se puede definir la funcion cambiarventanaclick
ui2.elements[botonirprincipal].setclick(cambiaventanaclick)  
ui.elements[barrasuperior].barElements[botonvolverinicio].setclick(cambiaventanaclick)