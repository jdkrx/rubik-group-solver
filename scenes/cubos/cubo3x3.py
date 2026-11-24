import py5 #3d
import json
from pathlib import Path
import queue
from math import pi as PI
from time import perf_counter as getTime
from representantes import get_reps1, get_reps2, get_reps3, get_reps4

cola = queue.Queue()

def obtener_firma_G0_G1(g):
    w_tupla = tuple(g.w)
    return w_tupla
def obtener_firma_G1_G2(g):
    v_tupla = tuple(g.v)
    e_slice_set = tuple(sorted(g.sigma[4:8]))
    return (v_tupla, e_slice_set)
def obtener_firma_G2_G3(estado):
    aristas = tuple(sorted(estado.sigma[i] for i in (0, 2, 8, 10)))
    rho = estado.rho
    esquinas = min(tuple(rho[h[i]] for i in range(8)) for h in H)
    return (aristas, esquinas)
def obtener_firma_G3_G4(g):
    v_tupla = tuple(g.v)
    w_tupla = tuple(g.w)
    rho = tuple(g.rho)
    sigma = tuple(g.sigma)
    return (v_tupla, w_tupla, rho, sigma)
def configurararchivos(cola):
    archivoreps1, archivoreps2, archivoreps3, archivoreps4 = False, False, False, False
    repscamino1, repscamino2, repscamino3, repscamino4 = [], [], [], []
    URL = str(Path(__file__).resolve().parent) + "/../../representantes"
    try:
        with open(f'{URL}/G0-G1.json', 'r', encoding='utf-8') as file:
            repscamino1 = json.load(file)
        archivoreps1 = True
    except FileNotFoundError:
        print("Faltan los representantes de G0/G1")
    try:
        with open(f'{URL}/G1-G2.json', 'r', encoding='utf-8') as file:
            repscamino2 = json.load(file)
        archivoreps2 = True
    except FileNotFoundError:
        print("Faltan los representantes de G1/G2")
    try:
        with open(f'{URL}/G2-G3.json', 'r', encoding='utf-8') as file:
            repscamino3 = json.load(file)
        archivoreps3 = True
    except FileNotFoundError:
        print("Faltan los representantes de G2/G3")
    try:
        with open(f'{URL}/G3-G4.json', 'r', encoding='utf-8') as file:
            repscamino4 = json.load(file)
        archivoreps4 = True
    except FileNotFoundError:
        print("Faltan los representantes de G1/G4")
    if not archivoreps1:
        get_reps1()
        with open(f'{URL}/G0-G1.json', 'r', encoding='utf-8') as file:
            repscamino1 = json.load(file)
        archivoreps1 = True
    if not archivoreps2:
        get_reps2()
        with open(f'{URL}/G1-G2.json', 'r', encoding='utf-8') as file:
            repscamino2 = json.load(file)
        archivoreps2 = True
    if not archivoreps3:
        get_reps3()
        with open(f'{URL}/G2-G3.json', 'r', encoding='utf-8') as file:
            repscamino3 = json.load(file)
        archivoreps3 = True
    if not archivoreps4:
        get_reps4()
        with open(f'{URL}/G3-G4.json', 'r', encoding='utf-8') as file:
            repscamino4 = json.load(file)
        archivoreps4 = True
    def construir_dict(caminos, obtener_firma):
        d = {}
        for camino in caminos:
            g = ID_CUBO
            for mov in camino:
                g = g * genname(mov)
            d[obtener_firma(g)] = camino
        return d
    inicioconfig = getTime()
    pasos = [
        (repscamino1, obtener_firma_G0_G1),
        (repscamino2, obtener_firma_G1_G2),
        (repscamino3, obtener_firma_G2_G3),
        (repscamino4, obtener_firma_G3_G4),
    ]
    dict_reps1, dict_reps2, dict_reps3, dict_reps4 = (construir_dict(caminos, firma) for caminos, firma in pasos)
    finalconfig = getTime()
    # print(f"Tiempo configurando los representantes: {finalconfig - inicioconfig} segundos") #
    cola.put((dict_reps1, dict_reps2, dict_reps3, dict_reps4))

