import py5
import py5ui
import time
from .styles import *
from math import pi as PI
from .cubos.cubo2x2 import cube
from .cubos.cubo3x3 import *
import random 

modolibre = False
CODIGOESPACIO = 32
isCTRLPressed = False
autoMode = False
startTurningTrigger = False
stopTurningTrigger = False
ROTATING = True
KEYPRESSED = False
inicio = 0
final = 0
theta = 0
phi = 0
theta0 = 0
scrambletext = ""
c333 = ID_CUBO.copy()
separation = 1
canmove = False
teclas_activas = set()
inicioSolving = 0
cubo_is_solving = False
startedSolving = False

dict_reps1 = []
dict_reps2 = []
dict_reps3 = []
dict_reps4 = []

# FUNCIONES DE PRUEBA PARA LOS BOTONES, TODOS HACEN LO MISMO
def onclick():
    print("helloworld")
def onpress():
    print(f"mouse x: {py5.mouse_x}")
def generar_scramble_3x3(min_giros=20, max_giros=25):
    global startedSolving, ROTATING, cubo_is_solving
    ejes = [
        ['R', 'L'],
        ['U', 'D'],
        ['F', 'B']
    ]
    modificadores = ['', "'", '2']
    
    # Elegir un largo aleatorio entre 20 y 25
    longitud = random.randint(min_giros, max_giros)
    
    scramble = []
    ultimo_eje = -1
    ultima_cara = ''
    
    while len(scramble) < longitud:
        eje_actual = random.randint(0, 2)
        cara_actual = random.choice(ejes[eje_actual])
        
        # Regla 1: No repetir la misma cara seguida (ej. R R')
        if cara_actual == ultima_cara:
            continue
            
        # Regla 2: Evitar secuencias redundantes en el mismo eje (ej. R L R)
        if len(scramble) >= 2 and eje_actual == ultimo_eje:
            # Extraemos solo la letra del penúltimo movimiento (ignorando ' o 2)
            penultima_cara = scramble[-2][0]
            if penultima_cara in ejes[eje_actual]:
                continue
                
        mod = random.choice(modificadores)
        scramble.append(cara_actual + mod)
        ultimo_eje = eje_actual
        ultima_cara = cara_actual
    mezcla = " ".join(scramble)
    print (" ".join(scramble))
    global c333, scrambletext
    scrambletext = ""
    scrambletext += mezcla
    ui.elements[ui_texto_mezcla].text = "Mezcla: "
    ui.elements[ui_texto_mezcla].text += scrambletext
    c333 = ID_CUBO.copy()
    partes = mezcla.split(" ")
    if not mezcla == "":
        for i in partes:
            c333 = c333*genname(i)
    startedSolving = False
    ROTATING = True
    cubo_is_solving = False


# region --- INTERFAZ
ui = UIManager() # Creamos una interfaz para la ventana cubo

ui_texto_mezcla = ui.addElement(UIText(10, 60, f"Mezcla: {scrambletext}", 20, py5.color(0), ""))
sceenemanager = SceneManager()

topbar = UITopBar(45, config_barra) # Hacemo un elemento de barra superior

barmenu0 = UIBarMenu(115, 45, "Mezcla", fontsize, config_barmenu1) # creamos un menu
barmenu0.addElement(UIBarButton(120, "Nueva Mezcla", fontsize, generar_scramble_3x3, funcionvacia, config_barmenu2)) # Ingresamos elementos al menu
barmenu0.addElement(UIBarButton(115, "Editar Mezcla", fontsize, onclick, onpress, config_barmenu2))
barmenu0.addElement(UIBarButton(200, "Ingresar Colores", fontsize, onclick, onpress, config_barmenu2))
barmenu0.addElement(UIBarButton(115, "Ingresar Mezcla", fontsize, onclick, onpress, config_barmenu2))

barmenu1 = UIBarMenu(80, 45, "Cubo", fontsize, config_barmenu1) # Hacemos otro menu
barmenu1.addElement(UIBarButton(115, "2x2x2", fontsize, onclick, onpress, config_barmenu2)) # Tambien le damos elementos
barmenu1.addElement(UIBarButton(80, "3x3x3", fontsize, onclick, onpress, config_barmenu2))
barmenu1.addElement(UIBarButton(140, "Pyraminx", fontsize, onclick, onpress, config_barmenu2))
barmenu1.addElement(UIBarButton(80, "Skewb", fontsize, onclick, onpress, config_barmenu2))

barmenu2 = UIBarMenu(160, 45, "Personalizar", fontsize, config_barmenu1)
barmenu2.addElement(UIBarButton(115, "Colores", fontsize, onclick, onpress, config_barmenu2)) # Tambien le damos elementos
barmenu2.addElement(UIBarButton(115, "Fondos", fontsize, onclick, onpress, config_barmenu2)) # Tambien le damos elementos

