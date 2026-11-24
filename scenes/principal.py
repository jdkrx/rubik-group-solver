import py5
import py5ui
import time
from .styles import *
from .cubos.cubo2x2 import cube
from .cubos.cubo3x3 import *
import random 

class Variables_globales:
    def __init__(self):
        # Objetos del cubo y tablas de búsqueda
        self.c333 = ID_CUBO.copy()
        self.b333 = Build333()
        self.obj_2x2 = cube()
        self.finished_building = True
        self.dict_reps = ([], [], [], [])  # Agrupa dict_reps1..4 en una tupla

        # Control de teclado
        self.teclas_activas = set()

        # Inicializa el resto de variables de cámara y animación
        self.reset()
    def reset(self):
        # Cámara y vista
        self.theta = 0.0
        self.phi = 0.0
        self.theta0 = 0.0
        self.separation = 1.0
        self.rotating = True

        # Estados de modo libre y animación
        self.modo_libre = False
        self.can_move = False
        self.start_turning = False
        self.stop_turning = False
        self.key_pressed = False
        self.inicio_anim = 0.0

        # Estados de resolución automática
        self.cubo_is_solving = False
        self.started_solving = False
        self.inicio_solving = 0.0

        # Datos de mezcla
        self.scramble_text = ""
        self.c333 = ID_CUBO.copy()

state = Variables_globales()

CODIGOESPACIO = 32
KEY_MOVES = {
    'j': 'U',
    'J': 'U',
    'f': "U'",
    'F': "U'",
    'i': 'R',
    'I': 'R',
    'k': "R'",
    'K': "R'",
    'd': 'L',
    'D': 'L',
    'e': "L'",
    'E': "L'",
    'h': 'F',
    'H': 'F',
    'g': "F'",
    'G': "F'",
    's': 'D',
    'S': 'D',
    'l': "D'",
    'L': "D'",
    'w': 'B',
    'W': 'B',
    'o': "B'",
    'O': "B'",
}

KEY_STICKERS = {
    'q': 'U',
    'Q': 'U',
    'w': 'L',
    'W': 'L',
    'e': 'F',
    'E': 'F',
    'r': 'R',
    'R': 'R',
    't': 'B',
    'T': 'B',
    'y': 'D',
    'Y': 'D',
}

BUILD_ANGLES = [
    (2 * PI / 11, 0),  # 0 - 7
    (0, PI / 2),  # 8 - 15
    (0, 0),  # 16 - 23
    (0, -PI / 2),  # 24 - 31
    (0, -PI),  # 32 - 39
    (-PI / 2, 0),  # 40 - 47
]

# FUNCIONES DE PRUEBA PARA LOS BOTONES, TODOS HACEN LO MISMO
def onclick():
    print("helloworld")
def onpress():
    print(f"mouse x: {py5.mouse_x}")

def generar_scramble_3x3(min_giros=20, max_giros=25):
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
    state.scramble_text = ""
    state.scramble_text += mezcla
    ui.elements[ui_texto_mezcla].text = "Mezcla: "
    ui.elements[ui_texto_mezcla].text += state.scramble_text
    state.c333 = ID_CUBO.copy()
    partes = mezcla.split(" ")
    if not mezcla == "":
        for i in partes:
            state.c333 = state.c333*genname(i)
    state.started_solving = False
    state.rotating = True
    state.cubo_is_solving = False

#----------- INTERFAZ --------------
ui = UIManager() # Creamos una interfaz para la ventana cubo

ui_texto_mezcla = ui.addElement(UIText(10, 60, f"Mezcla: {state.scramble_text}", 20, py5.color(0), ""))
sceenemanager = SceneManager()

topbar = UITopBar(45, config_barra) # Hacemo un elemento de barra superior
def buttoningresarcolores():
    state.b333 = Build333()
    state.finished_building = False
def buttonresolver():   
    if not state.modo_libre:
        state.cubo_is_solving = True
        state.inicio_solving = time.perf_counter()
        state.theta0 = state.theta