# Buscar Solve con el metodo de Thistlethwaite
def buscarsolvetw(scramble, dict_reps1, dict_reps2, dict_reps3, dict_reps4, spacing): 
    alg1 = dict_reps1[obtener_firma_G0_G1(scramble)] 
    # Comprobamos que representante lleva el estado entregado del cubo desde el grupo G0 al subgrupo G1
    # algX es un array con los giros en formato de texto para pasar de etapa
    # Note que no necesitamos verificar que el cubo está armado antes de buscar la solución
    # porque el estado identidad ya es un representante de clase en cada paso Gi-Gi+1
    sol1 = [] # Esta lista guarda los movimientos en el orden correcto para pasar de G0 a G1
    for i in alg1[::-1]: 
        # Los representantes asumen giros inversos, por lo que el algoritmo real que nos mueve
        # Primero calculamos que giro como objeto corresponde al texto que hay en i
        # Luego lo invertimos segun la formula dada en la clase Rubik333
        # y lo pasamos a texto denuevo
        gen = namegen(genname(i).inverso()) 
        sol1.append(gen) # Sol1 guarda la solución hasta el momento
    g1 = ID_CUBO.copy() # incializamos un objeto Rubik333 copiando el cubo armado 
    for i in alg1:
        g1 = g1*genname(i) # calculamos el inverso de nuestra solución hasta el momento
    if (scramble*g1.inverso() == ID_CUBO): 
        # Si nuestra mezcla por el inverso de nuestra solucion es el estado armado quiere decir que nuestra parte de la solución 
        # es enrealidad toda la solución y el cubo ya está armado
        solfinal = sol1 # Nuestra solucion final es lo que llevamos hasta ahora
        return (solfinal) # Y retornamos la solucion
    if spacing: sol1 += [" // (EO)\n"] # El flag spacing sirve para poder mostrar en que paso vamos hasta ahora en el string de solucion
    # EO -> Edges Orientated, las aristas del cubo están orientadas respecto al eje Z
    # Un cubo con aristas orientadas en el eje Z no necesita movimientos del tipo F, F', B, B'
    # Si puede necesitar giros dobles de esas caras pues los giros dobles no alteran la orientacion de aristas
    # Hasta aqui llega el primer paso G0->G1

    # Repetimos el proceso para el paso 2
    # Hasta ahora tenemos scramble que es el estado del cubo desarmado
    # y tambien tenemos g1 como objeto Rubik333, que es el primer representante de nuestra solucion
    # entonces scramble * g1.inverso() corresponde al estado del cubo ejecutando los primeros pasos de la solucion i.e. el estado "actual" del cubo
    # a partir de aqui el codigo es casi lo mismo que antes otras 3 veces mas para completar el metodo de 4 fases de Thistlethwaite
    alg2 = dict_reps2[obtener_firma_G1_G2(scramble*g1.inverso())] # comprobamos que representante de G1/G2 corresponde al estado actual
    sol2 = []
    for i in alg2[::-1]:
        gen = namegen(genname(i).inverso())
        sol2.append(gen)
    g2 = ID_CUBO
    for i in alg2:
        g2 = g2*genname(i)
    if (scramble*g1.inverso()*g2.inverso() == ID_CUBO):
        solfinal = sol1 + sol2
        return (solfinal)
    if spacing: sol2 += [" // (DR)\n"] # DR -> Domino Reduction
    # La reducción Domino quiere decir que el cubo tiene todas las esquinas orientadas,
    # ademas las aristas estan orientadas en el eje Z y tambien en el eje X
    # la orientacion de aristas en el eje X hace que no sean necesarios los giros del tipo R, R', L, L'
    # y nuevamente los giros dobles de estas caras siguen estando permitidos
    alg3 = dict_reps3[obtener_firma_G2_G3(scramble*g1.inverso()*g2.inverso())]
    sol3 = []
    for i in alg3[::-1]:
        gen = namegen(genname(i).inverso())
        sol3.append(gen)
    g3 = ID_CUBO
    for i in alg3:
        g3 = g3*genname(i)
    if (scramble*g1.inverso()*g2.inverso()*g3.inverso() == ID_CUBO):
        solfinal = sol1 + sol2 + sol3
        return (solfinal)
    if spacing: sol3 += [" // (HTR)\n"] # HTR -> Half Turn Reduction
    # El cubo en reduccion de medios giros es un cubo que tiene las esquinas correctamente orientadas
    # y las aristas están orientadas en los 3 ejes X, Y, Z, se puede identificar porque cada cara tiene solo
    # el color correspondiente a esa cara o el color de la cara opuesta
    # como la orientacion de aristas en cada eje elimina los cuartos de giros en ese eje, un cubo en HTR solo necesita medios giros para armarlo
    alg4 = dict_reps4[obtener_firma_G3_G4(scramble*g1.inverso()*g2.inverso()*g3.inverso())]
    sol4 = []
    for i in alg4[::-1]:
        gen = namegen(genname(i).inverso())
        sol4.append(gen)
    solfinal = sol1 + sol2 + sol3 + sol4 # Si el cubo llego hasta este paso solo puede estar armado
    # por lo que no hacemos un check de si esta armado o no, esto esta probado por el teorema de los metodos de subgrupos.
    return (solfinal) # entregamos la solucion final

# un array con las instrucciones para llegar a cada arista del cubo
# [ (rotacionx, rotaciony), translate(x, y, z) ] -> id de pieza en el espacio de aristas
setcoordedges = [
    [(0, PI), (0, -80, -80)],       # UB
    [(0, PI/2), (80, -80, 0)],      # UR
    [(0, 0), (0, -80, 80)],         # UF
    [(0, -PI/2), (-80, -80, 0)],    # UL
    [(PI/2, -PI/2), (-80, 0, -80)], # BL
    [(-PI/2, -PI/2), (-80, 0, 80)], # FL
    [(-PI/2, PI/2), (80, 0, 80)],   # FR
    [(PI/2, PI/2), (80, 0, -80)],   # BR
    [(PI, PI), (0, 80, 80)],        # DF
    [(PI, PI/2), (80, 80, 0)],      # DR
    [(PI, 0), (0, 80, -80)],        # DB
    [(PI, -PI/2), (-80, 80, 0)]     # DL
]
# un array con las instrucciones para llegar a cada arista del cubo
# [ (rotacionx, rotaciony), translate(x, y, z) ] -> id de pieza en el espacio de arista
setcoordcorners = [
    [(0, PI), (-80, -80, -80)],   # UBL
    [(0, PI/2), (80, -80, -80)],  # UBR
    [(0, 0), (80, -80, 80)],      # UFR
    [(0, -PI/2), (-80, -80, 80)], # UFL
    [(PI, PI), (-80, 80, 80)],    # DFL
    [(PI, PI/2), (80, 80, 80)],   # DFR
    [(PI, 0), (80, 80, -80)],     # DBR
    [(PI, -PI/2), (-80, 80, -80)] # DBL
]
# un array con las instrucciones para llegar a cada centro del cubo
# [ (rotacionx, rotaciony), translate(x, y, z) ] -> id de centro
setcoordcenters = [
    [(-PI/2, 0), (0, -120, 0)],
    [(0, PI/2), (-120, 0, 0)],
    [(0, 0), (0, 0, 120)],
    [(0, PI/2), (120, 0, 0)],
    [(0, 0), (0, 0, -120)],
    [(PI/2, 0), (0, 120, 0)],
]
# un array con las instrucciones para llegar a cada sticker del cubo
# [ (rotacionx, rotaciony), translate(x, y, z) ] -> id del sticker en el espacio de pegatinas
setcoordstickers = [
    [(PI/2, 0), (-80, -120, -80)],               #0     #U
    [(PI/2, 0), (0, -120, -80)],                 #1
    [(PI/2, 0), (80, -120, -80)],                #2
    [(PI/2, 0), (80, -120, 0)],                  #3
    [(PI/2, 0), (80, -120, 80)],                 #4
    [(PI/2, 0), (0, -120, 80)],                  #5
    [(PI/2, 0), (-80, -120, 80)],                #6
    [(PI/2, 0), (-80, -120, 0)],                 #7     #U
    [(0, PI/2), (-120, -80,-80)],                #8     #L
    [(0, PI/2), (-120, -80, 0)],                 #9
    [(0, PI/2), (-120, -80, 80)],                #10
    [(0, PI/2), (-120, 0, 80)],                  #11
    [(0, PI/2), (-120, 80, 80)],                 #12
    [(0, PI/2), (-120, 80, 0)],                  #13
    [(0, PI/2), (-120, 80, -80)],                #14
    [(0, PI/2), (-120, 0, -80)],                 #15    #L
    [(0, 0), (-80, -80, 120)],                   #16    #F
    [(0, 0), (0, -80, 120)],                     #17
    [(0, 0), (80, -80, 120)],                    #18
    [(0, 0), (80, 0, 120)],                      #19
    [(0, 0), (80, 80, 120)],                     #20
    [(0, 0), (0, 80, 120)],                      #21
    [(0, 0), (-80, 80, 120)],                    #22
    [(0, 0), (-80, 0, 120)],                     #23    #F
    [(0, PI/2), (120, -80, 80)],                 #24    #R
    [(0, PI/2), (120, -80, 0)],                  #25
    [(0, PI/2), (120, -80, -80)],                #26
    [(0, PI/2), (120, 0, -80)],                  #27
    [(0, PI/2), (120, 80, -80)],                 #28
    [(0, PI/2), (120, 80, 0)],                   #29
    [(0, PI/2), (120, 80, 80)],                  #30
    [(0, PI/2), (120, 0, 80)],                   #31    #R
    [(0, 0), (80, -80, -120)],                   #32    #B
    [(0, 0), (0, -80, -120)],                    #33
    [(0, 0), (-80, -80, -120)],                  #34
    [(0, 0), (-80, 0, -120)],                    #35
    [(0, 0), (-80, 80, -120)],                   #36
    [(0, 0), (0, 80, -120)],                     #37
    [(0, 0), (80, 80, -120)],                    #38
    [(0, 0), (80, 0, -120)],                     #39    #B
    [(PI/2, 0), (-80, 120, 80)],                 #40    #D
    [(PI/2, 0), (0, 120, 80)],                   #41
    [(PI/2, 0), (80, 120, 80)],                  #42
    [(PI/2, 0), (80, 120, 0)],                   #43
    [(PI/2, 0), (80, 120, -80)],                 #44
    [(PI/2, 0), (0, 120, -80)],                  #45
    [(PI/2, 0), (-80, 120, -80)],                #46
    [(PI/2, 0), (-80, 120, 0)]                   #47    #D
 ]