botonvolverinicio = topbar.addBarElement(UIBarButton(40, " B ", fontsize, funcionvacia, funcionvacia, config_barmenu1))
topbar.addBarElement(barmenu0) #añadimos ambos menu a la barra superior
topbar.addBarElement(barmenu1)
topbar.addBarElement(barmenu2)

def buttonresolver():
    global modolibre, cubo_is_solving, inicioSolving, theta, theta0
    if not modolibre:
        cubo_is_solving = True
        inicioSolving = time.perf_counter()
        theta0 = theta
def buttonmodolibre():
    global startTurningTrigger, stopTurningTrigger, KEYPRESSED, ROTATING, inicio, theta0, modolibre, canmove
    if modolibre and canmove:
        stopTurningTrigger = True
        startTurningTrigger = False
        canmove = False
        inicio = time.perf_counter()
        modolibre = False
    else:
        if  not (startTurningTrigger) and not (py5.CONTROL in teclas_activas):#p
            startTurningTrigger = True
            stopTurningTrigger = False
            KEYPRESSED = True
            ROTATING = False
            inicio = time.perf_counter()
            theta0 = theta
            modolibre = True
def buttonmostrarsolve():
    global dict_reps1, dict_reps2, dict_reps3, dict_reps4
    solve = c333.getsolve(dict_reps1, dict_reps2, dict_reps3, dict_reps4)
    solvestr = ""
    for x in solve:
        solvestr += x
        if "\n" not in x: solvestr += " "
    ui.elements[textboxsolveid].text = "Solución:\n" + solvestr

barrasuperior = ui.addElement(topbar) # añadimos la barra a la interfaz
ui.addElement(UIText(26, 23, "3", 15, py5.color(255), ""))
botonresolverid = ui.addElement(UIButton(24, py5.height -54, 160, 30, "Resolver", 20, buttonresolver, funcionvacia, config_botones_principal))
botonmodolibreid = ui.addElement(UIButton(24, py5.height -94, 160, 30, "Modo libre", 20, buttonmodolibre, funcionvacia, config_botones_principal))
botonversolveid = ui.addElement(UIButton(24, py5.height -134, 160, 30, "Ver solución", 20, buttonmostrarsolve, funcionvacia, config_botones_principal))
textboxsolveid = ui.addElement(UITextBox(194, py5.height -131, py5.width - 184, py5.height -134, "Solución:", 20, py5.color(0), ""))
# endregion --- FIN INTERFAZ
obj = cube()    
#print(c333)
def settheta0(): # REINICIA LA ESCENA Y SUS VARIABLES CADA VEZ QUE ENTRAS EN LA ESCENA
    global theta, theta0, startTurningTrigger, stopTurningTrigger, ROTATING, KEYPRESSED, inicio, phi, scrambletext, c333, separation, canmove
    startTurningTrigger = False
    stopTurningTrigger = False
    ROTATING = True
    KEYPRESSED = False
    inicio = 0
    final = 0
    theta = 0
    phi = 0
    theta0 = 0
    scrambletext = ""
    c333 = ID_CUBO.copy()
    separation = 1
    canmove = False
    ui.elements[ui_texto_mezcla].text = "Mezcla: "
    ui.elements[textboxsolveid].text = "Solución:\n"
def animating():
    global theta, theta0, separation, phi, canmove, ROTATING, c333, inicioSolving, startTurningTrigger, stopTurningTrigger, startedSolving, cubo_is_solving, dict_reps1, dict_reps2, dict_reps3, dict_reps4
    if (cubo_is_solving):
        ROTATING = False
        if 0 <= (time.perf_counter() - inicioSolving) <= 0.5:
            if theta >= PI: theta = theta0 + (2*PI - theta0)*(time.perf_counter() - inicioSolving)/0.5
            elif theta <= PI: theta = theta0 - (theta0)*(time.perf_counter() - inicioSolving)/0.5
        elif not startedSolving: 
            c333.solve(dict_reps1, dict_reps2, dict_reps3, dict_reps4)
            startedSolving = True
            ui.elements[ui_texto_mezcla].text = "Mezcla: "
        if startedSolving and not c333.turning and c333 == ID_CUBO.copy():
            startedSolving = False
            ROTATING = True
            cubo_is_solving = False
            ui.elements[textboxsolveid].text = "Solución:\n"
    if ROTATING:
        theta += 2*PI - 0.01
        if (theta >= 2*PI): theta -= 2*PI
        if (theta <= 0): theta += 2*PI
    if startTurningTrigger:
        ROTATING = False
        if 0 <= time.perf_counter() - inicio <= 0.5: 
            if theta >= PI: theta = theta0 + (2*PI - theta0)*(time.perf_counter() - inicio)/0.5
            elif theta <= PI: theta = theta0 - (theta0)*(time.perf_counter() - inicio)/0.5
        elif 0.5 <= time.perf_counter() - inicio <= 1:
            t = time.perf_counter() - inicio - 0.5
            separation = 1 + 0.2/0.5*t
            phi = t*(PI/11)/0.5
        else: 
            theta = 0
            phi = PI/11
            separation = 1.2
            canmove = True
    if stopTurningTrigger:
        if 0 <= time.perf_counter() - inicio <= 0.5:
            t = time.perf_counter() - inicio
            separation = 1.2 - 0.2/0.5*t
            phi = PI/11 - t*(PI/11)/0.5
        else:
            ROTATING = True
            phi = 0
            separation = 1
            KEYPRESSED = False
    c333.display(separation)

