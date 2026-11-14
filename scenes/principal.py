import py5
import py5ui
import time
from .styles import *
from math import pi as PI
from .cubos.cubo2x2 import cube
from .cubos.cubo3x3 import *
import random 

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


#--- INTERFAZ
ui = UIManager() # Creamos una interfaz para la ventana cubo

ui_texto_mezcla = ui.addElement(UIText(10, 70, f"Mezcla: {scrambletext}", 20, py5.color(0), ""))
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

barrasuperior = ui.addElement(topbar) # añadimos la barra a la interfaz
ui.addElement(UIText(26, 23, "3", 15, py5.color(255), ""))
#--- FIN INTERFAZ
obj = cube()
#print(c333)
def principal():
    global theta, theta0, separation, phi, canmove
    py5.background(color_fondo_pantalla_cubo)
    py5.translate(py5.width / 2, py5.height / 2, -100)
    py5.rotate_x(-PI/6 - phi)
    py5.rotate_y(theta)
    if ROTATING:
        theta += 2*PI - 0.01
        if (theta >= 2*PI): theta -= 2*PI
        if (theta <= 0): theta += 2*PI
    elif 0 <= time.perf_counter() - inicio <= 0.5: ## (2pi-theta0)*t
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
    c333.display(separation)

    ui.drawElements() # dibujar ui

def keyeventpress(key):
    global KEYPRESSED, theta0, theta, c333, canmove
    global ROTATING
    global inicio
    if not KEYPRESSED and key == " ":
        KEYPRESSED = True
        ROTATING = False
        inicio = time.perf_counter()
        theta0 = theta
    if canmove:
        if key == 'j' or key == 'J': c333 = c333*U
        if key == 'f' or key == 'F': c333 = c333*u
        if key == 'i' or key == 'I': c333 = c333*R
        if key == 'k' or key == 'K': c333 = c333*r
        if key == 'd' or key == 'D': c333 = c333*L
        if key == 'e' or key == 'E': c333 = c333*l
        if key == 'h' or key == 'H': c333 = c333*F
        if key == 'g' or key == 'G': c333 = c333*f
        if key == 's' or key == 'S': c333 = c333*D
        if key == 'l' or key == 'L': c333 = c333*d
        if key == 'w' or key == 'W': c333 = c333*B
        if key == 'o' or key == 'O': c333 = c333*b
        if c333 == ID_CUBO: canmove = False

    pass
def keyeventrelease(key):
    print(key)
    pass