faces = ["U", "L", "F", "R", "B", "D"]
# Paleta de colores del cubo a dibujar
palette = {
    "U": py5.color(255, 255, 255),
    "L": py5.color(255, 128, 0),
    "F": py5.color(0,255,0),
    "R": py5.color(255, 0, 0),
    "B": py5.color(0, 0, 255),
    "D": py5.color(255, 255, 0)
}
# Le asignamos un ID a cada arista del cubo
# La convencion general es partir con las 4 aristas de la cara superior
# numerando primero UB y se sigue en sentido horario
# para la capa E seleccionamos BL y rotamos en direccion FL manteniendose en esa capa
# para ordenar la capa D rote el cubo en el eje X 180 grados y continue la numeracion igual que la capa U
edges = [
    ("U", "B"), # 0
    ("U", "R"), # 1
    ("U", "F"), # 2
    ("U", "L"), # 3
    ("B", "L"), # 4
    ("F", "L"), # 5
    ("F", "R"), # 6
    ("B", "R"), # 7
    ("D", "F"), # 8
    ("D", "R"), # 9
    ("D", "B"), # 10
    ("D", "L")  # 11
]
# Para las esquinas las ordenamos de forma similar
# Partimos con UBL y rotamos en sentido horario
# para la capa D rotamos 180 grados en el eje X y seguimos la misma convencion de la capa U
corners = [
    ("U", "B", "L"), # 0
    ("U", "R", "B"), # 1
    ("U", "F", "R"), # 2
    ("U", "L", "F"), # 3
    ("D", "F", "L"), # 4
    ("D", "R", "F"), # 5
    ("D", "B", "R"), # 6
    ("D", "L", "B")  # 7
]
# Guardamos un set de las piezas en forma de tupla en cada capa (esquinas y aristas de la cara que corresponda) del cubo
# Estos nos serviran para detectar que piezas son parte de la capa que se esté girando y 
# podemos filtrarlas en el renderizado para ejecutar una animacion de rotacion
F_LAYER = {
    ("U", "F"),
    ("F", "L"),
    ("F", "R"),
    ("D", "F"),
    ("U", "F", "R"),
    ("U", "L", "F"),
    ("D", "F", "L"),
    ("D", "R", "F")
}
B_LAYER = {
    ("U", "B"),
    ("B", "L"),
    ("B", "R"),
    ("D", "B"),
    ("U", "B", "L"),
    ("U", "R", "B"),
    ("D", "B", "R"),
    ("D", "L", "B")
}
U_LAYER = {
    ("U", "B"),
    ("U", "R"),
    ("U", "F"),
    ("U", "L"),
    ("U", "B", "L"),
    ("U", "R", "B"),
    ("U", "F", "R"),
    ("U", "L", "F"),
}
L_LAYER = {
    ("U", "L"),
    ("F", "L"),
    ("D", "L"),
    ("B", "L"),
    ("U", "B", "L"),
    ("U", "L", "F"),
    ("D", "F", "L"),
    ("D", "L", "B")
}
R_LAYER = {
    ("U", "R"),
    ("F", "R"),
    ("D", "R"),
    ("B", "R"),
    ("U", "R", "B"),
    ("U", "F", "R"),
    ("D", "R", "F"),
    ("D", "B", "R")
}
D_LAYER = {
    ("D", "F"),
    ("D", "R"),
    ("D", "B"),
    ("D", "L"),
    ("D", "F", "L"),
    ("D", "R", "F"),
    ("D", "B", "R"),
    ("D", "L", "B")
}
# un diccionario que a cada cara le asigna una capa
layers = {
    "U": U_LAYER,
    "D": D_LAYER,
    "R": R_LAYER,
    "L": L_LAYER,
    "F": F_LAYER,
    "B": B_LAYER
}

