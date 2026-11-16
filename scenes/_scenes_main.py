from scenes.inicio import inicio, ui2, botonirprincipal
from scenes.principal import principal, ui, barrasuperior, botonvolverinicio, settheta0
from py5ui import SceneManager

sceenemanager = SceneManager()
INICIO = sceenemanager.addScene(inicio)
PRINCIPAL = sceenemanager.addScene(principal)

def cambiaventanaclick():
    settheta0()
    if sceenemanager.getScene() == INICIO: sceenemanager.sceneGoTo(PRINCIPAL)
    elif sceenemanager.getScene() == PRINCIPAL: sceenemanager.sceneGoTo(INICIO)

# la funcion de cambiar ventana la debemos añadir despues pues en el archivo de la escena
# aun no estan creadas las otras escenas y no se puede definir la funcion cambiarventanaclick
ui2.elements[botonirprincipal].setclick(cambiaventanaclick)  
ui.elements[barrasuperior].barElements[botonvolverinicio].setclick(cambiaventanaclick)
