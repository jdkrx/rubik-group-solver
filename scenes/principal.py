import py5
import py5ui
import time
from .styles import *
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
# Contribucion externa
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
    # fin contribucion externa
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
def buttoningresarcolores():
    global finishedbuildingcube, b333
    b333 = Build333()
    finishedbuildingcube = False
barmenu0 = UIBarMenu(115, 45, "Mezcla", fontsize, config_barmenu1) # creamos un menu
barmenu0.addElement(UIBarButton(120, "Nueva Mezcla", fontsize, generar_scramble_3x3, funcionvacia, config_barmenu2)) # Ingresamos elementos al menu
barmenu0.addElement(UIBarButton(115, "Editar Mezcla", fontsize, onclick, onpress, config_barmenu2))
barmenu0.addElement(UIBarButton(200, "Ingresar Colores", fontsize, buttoningresarcolores, funcionvacia, config_barmenu2))
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
c333 = ID_CUBO.copy()
b333 = Build333()
stickers = [""]*48

# endregion


# Caso identidad
b = Build333()
b.array = ["U"]*8 + ["L"]*8 + ["F"]*8 + ["R"]*8 + ["B"]*8 + ["D"]*8
b.index = 47
assert b.build() == ID_CUBO, "falla con el cubo resuelto"
print("ID_CUBO OK")

# Caso con cada movimiento
def to_array(r):
    """Convierte un Rubik333 en el array de 48 colores que vería el usuario."""
    def order(sset, tup):
        out, rem = [], list(sset)
        for c in tup:
            for s in rem:
                if indextocolor(s) == c:
                    out.append(s)
                    rem.remove(s)
                    break
        return out

    rho_inv = [0] * 8
    for i in range(8):
        rho_inv[r.rho[i]] = i
        
    sigma_inv = [0] * 12
    for i in range(12):
        sigma_inv[r.sigma[i]] = i

    arr = [-1] * 48
    for z in range(8):
        x = rho_inv[z]
        for k, s in enumerate(order(cornersid[z], corners[z])):
            arr[s] = corners[x][(r.v[z] + k) % 3]
    for z in range(12):
        x = sigma_inv[z]
        for k, s in enumerate(order(edgesid[z], edges[z])):
            arr[s] = edges[x][(r.w[z] + k) % 2]
    return arr
for name in ("U","R","F","D","L","B"):
    g = genname(name)
    b = Build333()
    b.array = to_array(g)
    b.index = 47
    assert b.build() == g, f"falla con {name}"
    print(f"{name} OK")

finishedbuildingcube = True
def principal():
    global finishedbuildingcube

    ui.elements[botonresolverid].y = py5.height -46
    ui.elements[botonmodolibreid].y = py5.height -90
    ui.elements[botonversolveid].y = py5.height - 134
    ui.elements[textboxsolveid].y = py5.height -131
    ui.elements[textboxsolveid].width = py5.width - 184
    ui.elements[textboxsolveid].height = py5.height -134
    global dict_reps1, dict_reps2, dict_reps3, dict_reps4
    if dict_reps1 == []:
        dict_reps1, dict_reps2, dict_reps3, dict_reps4 = cola.get()

    global theta, theta0, separation, phi, canmove
    py5.background(color_fondo_pantalla_cubo)
    py5.translate(py5.width / 2, py5.height / 2, -100)
    py5.rotate_x(-PI/6 - phi)
    py5.rotate_y(theta)  
    if not finishedbuildingcube:
        if (0 <= b333.index <= 7):
            phi = 2*PI/11
            theta = 0
        elif (8 <= b333.index <= 15):
            phi = 0
            theta = PI/2
        elif (16 <= b333.index <= 23):
            phi = 0
            theta = 0
        elif (24 <= b333.index <= 31):
            phi = 0
            theta = -PI/2
        elif (32 <= b333.index <= 39):
            phi = 0
            theta = -PI
        elif (40 <= b333.index <= 47):
            phi = -PI/2
            theta = 0
        if finishedbuildingcube:
            phi = 0
            theta = 0
    else:  
        animating()
    

    
    if not finishedbuildingcube:
        b333.draw_centers()
    
        print(b333.get_available_colors(b333.index))
        print(b333.edges)
        b333.draw_stickers() 
    ui.drawElements() # dibujar ui



def keyeventpress():
    global finishedbuildingcube, phi
    global KEYPRESSED, ROTATING, inicio, modolibre, theta0, theta, c333, cubo_is_solving, inicioSolving, canmove, startTurningTrigger, stopTurningTrigger, teclas_activas, dict_reps1, dict_reps2, dict_reps3, dict_reps4
    if py5.key == py5.CODED:
        teclas_activas.add(py5.key_code)
    else:
        # .lower() evita errores si sueltas Shift antes que la letra
        teclas_activas.add(str(py5.key).lower())

    if  (' ' in teclas_activas) and not (startTurningTrigger) and not (py5.CONTROL in teclas_activas) and not modolibre and finishedbuildingcube:#p
        startTurningTrigger = True
        stopTurningTrigger = False
        KEYPRESSED = True
        ROTATING = False
        inicio = time.perf_counter()
        theta0 = theta
        modolibre = True
    if  (py5.CONTROL in teclas_activas) and (CODIGOESPACIO in teclas_activas) and not modolibre and finishedbuildingcube:
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
        if py5.key == ' ' and finishedbuildingcube: 
            stopTurningTrigger = True
            startTurningTrigger = False
            canmove = False
            inicio = time.perf_counter()
            modolibre = False
    if finishedbuildingcube: return
    if (py5.key == "Q" or py5.key == 'q'):
        b333.set_sticker("U")
    if (py5.key == "w" or py5.key == 'W'):
        b333.set_sticker("L")
    if (py5.key == "e" or py5.key == 'E'):
        b333.set_sticker("F")
    if (py5.key == "r" or py5.key == 'R'):
        b333.set_sticker("R")
    if (py5.key == "t" or py5.key == 'T'):
        b333.set_sticker("B")
    if (py5.key == "y" or py5.key == 'Y'):
        b333.set_sticker("D")
    if (py5.key == " " and not finishedbuildingcube): b333.delete_sticker()
    if (b333.array[47] != -1 and py5.key in {"q", "Q", "w", "W", "e", "E", "r", "R", "t", "T", "y", "Y"}):
        finishedbuildingcube = True
        try:
            c333 = b333.build()
            print("OK:", c333)
        except ValueError as e:
            print("Fallo build():", e)
            b333.diagnose()
        phi = 0
    pass
def keyeventrelease():
    global teclas_activas
    if py5.key == py5.CODED:
        teclas_activas.discard(py5.key_code)
    else:
        teclas_activas.discard(str(py5.key).lower())
    if py5.key == ' ':
        teclas_activas.discard(CODIGOESPACIO)