# una pieza debe ser 80x80x80
def drawEdge(edge, orientation, t): # t es un parametro que sirve para estirar las piezas del cubo en el modo libre
    # edge = (face0, face1)
    # ejemplo: edge = ("U", "F")
    # las piezas son tuplas como las de los conjuntos de capas
    if orientation == 1: edge = edge[::-1] # para ahorrar codigo si la pieza tiene la orientacion contraria solo damos vuelta la tupla
    # orientation es una variable que debe tomar dos valores, 0 o 1
    # el valor 0 corresponde a una arista orientada
    # y el valor 1 a una arista desorientada
    # podriamos usar un booleano pero el valor numerico
    # se entiende mejor para nuestro marco teorico
    py5.stroke(0) # Los bordes seran de color negro
    py5.rect_mode(py5.CENTER) # Como tenemos las coordenadas de los centros de las piezas nos conviene dibujar cuadrados desde el centro
    # Cada dibujo viene antes con una traslacion al centro de la cara del sticker
    # y despues una rotacion para poder dibujar el cuadrado correctamente
    # despues de dibujar retrocedemos la rotacion y la traslacion en ese orden para volver a nuestro origen
    stickers = {
        1: ((0, 0, 40 * t), (0, 0)),
        0: ((0, -40 * t, 0), (PI / 2, 0))
    }
    for idx, (pos, rot) in stickers.items(): # transformamos el diccionario en varios pares de elementos para recorrer las transformaciones de cada sticker
        py5.fill(palette[edge[idx]]) # seleccionamos el color de la paleta que le correspopnde al primer sticker de la arista
        with py5.push_matrix(): # guardamos las transformaciones actuales para poder trasladar y rotar a gusto y que al salir de with se reinicien las transformaciones
            py5.translate(*pos)
            if rot: py5.rotate_x(rot[0])
            if rot: py5.rotate_y(rot[1])
            py5.rect(0, 0, 80, 80)
    py5.rect_mode(py5.CORNER)

# Esta funcion es muy similar a la de dibujar arista pero simplemente debemos dibujar una cara mas, se siguen las mismas convenciones que del marco teorico
def drawCorner(corner, orientation, t):
    if orientation == 1:  corner = (corner[1], corner[2], corner[0]) # la orientacion en este caso toma 3 valores
    if orientation == 2:  corner = (corner[2], corner[0], corner[1]) 
    # el valor de orientation es cuantos giros de 120 grados en sentido anti horario se necesitan para tener la esquina orientada
    py5.stroke(0)
    py5.rect_mode(py5.CENTER)
    stickers = {
        1: ((0, 0, 40 * t), (0, 0)),
        0: ((0, -40 * t, 0), (PI / 2, 0)),
        2: ((40 * t, 0, 0), (0, PI / 2)),
    }
    for idx, (pos, rot) in stickers.items(): # transformamos el diccionario en varios pares de elementos para recorrer las transformaciones de cada sticker
        py5.fill(palette[corner[idx]])
        with py5.push_matrix():
            py5.translate(*pos)
            if rot: py5.rotate_x(rot[0])
            if rot: py5.rotate_y(rot[1])
            py5.rect(0, 0, 80, 80)
    py5.rect_mode(py5.CORNER)

def drawSticker(index, color): # Seguimos la misma logica que para las funciones anteriores pero con solo una cara
    py5.stroke(0)
    py5.rect_mode(py5.CENTER)
    a = setcoordstickers[index][1][0]
    b = setcoordstickers[index][1][1]
    c = setcoordstickers[index][1][2]
    with py5.push_matrix():
        py5.translate(a, b, c)
        py5.fill(palette[color])
        py5.rotate_x(setcoordstickers[index][0][0])
        py5.rotate_y(setcoordstickers[index][0][1])
        py5.rect(0, 0, 80, 80)