# region crear 
b333 = Build333()
stickers = [""]*48

# endregion


def principal():
    ui.elements[botonresolverid].y = py5.height -46
    ui.elements[botonmodolibreid].y = py5.height -90
    ui.elements[botonversolveid].y = py5.height - 134
    ui.elements[textboxsolveid].y = py5.height -131
    ui.elements[textboxsolveid].width = py5.width - 184
    ui.elements[textboxsolveid].height = py5.height -134
    # global dict_reps1, dict_reps2, dict_reps3, dict_reps4
    # if dict_reps1 == []:
    #     dict_reps1, dict_reps2, dict_reps3, dict_reps4 = cola.get()

    global theta, theta0, separation, phi, canmove
    py5.background(color_fondo_pantalla_cubo)
    py5.translate(py5.width / 2, py5.height / 2, -100)
    py5.rotate_x(-PI/6 - phi)
    py5.rotate_y(theta)
    
    #animating()
    py5.rotate_x(-PI/11)
    b333.draw_centers()
    b333.draw_corners()
    b333.draw_edges()

    ui.drawElements() # dibujar ui



def keyeventpress():
    global KEYPRESSED, ROTATING, inicio, modolibre, theta0, theta, c333, cubo_is_solving, inicioSolving, canmove, startTurningTrigger, stopTurningTrigger, teclas_activas, dict_reps1, dict_reps2, dict_reps3, dict_reps4
    if py5.key == py5.CODED:
        teclas_activas.add(py5.key_code)
    else:
        # .lower() evita errores si sueltas Shift antes que la letra
        teclas_activas.add(str(py5.key).lower())

    if  (' ' in teclas_activas) and not (startTurningTrigger) and not (py5.CONTROL in teclas_activas) and not modolibre:#p
        startTurningTrigger = True
        stopTurningTrigger = False
        KEYPRESSED = True
        ROTATING = False
        inicio = time.perf_counter()
        theta0 = theta
        modolibre = True
    if  (py5.CONTROL in teclas_activas) and (CODIGOESPACIO in teclas_activas) and not modolibre:
        cubo_is_solving = True
        inicioSolving = time.perf_counter()
        theta0 = theta
    if canmove:
        if (py5.key in {'j', 'J', 'f', 'F', 'i', 'I', 'k', 'K', 'd', 'D', 'e', 'E', 'h', 'H', 'g', 'G', 's', 'S', 'l', 'L', 'w', 'W', 'o', 'O'}): ui.elements[ui_texto_mezcla].text = "Mezcla: "
        if py5.key == 'j' or py5.key == 'J': c333.turnU()
        if py5.key == 'f' or py5.key == 'F': c333.turnu()
        if py5.key == 'i' or py5.key == 'I': c333.turnR()
        if py5.key == 'k' or py5.key == 'K': c333.turnr()
        if py5.key == 'd' or py5.key == 'D': c333.turnL()
        if py5.key == 'e' or py5.key == 'E': c333.turnl()
        if py5.key == 'h' or py5.key == 'H': c333.turnF()
        if py5.key == 'g' or py5.key == 'G': c333.turnf()
        if py5.key == 's' or py5.key == 'S': c333.turnD()
        if py5.key == 'l' or py5.key == 'L': c333.turnd()
        if py5.key == 'w' or py5.key == 'W': c333.turnB()
        if py5.key == 'o' or py5.key == 'O': c333.turnb()
        if py5.key == ' ': 
            stopTurningTrigger = True
            startTurningTrigger = False
            canmove = False
            inicio = time.perf_counter()
            modolibre = False
    if (py5.key == "Q" or py5.key == 'q'):
        b333.set_corner_sticker("F")
    pass
def keyeventrelease():
    global teclas_activas
    if py5.key == py5.CODED:
        teclas_activas.discard(py5.key_code)
    else:
        teclas_activas.discard(str(py5.key).lower())
    if py5.key == ' ':
        teclas_activas.discard(CODIGOESPACIO)