def buttonmodolibre():
    if state.modo_libre and state.can_move:
        state.stop_turning = True
        state.start_turning = False
        state.can_move = False
        state.inicio_anim = time.perf_counter()
        state.modo_libre = False
    elif not state.start_turning and py5.CONTROL not in state.teclas_activas:
        state.start_turning = True
        state.stop_turning = False
        state.key_pressed = True
        state.rotating = False
        state.inicio_anim = time.perf_counter()
        state.theta0 = state.theta
        state.modo_libre = True
def buttonmostrarsolve():
    solve = state.c333.getsolve(*state.dict_reps)
    solvestr = "".join(x if "\n" in x else f"{x} " for x in solve)
    ui.elements[textboxsolveid].text = "Solución:\n" + solvestr

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

barrasuperior = ui.addElement(topbar) # añadimos la barra a la interfaz
ui.addElement(UIText(26, 13, "3", 15, py5.color(255), ""))
botonresolverid = ui.addElement(UIButton(24, py5.height -54, 160, 30, "Resolver", 20, buttonresolver, funcionvacia, config_botones_principal))
botonmodolibreid = ui.addElement(UIButton(24, py5.height -94, 160, 30, "Modo libre", 20, buttonmodolibre, funcionvacia, config_botones_principal))
botonversolveid = ui.addElement(UIButton(24, py5.height -134, 160, 30, "Ver solución", 20, buttonmostrarsolve, funcionvacia, config_botones_principal))
textboxsolveid = ui.addElement(UITextBox(194, py5.height -131, py5.width - 184, py5.height -134, "Solución:", 20, py5.color(0), ""))
# ------------------ FIN INTERFAZ --------------------------


def settheta0(): # REINICIA LA ESCENA Y SUS VARIABLES CADA VEZ QUE ENTRAS EN LA ESCENA
    state.reset()
    ui.elements[ui_texto_mezcla].text = "Mezcla: "
    ui.elements[textboxsolveid].text = "Solución:\n"

# Traslada suavemente el angulo theta hacia 0 (o 2*PI) en 0.5 segundos.
def centrar_theta(dt):
  progreso = dt / 0.5
  if state.theta0 >= PI:
    state.theta = state.theta0 + (2 * PI - state.theta0) * progreso
  else:
    state.theta = state.theta0 * (1 - progreso)

# ESTA FUNCION SE ENCARGA DE ANIMAR EL CUBO EN LA TRANSICION DE MODO VISTA A MODO LIBRE O MODO AUTOMATICO
def animating():
  ahora = time.perf_counter()

  # MODO RESOLUCION AUTOMATICA
  if state.cubo_is_solving:
    state.rotating = False
    dt_solve = ahora - state.inicio_solving

    if dt_solve <= 0.5:
      centrar_theta(dt_solve)
    elif not state.started_solving:
      state.c333.solve(*state.dict_reps)
      state.started_solving = True
      ui.elements[ui_texto_mezcla].text = "Mezcla: "

    if (
        state.started_solving
        and not state.c333.turning
        and state.c333 == ID_CUBO
    ):
      state.started_solving = False
      state.rotating = True
      state.cubo_is_solving = False
      ui.elements[textboxsolveid].text = "Solución:\n"

  # ROTACION CONTINUA EN MODO VISTA
  if state.rotating:
    state.theta = (state.theta - 0.01) % (2 * PI)

  # TRANSICION DE ENTRADA AL MODO LIBRE
  if state.start_turning:
    state.rotating = False
    dt = ahora - state.inicio_anim

    if dt <= 0.5:
      centrar_theta(dt)
    elif dt <= 1.0:
      t = dt - 0.5
      progreso = t / 0.5
      state.separation = 1 + 0.2 * progreso
      state.phi = (PI / 11) * progreso
    else:
      state.theta = 0
      state.phi = PI / 11
      state.separation = 1.2
      state.can_move = True
      state.start_turning = False  # Apaga el trigger al terminar la transicion

  # TRANSICION DE SALIDA DEL MODO LIBRE
  if state.stop_turning:
    dt = ahora - state.inicio_anim

    if dt <= 0.5:
      progreso = dt / 0.5
      state.separation = 1.2 - 0.2 * progreso
      state.phi = (PI / 11) * (1 - progreso)
    else:
      state.rotating = True
      state.phi = 0
      state.separation = 1
      state.key_pressed = False
      state.stop_turning = False  # Apaga el trigger al terminar la transicion