# Esta es la clase que describe el comportamiento del cubo segun nuestro marco teorico usando la teoria de grupos
# ademas le añadimos funciones que nos permiten dibujar el cubo y animar sus giros
class Rubik333:
    def __init__(self, v, w, rho, sigma):
        self.v = v[:] # vector de orientacion de vertices, son elementos de (Z_3)^8
        self.w = w[:] # vector de orientacion de aristas, son elementos de (Z_2)^12
        self.rho = rho[:] # permutacion de esquinas, es un elemento de S_8
        self.sigma = sigma[:] # permutacion de aristas, es un elemento de S_12 
        self.inicio = 0 # una variable que nos guarda la marca temporal de cuando se inicia la animacion de girar una cara
        self.startTurningtrigger = False # par de variables que indican cuando se inicia/termina la animacion de giro
        self.stopTurningtrigger = False
        self.faceToTurn = "" # un indicador de que cara se esta girando
        self.direction = 1 # nos dice si el giro es horario (1) o antihorario (-1)

        self.toSolve = [] # Aqui guardamos la solucion que debe auto ejecutar el cubo en modo autosolve
        self.turning = False # nos dice si el cubo esta en medio un giro en una solucion automatica 
        self.iniciosolve = 0 # marca de tiempo cuando empieza a resolverse
        self.index = 0 # en que paso va de la solucion
    def __repr__(self): # esta funcion nos permitia testear con estados del cubo antes de la interfaz grafica
        return f"v:{self.v}\nw:{self.w}\nrho:{self.rho}\nsigma:{self.sigma}" 
    def __mul__(self, otro): # aqui realizamos el algoritmo de composicion de estados siguiendo la 
        # convencion estado actual*giro que se va a hacer ahora
        # ejemplo ID_CUBO*R*U es tomar un cubo armado, ejecutar R y despues U
        # esta convencion es necesaria pues la teoria matematica se fue desarrollando con composiciones matematicas
        # que se ejecutan de derecha a izquierda

        # debemos seguir la formula 
        # (v, w, rho1, sigma1)*(x, y, rho2, sigma2) = ( x + rho2(v), y + sigma2(w), rho2*rho1, sigma2*sigma1 )
        # la multiplicacion de permutaciones se refiere a su composicion como funciones biyectivas

        rho_inv = [0]*8
        sigma_inv = [0]*12

        for i in range(8): rho_inv[otro.rho[i]] = i
        for i in range(12): sigma_inv[otro.sigma[i]] = i

        nuevo_v = [(otro.v[i] + self.v[rho_inv[i]]) % 3 for i in range(8)] # la suma aqui es modulo 3 coordenada a coordenada (Z_3)^8
        nuevo_w = [(otro.w[i] + self.w[sigma_inv[i]]) % 2 for i in range(12)] # la suma aqui es modulo 2 coordenada a coordenada (Z_2)^12

        nuevo_rho = [otro.rho[self.rho[i]] for i in range(8)]
        nuevo_sigma = [otro.sigma[self.sigma[i]] for i in range(12)]
        return Rubik333(nuevo_v, nuevo_w, nuevo_rho, nuevo_sigma)
    def mul(self, otro): # tenemos otra funcion por si queremos calcular una multiplicacion alterando el estado del objeto Rubik333
        rho_inv = [0]*8
        sigma_inv = [0]*12

        for i in range(8): rho_inv[otro.rho[i]] = i
        for i in range(12): sigma_inv[otro.sigma[i]] = i

        nuevo_v = [(otro.v[i] + self.v[rho_inv[i]]) % 3 for i in range(8)]
        nuevo_w = [(otro.w[i] + self.w[sigma_inv[i]]) % 2 for i in range(12)]

        nuevo_rho = [otro.rho[self.rho[i]] for i in range(8)]
        nuevo_sigma = [otro.sigma[self.sigma[i]] for i in range(12)]
        self.v = nuevo_v
        self.w = nuevo_w
        self.rho = nuevo_rho
        self.sigma = nuevo_sigma
    def inverso(self): # La inversion la hacemos por medio de la siguiente formula
        # (v, w, rho, sigma)^-1 = (-rho^-1(v), -sigma^-1(w), rho^-1, sigma^-1)

        inv_rho = [0] * 8
        for i in range(8): inv_rho[self.rho[i]] = i
        inv_sigma = [0] * 12
        for i in range(12): inv_sigma[self.sigma[i]] = i
        inv_v = [(-self.v[self.rho[i]]) % 3 for i in range(8)]
        inv_w = [(-self.w[self.sigma[i]]) % 2 for i in range(12)]
        return Rubik333(inv_v, inv_w, inv_rho, inv_sigma)
    def __eq__(self, otro): # Redefinimos la igualdad de objetos Rubik333
        # sin esto la igualdad Rubik333_1 == Rubik333_2 solo es True si ambos objetos tienen la misma referencia
        if not isinstance(otro, Rubik333): # primero chequeamos que el objeto a comparar sea del tipo Rubik
            return False
        return (self.v == otro.v) and (self.w == otro.w) and (self.rho == otro.rho) and (self.sigma == otro.sigma) # definimos igualdad componente a componente
    def copy(self): # entregamos una copia del cubo construyendolo denuevo con los mismos valores de estado iniciales 
        return Rubik333(self.v, self.w, self.rho, self.sigma)
    def display(self, t): # en esta funcion dibujamos el cubo en la interfaz grafica
        if self.index != len(self.toSolve) and not self.turning:
            move = self.toSolve[self.index]
            self.turn(move.replace("2", ""))
            self.turning = True
        if (self.index < len(self.toSolve) and getTime() - self.inicio > 1.75):
            self.iniciosolve = getTime()
            self.turning = False
            if not ("2" in self.toSolve[self.index]):
                self.index += 1
            else:
                self.toSolve[self.index] = self.toSolve[self.index].replace("2", "")
        if(self.v == [0]*8 and self.w == [0]*12 and self.rho == range(8) and self.sigma == range(12)):
            self.toSolve = []
            self.turning = False
            self.iniciosolve = 0
            self.index = 0
        axes = {
            "R": (1, 0, 0),
            "L": (-1, 0, 0),
            "U": (0, -1, 0),
            "D": (0, 1, 0),
            "F": (0, 0, 1),
            "B": (0, 0, -1)
        }
        for z in range(12): # DRAW EDGES
            x = self.sigma[z]
            sigmainversa = [0]*12
            for i in range(12): sigmainversa[self.sigma[i]] = i
            x = sigmainversa[z]
            y = self.w[z]
            a = setcoordedges[z][1][0]
            b = setcoordedges[z][1][1]
            c = setcoordedges[z][1][2] 
            with py5.push_matrix():
                if self.faceToTurn != "" and self.startTurningtrigger:
                    if (edges[z] in layers[self.faceToTurn]):
                        if (getTime() - self.inicio >= 0.2):
                            self.stopTurningtrigger = True
                        if self.faceToTurn in axes: 
                            angle = self.direction*(getTime() - self.inicio)*PI/(2*0.2)
                            py5.rotate(angle, *axes[self.faceToTurn])
                py5.translate(a*t, b*t, c*t)
                py5.rotate_x(setcoordedges[z][0][0])
                py5.rotate_y(setcoordedges[z][0][1])
                drawEdge(edges[x], y, t)
        for z in range(8): # DRAW CORNERS
            x = self.rho[z]
            rhoinversa = [0]*8
            for i in range(8): rhoinversa[self.rho[i]] = i
            x = rhoinversa[z]
            y = self.v[z]
            a = setcoordcorners[z][1][0]
            b = setcoordcorners[z][1][1]
            c = setcoordcorners[z][1][2]
            with py5.push_matrix():
                if self.faceToTurn != "" and self.startTurningtrigger:
                    if (corners[z] in layers[self.faceToTurn]):
                        if (getTime() - self.inicio >= 0.2):
                            self.stopTurningtrigger = True
                        if self.faceToTurn in axes:
                            angle = self.direction*(getTime() - self.inicio)*PI/(2*0.2)
                            py5.rotate(angle, *axes[self.faceToTurn])
                py5.translate(a*t, b*t, c*t)
                py5.rotate_x(setcoordcorners[z][0][0])
                py5.rotate_y(setcoordcorners[z][0][1])
                drawCorner(corners[x], y, t)
        for z in range(6): # DRAW CENTERS
            a = setcoordcenters[z][1][0]
            b = setcoordcenters[z][1][1]
            c = setcoordcenters[z][1][2]
            with py5.push_matrix():
                if self.faceToTurn != "" and self.startTurningtrigger:
                    if (faces[z] == self.faceToTurn):
                        if (getTime() - self.inicio >= 0.2):
                            self.stopTurningtrigger = True
                        if self.faceToTurn in axes:
                            angle = self.direction*(getTime() - self.inicio)*PI/(2*0.2)
                            py5.rotate(angle, *axes[self.faceToTurn])
                py5.translate(a*t, b*t, c*t)
                py5.rotate_x(setcoordcenters[z][0][0])
                py5.rotate_y(setcoordcenters[z][0][1])
                py5.fill(palette[faces[z]])
                py5.rect_mode(py5.CENTER)
                py5.rect(0, 0, 80, 80)
                py5.rect_mode(py5.CORNER)
        if self.stopTurningtrigger:
            move = self.faceToTurn
            if self.direction == -1: move += "'"
            if self.direction ==  2: move += "2"
            self.mul(genname(move))
            self.stopTurningtrigger = False
            self.startTurningtrigger = False
            self.faceToTurn = ""  
    def turn(self, giro): # funcion para animar un giro
        if (self.startTurningtrigger): # si estaba girando de antes adelantamos el giro
            self.startTurningtrigger = False
            move = self.faceToTurn
            if self.direction == -1: move += "'"
            if self.direction ==  2: move += "2"
            self.mul(genname(move)) # añadimos el giro al estado del cubo, pues esto se hace al final de la animacion
            # al cancelar la animacion no se actualiza el estado interno del cubo asi que lo hacemos manualmente
        self.inicio = getTime() # marcamos en que tiempo empezo el giro
        self.startTurningtrigger = True # volvemos a triggerear el incio de giro
        self.stopTurningtrigger = False # desactivamos el trigger de dejar de girar
        dir = 1
        if "'" in giro:
            giro = giro.replace("'", "") # quitamos la inversion de giro para guardar solo la cara
            dir *= -1 #invertimos la direccion
        self.faceToTurn = giro
        self.direction = dir
    def solve(self, dict_reps1, dict_reps2, dict_reps3, dict_reps4): # le pasamos los diccionarios a usar y resolvemos con el metodo de thistlethwaite
        self.toSolve = buscarsolvetw(self.copy(), dict_reps1, dict_reps2, dict_reps3, dict_reps4, False)
        self.iniciosolve = getTime()
        self.index = 0
    def getsolve(self, dict_reps1, dict_reps2, dict_reps3, dict_reps4): # retornamos la solucion en formato legible
        return buscarsolvetw(self.copy(), dict_reps1, dict_reps2, dict_reps3, dict_reps4, True)
# estados de cubo Rubik333 utiles
ID_CUBO = Rubik333( # estado resuelto
    [0]*8, [0]*12,
    list(range(8)), list(range(12))
)
U = Rubik333( #Giro horario en cara U
    v=[0, 0, 0, 0, 0, 0, 0, 0],
    w=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    rho=[1, 2, 3, 0, 4, 5, 6, 7],
    sigma=[1, 2, 3, 0, 4, 5, 6, 7, 8, 9, 10, 11]
)
R = Rubik333( #Giro horario en cara R
    v=[0, 1, 2, 0, 0, 1, 2, 0],
    w=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    rho=[0, 6, 1, 3, 4, 2, 5, 7],
    sigma=[0, 7, 2, 3, 4, 5, 1, 9, 8, 6, 10, 11]
)
L = Rubik333( #Giro horario en cara L
    v=[2, 0, 0, 1, 2, 0, 0, 1],
    w=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    rho=[3, 1, 2, 4, 7, 5, 6, 0],
    sigma=[0, 1, 2, 5, 3, 11, 6, 7, 8, 9, 10, 4]
)
D = Rubik333( #Giro horario en cara D
    v=[0, 0, 0, 0, 0, 0, 0, 0],
    w=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    rho=[0, 1, 2, 3, 5, 6, 7, 4],
    sigma=[0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 8]
)
F = Rubik333( #Giro horario en cara F
    v=[0, 0, 1, 2, 1, 2, 0, 0],
    w=[0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0],
    rho=[0, 1, 5, 2, 3, 4, 6, 7],
    sigma=[0, 1, 6, 3, 4, 2, 8, 7, 5, 9, 10, 11]
)
B = Rubik333( #Giro horario en cara B
    v=[1, 2, 0, 0, 0, 0, 1, 2],
    w=[1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0],
    rho=[7, 0, 2, 3, 4, 5, 1, 6],
    sigma=[4, 1, 2, 3, 10, 5, 6, 0, 8, 9, 7, 11]
)
u = U.inverso() # denotamos por codigo los giros inversos como el mismo giro pero en minuscula
r = R.inverso()
l = L.inverso()
d = D.inverso()
f = F.inverso()
b = B.inverso()
U2 = U*U # Los giros dobles no tienen direccion asi que simplemente elevamos al cuadrado cada giro
R2 = R*R
L2 = L*L
D2 = D*D
F2 = F*F
B2 = B*B

def namegen(gen): # esta funcion le pasamos un generador del Grupo de Rubik y nos devuelve en string que giro es
    if (gen == U):
        return "U"
    if (gen == R):
        return "R"
    if (gen == F):
        return "F"
    if (gen == D):
        return "D"
    if (gen == L):
        return "L"
    if (gen == B):
        return "B"
    if (gen == U2):
        return "U2"
    if (gen == R2):
        return "R2"
    if (gen == F2):
        return "F2"
    if (gen == D2):
        return "D2"
    if (gen == L2):
        return "L2"
    if (gen == B2):
        return "B2"
    if (gen == u):
        return "U'"
    if (gen == r):
        return "R'"
    if (gen == f):
        return "F'"
    if (gen == d):
        return "D'"
    if (gen == l):
        return "L'"
    if (gen == b):
        return "B'"
    return ""
def genname(name): # esta funcion le pasamos en texto que giro es y nos devuelve el correspondiente generador del grupo de Rubik
    if (name == "U"):
        return U
    if (name == "R"):
        return R
    if (name == "F"):
        return F
    if (name == "D"):
        return D
    if (name == "L"):
        return L
    if (name == "B"):
        return B
    if (name == "U2"):
        return U2
    if (name == "R2"):
        return R2
    if (name == "F2"):
        return F2
    if (name == "D2"):
        return D2
    if (name == "L2"):
        return L2
    if (name == "B2"):
        return B2
    if (name == "U'"):
        return u
    if (name == "R'"):
        return r
    if (name == "F'"):
        return f
    if (name == "D'"):
        return d
    if (name == "L'"):
        return l
    if (name == "B'"):
        return b
    return ID_CUBO
def generar_H(): # Grupo auxiliar para poder detectar las firmas de los representantes de G2/G3
    gens = [tuple(g.rho) for g in (U2, D2, F2, B2, L2, R2)]
    H = {tuple(range(8))}
    frontera = [tuple(range(8))]
    while frontera:
        nueva = []
        for h in frontera:
            for g in gens:
                n = tuple(g[h[i]] for i in range(8))
                if n not in H:
                    H.add(n)
                    nueva.append(n)
        frontera = nueva
    return list(H)