def principal():
    # Actualizamos dinamicamente las coordenadas/tamaños de los objetos en la interfaz de usuario
    ui.elements[botonresolverid].y = py5.height -46
    ui.elements[botonmodolibreid].y = py5.height -90
    ui.elements[botonversolveid].y = py5.height - 134
    ui.elements[textboxsolveid].y = py5.height -131
    ui.elements[textboxsolveid].width = py5.width - 184
    ui.elements[textboxsolveid].height = py5.height -134
    if not state.dict_reps[0]:
        state.dict_reps = cola.get() # recibe los diccionarios desde la cola que carga en segundo plano

    if not state.finished_building: # fija las rotaciones para el modo introducir colores
        paso = min(state.b333.index // 8, 5)
        state.phi, state.theta = BUILD_ANGLES[paso]
    else:  
        animating()

    py5.background(color_fondo_pantalla_cubo)
    py5.translate(py5.width / 2, py5.height / 2, -100)
    py5.rotate_x(-PI/6 - state.phi)
    py5.rotate_y(state.theta)
     
    if not state.finished_building: # si falta cubo dibujaremos el cubo a medio armar
        state.b333.draw_centers()
        print(state.b333.get_available_colors(state.b333.index))
        state.b333.draw_stickers() 
    else: # Si el cubo a construir ya tiene todos los stickers dibujamos a c333
        state.c333.display(state.separation)
    ui.drawElements() # dibujar ui




def keyeventpress():
    global finishedbuildingcube, phi, KEYPRESSED, ROTATING, inicio, modolibre, theta0, theta, c333, cubo_is_solving, inicioSolving, canmove, startTurningTrigger, stopTurningTrigger, teclas_activas, dict_reps1, dict_reps2, dict_reps3, dict_reps4
    tecla = py5.key_code if py5.key == py5.CODED else str(py5.key).lower()
    state.teclas_activas.add(tecla)
    
    if not state.finished_building: # modo construir cubo
        if (py5.key in KEY_STICKERS):
            state.b333.set_sticker(KEY_STICKERS[py5.key])
            if state.b333.array[47] != -1:
                state.finished_building= True
                nuevo_cubo = state.b333.build()
                if nuevo_cubo:
                    state.c333 = nuevo_cubo
                    print("ok", state.c333)
                else: print("fallo build()")
                state.phi = 0
        elif (py5.key == ' '): state.b333.delete_sticker()
        return
    
    if state.can_move: # controles en modo libre
        if (py5.key in KEY_MOVES):  
            ui.elements[ui_texto_mezcla].text = "Mezcla: "
            state.c333.turn(KEY_MOVES[py5.key]) 
        elif py5.key == ' ' and state.finished_building: 
            buttonmodolibre() # sale del modo libre
        return 

    if not state.modo_libre : # activamos modo libre o resolucion automatica
        if (py5.CONTROL in state.teclas_activas) and (CODIGOESPACIO in state.teclas_activas): buttonresolver() # autosolve
        elif (' ' in state.teclas_activas): buttonmodolibre()        
     

def keyeventrelease():
    if py5.key == py5.CODED:
        state.teclas_activas.discard(py5.key_code)
    else:
        state.teclas_activas.discard(str(py5.key).lower())
    if py5.key == ' ':
        state.teclas_activas.discard(CODIGOESPACIO)