H = generar_H() # generamos el grupo
# Hasta aqui llegan las definiciones utiles para Rubik333
# ahora debemos crear la clase que nos permite dibujar cada color del cubo

# Las siguientes definiciones nos permiten hacer restricciones a que colores son validos
# ejemplo: no se si tenemos dos aristas que por un lado tienen color blanco
# y a una de ellas le ponemos color rojo por el otro lado, al llegar a la otra arista el color rojo no será opcion
# pues ya existe la pieza
# queremos poner este tipo de restricciones para evitar cubos imposibles

#conjuntos de piezas en indices
cornersid = [
    {0, 8, 34},
    {2, 26, 32},
    {4, 18, 24},
    {6, 10, 16},
    {12, 22, 40},
    {20, 30, 42},
    {28, 38, 44},
    {14, 36, 46}
]
edgesid = [
    {1, 33},
    {3, 25},
    {5, 17},
    {7, 9},
    {15, 35},
    {11, 23},
    {19, 31},
    {27, 39},
    {21, 41},
    {29, 43},
    {37, 45},
    {13, 47}
]
def indextopiece(index):
    for x in range(len(edgesid)):
        if index in edgesid[x]:
            piece = edges[x]
            return piece
    for x in range(len(cornersid)):
        if index in cornersid[x]:
            piece = corners[x]
            return piece
    return [[], [], []]
def indextocolor(index):
    if index in {0, 1, 2, 3, 4, 5, 6, 7}:
        return "U"
    if index in {8, 9, 10, 11, 12, 13, 14, 15}:
        return "L"
    if index in {16, 17, 18, 19, 20, 21, 22, 23}:
        return "F"
    if index in {24, 25, 26, 27, 28, 29, 30, 31}:
        return "R"
    if index in {32, 33, 34, 35, 36, 37, 38, 39}:
        return "B"
    if index in {40, 41, 42, 43, 44, 45, 46, 47}:
        return "D"
OPPOSITE = {"U": "D", "D": "U", "L": "R", "R": "L", "F": "B", "B": "F"} # diccionario que nos dice que caras son opuestas
ALL_COLORS = frozenset({"U", "L", "F", "R", "B", "D"}) # Conjunto de caras pero inmutable
# 12 aristas validas
ALL_EDGE_TYPES = frozenset(
    frozenset((a, b))
    for a in ALL_COLORS for b in ALL_COLORS
    if a < b and OPPOSITE[a] != b
)

# 8 esquinas validas
ALL_CORNER_TYPES = frozenset(
    frozenset((a, b, c))
    for a in ALL_COLORS for b in ALL_COLORS for c in ALL_COLORS
    if a < b < c
    and OPPOSITE[a] != b and OPPOSITE[a] != c and OPPOSITE[b] != c
)


# 12 aristas: 2 colores no opuestos
EDGE_TYPES = frozenset({
    frozenset(("U","R")), frozenset(("U","F")), frozenset(("U","L")), frozenset(("U","B")),
    frozenset(("D","R")), frozenset(("D","F")), frozenset(("D","L")), frozenset(("D","B")),
    frozenset(("F","R")), frozenset(("F","L")), frozenset(("B","R")), frozenset(("B","L")),
})

# 8 esquinas: 3 colores mutuamente no opuestos
CORNER_TYPES = frozenset({
    frozenset(("U","R","F")), frozenset(("U","F","L")),
    frozenset(("U","L","B")), frozenset(("U","B","R")),
    frozenset(("D","F","R")), frozenset(("D","L","F")),
    frozenset(("D","B","L")), frozenset(("D","R","B")),
})
def chekdecompatibilidad(pieces, free_types):
    if len(pieces) > len(free_types):
        return False
    match = {}   # tipo -> índice de pieza
    def filtrar(i, visited):
        for t in pieces[i]: # revisamos cada opcion compatible con el elemento i
            if t in visited or t not in free_types: # filtramos opciones no validas
                continue
            visited.add(t)
            if t not in match or filtrar(match[t], visited):
                match[t] = i
                return True
        return False
    return all(filtrar(i, set()) for i in range(len(pieces)))

def perm_parity(perm): # calculamos el signo de una permutacion descomponiendola en ciclos disjuntos, O(n)
    n = len(perm)
    visited = [False] * n
    parity = 0
    for i in range(n):
        if not visited[i]:
            j, length = i, 0
            while not visited[j]: # seguimos los saltos hasta volver al inicio
                visited[j] = True
                j = perm[j]
                length += 1
            parity ^= (length - 1) & 1 # length-1 es el numero de transposiciones para descomponer el ciclo actual, con & 1 filtramos la paridad con operaciones de bit que son mas rapidas, usando ^= cambiamos el estado de parity solo si el ciclo tiene signo impar
    return parity

class Build333: # esta clase corresponde a un cubo en proceso de construirse introduciendo los colores de cada pegatina del cubo
    def __init__(self):
        self.array = [-1]*48 # Un array de estado por pegatinas que incializa "vacio" con -1 en cada entrada 
        self.index = 0 # el indice en el que vamos
    def piece_info(self, index): # nos dice si el indice (indice dentro de range(48)) corresponde a una arista o esquina
        for x in edgesid:
            if index in x:
                return x, True
        for x in cornersid:
            if index in x:
                return x, False
        return None, None
    # chequeamos si el estado es posible de completar, en caso de que no sea posible, 
    # no dejaremos colocar el color indicado por el usuario
    def completable(self, pool, valid_types): 
        # used guarda las combinaciones ya completadas
        # incomplete sera una lista de conjuntos con las opciones validas para cada grupo incompleto
        used, incomplete = set(), []
        for p in pool:
            # Obtenemos los colores actuales de cada posición del grupo 'p' (-1 indica celda vacía)
            colors = [self.array[s] for s in p]

            # Caso 1: El grupo aún tiene celdas sin asignar (-1)
            if -1 in colors:
                # Guardamos los colores ya fijos en este grupo como conjunto inmutable
                fixed = frozenset(c for c in colors if c != -1)
                # Filtramos qué combinaciones válidas (valid_types) contienen a los colores ya fijos
                allowed = frozenset(t for t in valid_types if fixed <= t)

                # Si no existe ninguna combinación válida posible para este grupo, el estado falla
                if not allowed:
                    return False
                incomplete.append(allowed)
            else: # Caso 2: El grupo ya tiene todas sus celdas asignadas
                t = frozenset(colors) # Convertimos la combinación a frozenset para poder buscarla en sets/diccionarios
                if t not in valid_types or t in used:
                    return False
                # Registramos esta combinación como ocupada
                used.add(t)
        #Verificamos si existe un emparejamiento válido entre los grupos incompletos
        # y los tipos válidos que aún quedan disponibles (valid_types - used)
        return chekdecompatibilidad(incomplete, valid_types - used)

    def globalmente_completable(self):
        return (self.completable(edgesid, EDGE_TYPES) and self.completable(cornersid, CORNER_TYPES))
    def get_available_colors(self, index): # comprobamos que colores estan disponibles para index
        piece, is_edge = self.piece_info(index)
        if piece is None:
            return set()
        other = [self.array[s] for s in piece
                 if s != index and self.array[s] != -1]

        # filtro local rápido (color no repetido y no opuesto en la misma pieza)
        quick = {c for c in ALL_COLORS if c not in other and all(OPPOSITE[c] != oc for oc in other)}
        # filtro global: solo aceptamos si tras ponerlo el cubo sigue completable
        result = set()
        for c in quick:
            self.array[index] = c
            if self.globalmente_completable():
                result.add(c)
            self.array[index] = -1
        return result
    def is_stuck(self):
        return any(
            self.array[i] == -1 and not self.get_available_colors(i)
            for i in range(48)
        )
    def set_sticker(self, color): # colocamos el sticker color en self.index
        if color not in self.get_available_colors(self.index):
            return False # si el color no esta permitido no vamos a colocarlo en el estado del cubo
        self.array[self.index] = color # colocamos el sticker en array
        if self.index < 47: # esto para no pasarnos de 47
            self.index += 1
        return True
    def delete_sticker(self):
        if self.index > 0: # impedimos borrar el sticker -1
            self.array[self.index-1] = -1 # apagamos el sticker en la posicion self.index
            self.index -= 1 # restamos uno al index

    def build(self):
        if -1 in self.array: return False # Todas las esquinas deben estar coloreadas para construir el cubo
        def ordered_indices(sticker_set, color_tuple): # reordena los indices de una pieza para alinearlos con la secuencia de indices de referencia
            result, remaining = [], list(sticker_set)
            for color in color_tuple:
                for s in remaining:
                    if indextocolor(s) == color:
                        result.append(s)
                        remaining.remove(s)
                        break
                else: return False # No se encontro el color en el conjunto de stickers")
            return result
        # iniciamos un estado armado
        v     = [0] * 8
        w     = [0] * 12
        rho   = [-1] * 8
        sigma = [-1] * 12

        # ----- Esquinas -----
        for z in range(8):
            sset        = cornersid[z]
            colors_here = {self.array[s] for s in sset}
            x_found = next(
                (k for k in range(8) if set(corners[k]) == colors_here), None)
            if x_found is None: return False # Los colores de esquina son invalidos

            ordered  = ordered_indices(sset, corners[z])
            observed = tuple(self.array[s] for s in ordered)
            y_found = next(
                (y for y in range(3)
                 if tuple(corners[x_found][(y + i) % 3] for i in range(3))
                    == observed), None)
            if y_found is None: return False # No se pudo determinar la orientación de la esquina

            rho[x_found] = z
            v[z] = y_found

        # ----- Aristas -----
        for z in range(12):
            sset        = edgesid[z]
            colors_here = {self.array[s] for s in sset}

            x_found = next(
                (k for k in range(12) if set(edges[k]) == colors_here), None)
            if x_found is None: return False # los colores de arista son invalidos

            ordered  = ordered_indices(sset, edges[z])
            observed = tuple(self.array[s] for s in ordered)

            y_found = next(
                (y for y in range(2)
                 if tuple(edges[x_found][(y + i) % 2] for i in range(2))
                    == observed), None)
            if y_found is None: return False # No se pudo determinar orientación de la arista

            sigma[x_found] = z
            w[z] = y_found

        # ----- Validación de estado legal -----
        if sorted(rho) != list(range(8)): return False # Permutación de esquinas inválida
        if sorted(sigma) != list(range(12)): return False # Permutación de aristas inválida
        if sum(v) % 3 != 0: return False # Suma de orientaciones de esquina invalida
        if sum(w) % 2 != 0: return False # Suma de orientaciones de arista invalida
        if perm_parity(rho) ^ perm_parity(sigma) != 0: return False # Paridades de permutación distintas
        return Rubik333(v, w, rho, sigma) # creamos el Rubik333 que calculamos
   
    def draw_centers(self):
        for z in range(6):
            a = setcoordcenters[z][1][0]
            b = setcoordcenters[z][1][1]
            c = setcoordcenters[z][1][2]
            py5.translate(a, b, c)
            py5.rotate_x(setcoordcenters[z][0][0])
            py5.rotate_y(setcoordcenters[z][0][1])
            py5.fill(palette[faces[z]])
            py5.rect_mode(py5.CENTER)
            py5.rect(0, 0, 80, 80)
            py5.rect_mode(py5.CORNER)
            py5.rotate_y(-setcoordcenters[z][0][1])
            py5.rotate_x(-setcoordcenters[z][0][0])
            py5.translate(-a, -b, -c)
    def draw_stickers(self):
        for z in range(48):
            if (self.array[z] == -1):
                py5.fill(50, 50, 50)
            else:
                py5.fill(palette[self.array[z]])
            a = setcoordstickers[z][1][0]
            b = setcoordstickers[z][1][1]
            c = setcoordstickers[z][1][2]
            py5.translate(a, b, c)
            py5.rotate_x(setcoordstickers[z][0][0])
            py5.rotate_y(setcoordstickers[z][0][1])
            py5.rect_mode(py5.CENTER)
            py5.rect(0, 0, 80, 80)
            py5.rect_mode(py5.CORNER)
            py5.rotate_y(-setcoordstickers[z][0][1])
            py5.rotate_x(-setcoordstickers[z][0][0])
            py5.translate(-a, -b, -c)
