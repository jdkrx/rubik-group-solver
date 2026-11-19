import py5 #3d
import json
import queue
from math import pi as PI
from time import perf_counter as getTime
from representantes import get_reps1, get_reps2, get_reps3, get_reps4
# region


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

#archivoreps1 = False
#archivoreps2 = False
#archivoreps3 = False
#archivoreps4 = False
def configurararchivos(cola):
    #global archivoreps1, archivoreps2, archivoreps3, archivoreps4
    archivoreps1, archivoreps2, archivoreps3, archivoreps4 = (False, False, False, False)
    print("Haciendo cosas")
    try:
        with open('representantes/G0-G1.json', 'r', encoding='utf-8') as file:
            repscamino1 = json.load(file)
        archivoreps1 = True
    except FileNotFoundError:
        pass
    try:
        with open('representantes/G1-G2.json', 'r', encoding='utf-8') as file:
            repscamino2 = json.load(file)
        archivoreps2 = True
    except FileNotFoundError:
        pass
    try:
        with open('representantes/G2-G3.json', 'r', encoding='utf-8') as file:
            repscamino3 = json.load(file)
        archivoreps3 = True
    except FileNotFoundError:
        pass
    try:
        with open('representantes/G3-G4.json', 'r', encoding='utf-8') as file:
            repscamino4 = json.load(file)
        archivoreps4 = True
    except FileNotFoundError:
        pass
    #repscamino1, repscamino2, repscamino3, repscamino4 = ("", "", "", "")
    if not archivoreps1:
        get_reps1()
        with open('representantes/G0-G1.json', 'r', encoding='utf-8') as file:
            repscamino1 = json.load(file)
        archivoreps1 = True
    if not archivoreps2:
        get_reps2()
        with open('representantes/G1-G2.json', 'r', encoding='utf-8') as file:
            repscamino2 = json.load(file)
        archivoreps2 = True
    if not archivoreps3:
        get_reps3()
        with open('representantes/G2-G3.json', 'r', encoding='utf-8') as file:
            repscamino3 = json.load(file)
        archivoreps3 = True
    if not archivoreps4:
        get_reps4()
        with open('representantes/G3-G4.json', 'r', encoding='utf-8') as file:
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
    if True: print(f"Tiempo configurando los representantes: {finalconfig - inicioconfig} segundos")
    cola.put((dict_reps1, dict_reps2, dict_reps3, dict_reps4))

def buscarsolvetw(scramble, dict_reps1, dict_reps2, dict_reps3, dict_reps4, spacing):

    alg1 = dict_reps1[obtener_firma_G0_G1(scramble)]
    str = ""
    algo1 = []
    for i in alg1[::-1]:
        gen = namegen(genname(i).inverso()) # type: ignore
        str += gen + " "# type: ignore
        algo1.append(gen)
    g1 = ID_CUBO
    for i in alg1:
        g1 = g1*genname(i)
    if (scramble*g1.inverso() == ID_CUBO):
        algfinal = algo1
        return (algfinal)

    if spacing: algo1 += [" (EO)\n"]
    alg2 = dict_reps2[obtener_firma_G1_G2(scramble*g1.inverso())]
    algo2 = []
    str = ""
    for i in alg2[::-1]:
        gen = namegen(genname(i).inverso()) # type: ignore
        str += gen + " " # type: ignore
        algo2.append(gen)
    g2 = ID_CUBO
    for i in alg2:
        g2 = g2*genname(i)

    if (scramble*g1.inverso()*g2.inverso() == ID_CUBO):
        algfinal = algo1 + algo2
        return (algfinal)
    if spacing: algo2 += [" (DR)\n"]
    alg3 = dict_reps3[obtener_firma_G2_G3(scramble*g1.inverso()*g2.inverso())]
    str = ""
    algo3 = []
    for i in alg3[::-1]:
        gen = namegen(genname(i).inverso()) # type: ignore
        str += gen + " " # type: ignore
        algo3.append(gen)
    g3 = ID_CUBO
    for i in alg3:
        g3 = g3*genname(i)

    if (scramble*g1.inverso()*g2.inverso()*g3.inverso() == ID_CUBO):
        algfinal = algo1 + algo2 + algo3
        return (algfinal)
    if spacing: algo3 += [" (HTR)\n"]
    alg4 = dict_reps4[obtener_firma_G3_G4(scramble*g1.inverso()*g2.inverso()*g3.inverso())]
    str = ""
    algo4 = []
    for i in alg4[::-1]:
        gen = namegen(genname(i).inverso()) # type: ignore
        str += gen + " "                    # type: ignore
        algo4.append(gen)
    algfinal = algo1 + algo2 + algo3 + algo4
    return (algfinal)
# region
setcoordedges = [
    # un array con las instrucciones para llegar a cada arista del cubo
    # [ (rotacionx, rotaciony), translate(x, y, z) ] -> id de pieza en el espacio de aristas
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
setcoordcorners = [
    # un array con las instrucciones para llegar a cada arista del cubo
    # [ (rotacionx, rotaciony), translate(x, y, z) ] -> id de pieza en el espacio de aristas
    [(0, PI), (-80, -80, -80)],   # UBL
    [(0, PI/2), (80, -80, -80)],  # UBR
    [(0, 0), (80, -80, 80)],      # UFR
    [(0, -PI/2), (-80, -80, 80)], # UFL
    [(PI, PI), (-80, 80, 80)],    # DFL
    [(PI, PI/2), (80, 80, 80)],   # DFR
    [(PI, 0), (80, 80, -80)],     # DBR
    [(PI, -PI/2), (-80, 80, -80)] # DBL
]
setcoordcenters = [
    [(-PI/2, 0), (0, -120, 0)],
    [(0, PI/2), (-120, 0, 0)],
    [(0, 0), (0, 0, 120)],
    [(0, PI/2), (120, 0, 0)],
    [(0, 0), (0, 0, -120)],
    [(PI/2, 0), (0, 120, 0)],
]

faces = ["U", "L", "F", "R", "B", "D"]

palette = {
    "U": py5.color(255, 255, 255),
    "L": py5.color(255, 128, 0),
    "F": py5.color(0,255,0),
    "R": py5.color(255, 0, 0),
    "B": py5.color(0, 0, 255),
    "D": py5.color(255, 255, 0)
}

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

layers = {
    "U": U_LAYER,
    "D": D_LAYER,
    "R": R_LAYER,
    "L": L_LAYER,
    "F": F_LAYER,
    "B": B_LAYER
}
# endregion
# una pieza debe ser 80x80x80
def drawEdge(edge, orientation, t):
    if orientation == 1: edge = (edge[1], edge[0])

    py5.stroke(0)
    py5.rect_mode(py5.CENTER)


    py5.translate(0, 0, 40*t)
    py5.fill(palette[edge[1]]) # type: ignore
    py5.rect(0, 0, 80, 80)
    py5.translate(0, 0, -40*t)
    py5.translate(0, -40*t, 0)
    py5.rotate_x(PI/2)

    py5.fill(palette[edge[0]]) # type: ignore
    py5.rect(0, 0, 80, 80)

    py5.rotate_x(-PI/2)
    py5.translate(0, 40*t, 0)
    py5.rect_mode(py5.CORNER)
def drawCorner(corner, orientation, t):
    if orientation == 1:  corner = (corner[1], corner[2], corner[0])
    if orientation == 2:  corner = (corner[2], corner[0], corner[1])

    py5.stroke(0)
    py5.rect_mode(py5.CENTER)

    py5.translate(0, 0, 40*t)
    py5.fill(palette[corner[1]])
    py5.rect(0, 0, 80, 80)
    py5.translate(0, 0, -40*t)

    py5.translate(0, -40*t, 0)
    py5.rotate_x(PI/2)
    py5.fill(palette[corner[0]])
    py5.rect(0, 0, 80, 80)
    py5.rotate_x(-PI/2)
    py5.translate(0, 40*t, 0)

    py5.translate(40*t, 0, 0)
    py5.rotate_y(PI/2)
    py5.fill(palette[corner[2]])
    py5.rect(0, 0, 80, 80)
    py5.rotate_y(-PI/2)
    py5.translate(-40*t, 0, 0)

    py5.rect_mode(py5.CORNER)
setcoordstickers = [
    # un array con las instrucciones para llegar a cada sticker del cubo
    # [ (rotacionx, rotaciony), translate(x, y, z) ] -> id del sticker en el espacio de pegatinas
    [(PI/2, 0), (-80, -120, -80)],               #0
    [(PI/2, 0), (0, -120, -80)],                 #1
    [(PI/2, 0), (80, -120, -80)],                #2
    [(PI/2, 0), (80, -120, 0)],                  #3
    [(PI/2, 0), (80, -120, 80)],                 #4
    [(PI/2, 0), (0, -120, 80)],                  #5
    [(PI/2, 0), (-80, -120, 80)],                #6
    [(PI/2, 0), (-80, -120, 0)],                 #7     #U
    [(0, PI/2), (-120, -80,-80)],                #8
    [(0, PI/2), (-120, -80, 0)],                 #9
    [(0, PI/2), (-120, -80, 80)],                #10
    [(0, PI/2), (-120, 0, 80)],                  #11
    [(0, PI/2), (-120, 80, 80)],                 #12
    [(0, PI/2), (-120, 80, 0)],                  #13
    [(0, PI/2), (-120, 80, -80)],                #14
    [(0, PI/2), (-120, 0, -80)],                 #15   #L
    [(0, 0), (-80, -80, 120)],                   #16
    [(0, 0), (0, -80, 120)],                     #17
    [(0, 0), (80, -80, 120)],                    #18
    [(0, 0), (80, 0, 120)],                      #19
    [(0, 0), (80, 80, 120)],                     #20
    [(0, 0), (0, 80, 120)],                      #21
    [(0, 0), (-80, 80, 120)],                    #22
    [(0, 0), (-80, 0, 120)],                     #23   #F
    [(0, PI/2), (120, -80, 80)],                 #24
    [(0, PI/2), (120, -80, 0)],                  #25
    [(0, PI/2), (120, -80, -80)],                #26
    [(0, PI/2), (120, 0, -80)],                  #27
    [(0, PI/2), (120, 80, -80)],                 #28
    [(0, PI/2), (120, 80, 0)],                   #29
    [(0, PI/2), (120, 80, 80)],                  #30
    [(0, PI/2), (120, 0, 80)],                   #31  #R
    [(0, 0), (80, -80, -120)],                   #32
    [(0, 0), (0, -80, -120)],                    #33
    [(0, 0), (-80, -80, -120)],                  #34
    [(0, 0), (-80, 0, -120)],                    #35
    [(0, 0), (-80, 80, -120)],                   #36
    [(0, 0), (0, 80, -120)],                     #37
    [(0, 0), (80, 80, -120)],                    #38
    [(0, 0), (80, 0, -120)],                     #39  #B
    [(PI/2, 0), (-80, 120, 80)],                 #40
    [(PI/2, 0), (0, 120, 80)],                   #41
    [(PI/2, 0), (80, 120, 80)],                  #42
    [(PI/2, 0), (80, 120, 0)],                   #43
    [(PI/2, 0), (80, 120, -80)],                 #44
    [(PI/2, 0), (0, 120, -80)],                  #45
    [(PI/2, 0), (-80, 120, -80)],                #46
    [(PI/2, 0), (-80, 120, 0)]                   #47  #D
 ]

def drawSticker(index, color):
    py5.stroke(0)
    py5.rect_mode(py5.CENTER)
    a = setcoordstickers[index][1][0]
    b = setcoordstickers[index][1][1]
    c = setcoordstickers[index][1][2]
    py5.translate(a, b, c)
    py5.fill(palette[color])
    py5.rotate_x(setcoordstickers[index][0][0])
    py5.rotate_y(setcoordstickers[index][0][1])
    py5.rect(0, 0, 80, 80)
    py5.rotate_y(-setcoordstickers[index][0][1])
    py5.rotate_x(-setcoordstickers[index][0][0])
    py5.translate(-a, -b, -c)

# endregion
class Rubik333:
    def __init__(self, v, w, rho, sigma):
        self.v = v[:]
        self.w = w[:]
        self.rho = rho[:]
        self.sigma = sigma[:]
        self.inicio = 0
        self.startTurningtrigger = False
        self.stopTurningtrigger = False
        self.faceToTurn = ""
        self.direction = 1
        self.toSolve = []
        self.turning = False
        self.iniciosolve = 0
        self.index = 0

    def __repr__(self):
        return f"v:{self.v}\nw:{self.w}\nrho:{self.rho}\nsigma:{self.sigma}"
    def __mul__(self, otro):
        rho_inv = [0]*8
        sigma_inv = [0]*12

        for i in range(8): rho_inv[otro.rho[i]] = i
        for i in range(12): sigma_inv[otro.sigma[i]] = i

        nuevo_v = [(otro.v[i] + self.v[rho_inv[i]]) % 3 for i in range(8)]
        nuevo_w = [(otro.w[i] + self.w[sigma_inv[i]]) % 2 for i in range(12)]

        nuevo_rho = [otro.rho[self.rho[i]] for i in range(8)]
        nuevo_sigma = [otro.sigma[self.sigma[i]] for i in range(12)]
        return Rubik333(nuevo_v, nuevo_w, nuevo_rho, nuevo_sigma)
    def mul(self, otro):
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
    def inverso(self):
        inv_rho = [0] * 8
        for i in range(8): inv_rho[self.rho[i]] = i
        inv_sigma = [0] * 12
        for i in range(12): inv_sigma[self.sigma[i]] = i
        inv_v = [(-self.v[self.rho[i]]) % 3 for i in range(8)]
        inv_w = [(-self.w[self.sigma[i]]) % 2 for i in range(12)]
        return Rubik333(inv_v, inv_w, inv_rho, inv_sigma)
    def __eq__(self, otro):
        if not isinstance(otro, Rubik333):
            return False
        return self.v == otro.v and self.w == otro.w and self.rho == otro.rho and self.sigma == otro.sigma
    def display(self, t):
        if self.index != len(self.toSolve) and not self.turning:
            if(self.toSolve[self.index] == "R" or self.toSolve[self.index] == "R2"):
                self.turnR()
            if(self.toSolve[self.index] == "R'"):
                self.turnr()
            if(self.toSolve[self.index] == "U" or self.toSolve[self.index] == "U2"):
                self.turnU()
            if(self.toSolve[self.index] == "U'"):
                self.turnu()
            if(self.toSolve[self.index] == "L" or self.toSolve[self.index] == "L2"):
                self.turnL()
            if(self.toSolve[self.index] == "L'"):
                self.turnl()
            if(self.toSolve[self.index] == "D" or self.toSolve[self.index] == "D2"):
                self.turnD()
            if(self.toSolve[self.index] == "D'"):
                self.turnd()
            if(self.toSolve[self.index] == "B" or self.toSolve[self.index] == "B2"):
                self.turnB()
            if(self.toSolve[self.index] == "B'"):
                self.turnb()
            if(self.toSolve[self.index] == "F" or self.toSolve[self.index] == "F2"):
                self.turnF()
            if(self.toSolve[self.index] == "F'"):
                self.turnf()
            self.turning = True
        if (self.index < len(self.toSolve) and (getTime() - self.iniciosolve) > 0.7):
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

        for z in range(12): # DRAW EDGES
            x = self.sigma[z]
            sigmainversa = [0]*12
            for i in range(12): sigmainversa[self.sigma[i]] = i
            x = sigmainversa[z]
            y = self.w[z]
            a = setcoordedges[z][1][0]
            b = setcoordedges[z][1][1]
            c = setcoordedges[z][1][2]
            if self.faceToTurn != "" and self.startTurningtrigger:
                if (edges[z] in layers[self.faceToTurn]):
                    if (getTime() - self.inicio >= 0.2):
                        self.stopTurningtrigger = True
                    if (self.faceToTurn == "R"): py5.rotate_x(self.direction*(getTime() - self.inicio)*PI/(2*0.2))
                    if (self.faceToTurn == "L"): py5.rotate_x(-self.direction*(getTime() - self.inicio)*PI/(2*0.2))
                    if (self.faceToTurn == "U"): py5.rotate_y(-self.direction*(getTime() - self.inicio)*PI/(2*0.2))
                    if (self.faceToTurn == "D"): py5.rotate_y(self.direction*(getTime() - self.inicio)*PI/(2*0.2))
                    if (self.faceToTurn == "F"): py5.rotate_z(self.direction*(getTime() - self.inicio)*PI/(2*0.2))
                    if (self.faceToTurn == "B"): py5.rotate_z(-self.direction*(getTime() - self.inicio)*PI/(2*0.2))
                    pass
            py5.translate(a*t, b*t, c*t)
            py5.rotate_x(setcoordedges[z][0][0])
            py5.rotate_y(setcoordedges[z][0][1])
            drawEdge(edges[x], y, t)
            py5.rotate_y(-setcoordedges[z][0][1])
            py5.rotate_x(-setcoordedges[z][0][0])
            py5.translate(-a*t, -b*t, -c*t)
            if self.faceToTurn != "" and self.startTurningtrigger:
                if (edges[z] in layers[self.faceToTurn]):
                    if (getTime() - self.inicio >= 0.2):
                        self.stopTurningtrigger = True
                    if (self.faceToTurn == "R"): py5.rotate_x(-self.direction*(getTime() - self.inicio)*PI/(2*0.2))
                    if (self.faceToTurn == "L"): py5.rotate_x(self.direction*(getTime() - self.inicio)*PI/(2*0.2))
                    if (self.faceToTurn == "U"): py5.rotate_y(self.direction*(getTime() - self.inicio)*PI/(2*0.2))
                    if (self.faceToTurn == "D"): py5.rotate_y(-self.direction*(getTime() - self.inicio)*PI/(2*0.2))
                    if (self.faceToTurn == "F"): py5.rotate_z(-self.direction*(getTime() - self.inicio)*PI/(2*0.2))
                    if (self.faceToTurn == "B"): py5.rotate_z(self.direction*(getTime() - self.inicio)*PI/(2*0.2))
                    pass
        for z in range(8): # DRAW CORNERS
            x = self.rho[z]
            rhoinversa = [0]*8
            for i in range(8): rhoinversa[self.rho[i]] = i
            x = rhoinversa[z]
            y = self.v[z]
            a = setcoordcorners[z][1][0]
            b = setcoordcorners[z][1][1]
            c = setcoordcorners[z][1][2]
            if self.faceToTurn != "" and self.startTurningtrigger:
                if (corners[z] in layers[self.faceToTurn]):
                    if (getTime() - self.inicio >= 0.2):
                        self.stopTurningtrigger = True
                    if (self.faceToTurn == "R"): py5.rotate_x(self.direction*(getTime() - self.inicio)*PI/(2*0.2))
                    if (self.faceToTurn == "L"): py5.rotate_x(-self.direction*(getTime() - self.inicio)*PI/(2*0.2))
                    if (self.faceToTurn == "U"): py5.rotate_y(-self.direction*(getTime() - self.inicio)*PI/(2*0.2))
                    if (self.faceToTurn == "D"): py5.rotate_y(self.direction*(getTime() - self.inicio)*PI/(2*0.2))
                    if (self.faceToTurn == "F"): py5.rotate_z(self.direction*(getTime() - self.inicio)*PI/(2*0.2))
                    if (self.faceToTurn == "B"): py5.rotate_z(-self.direction*(getTime() - self.inicio)*PI/(2*0.2))
                    pass
            py5.translate(a*t, b*t, c*t)
            py5.rotate_x(setcoordcorners[z][0][0])
            py5.rotate_y(setcoordcorners[z][0][1])
            drawCorner(corners[x], y, t)
            py5.rotate_y(-setcoordcorners[z][0][1])
            py5.rotate_x(-setcoordcorners[z][0][0])
            py5.translate(-a*t, -b*t, -c*t)
            if self.faceToTurn != "" and self.startTurningtrigger:
                if (corners[z] in layers[self.faceToTurn]):
                    if (getTime() - self.inicio >= 0.2):
                        self.stopTurningtrigger = True
                    if (self.faceToTurn == "R"): py5.rotate_x(-self.direction*(getTime() - self.inicio)*PI/(2*0.2))
                    if (self.faceToTurn == "L"): py5.rotate_x(self.direction*(getTime() - self.inicio)*PI/(2*0.2))
                    if (self.faceToTurn == "U"): py5.rotate_y(self.direction*(getTime() - self.inicio)*PI/(2*0.2))
                    if (self.faceToTurn == "D"): py5.rotate_y(-self.direction*(getTime() - self.inicio)*PI/(2*0.2))
                    if (self.faceToTurn == "F"): py5.rotate_z(-self.direction*(getTime() - self.inicio)*PI/(2*0.2))
                    if (self.faceToTurn == "B"): py5.rotate_z(self.direction*(getTime() - self.inicio)*PI/(2*0.2))
                    pass
        for z in range(6): # DRAW CENTERS
            a = setcoordcenters[z][1][0]
            b = setcoordcenters[z][1][1]
            c = setcoordcenters[z][1][2]
            if self.faceToTurn != "" and self.startTurningtrigger:
                if (faces[z] == self.faceToTurn):
                    if (getTime() - self.inicio >= 0.2):
                        self.stopTurningtrigger = True
                    if (self.faceToTurn == "R"): py5.rotate_x(self.direction*(getTime() - self.inicio)*PI/(2*0.2))
                    if (self.faceToTurn == "L"): py5.rotate_x(-self.direction*(getTime() - self.inicio)*PI/(2*0.2))
                    if (self.faceToTurn == "U"): py5.rotate_y(-self.direction*(getTime() - self.inicio)*PI/(2*0.2))
                    if (self.faceToTurn == "D"): py5.rotate_y(self.direction*(getTime() - self.inicio)*PI/(2*0.2))
                    if (self.faceToTurn == "F"): py5.rotate_z(self.direction*(getTime() - self.inicio)*PI/(2*0.2))
                    if (self.faceToTurn == "B"): py5.rotate_z(-self.direction*(getTime() - self.inicio)*PI/(2*0.2))
                    pass
            py5.translate(a*t, b*t, c*t)
            py5.rotate_x(setcoordcenters[z][0][0])
            py5.rotate_y(setcoordcenters[z][0][1])
            py5.fill(palette[faces[z]])
            py5.rect_mode(py5.CENTER)
            py5.rect(0, 0, 80, 80)
            py5.rect_mode(py5.CORNER)
            py5.rotate_y(-setcoordcenters[z][0][1])
            py5.rotate_x(-setcoordcenters[z][0][0])
            py5.translate(-a*t, -b*t, -c*t)
            if self.faceToTurn != "" and self.startTurningtrigger:
                if (faces[z] == self.faceToTurn):
                    if (getTime() - self.inicio >= 0.2):
                        self.stopTurningtrigger = True
                    if (self.faceToTurn == "R"): py5.rotate_x(-self.direction*(getTime() - self.inicio)*PI/(2*0.2))
                    if (self.faceToTurn == "L"): py5.rotate_x(self.direction*(getTime() - self.inicio)*PI/(2*0.2))
                    if (self.faceToTurn == "U"): py5.rotate_y(self.direction*(getTime() - self.inicio)*PI/(2*0.2))
                    if (self.faceToTurn == "D"): py5.rotate_y(-self.direction*(getTime() - self.inicio)*PI/(2*0.2))
                    if (self.faceToTurn == "F"): py5.rotate_z(-self.direction*(getTime() - self.inicio)*PI/(2*0.2))
                    if (self.faceToTurn == "B"): py5.rotate_z(self.direction*(getTime() - self.inicio)*PI/(2*0.2))
                    pass
        if self.stopTurningtrigger:
            move = self.faceToTurn
            if self.direction == -1: move += "'"
            if self.direction ==  2: move += "2"
            self.mul(genname(move))
            self.stopTurningtrigger = False
            self.startTurningtrigger = False
            self.faceToTurn = ""
    def copy(self):
        return Rubik333(self.v, self.w, self.rho, self.sigma)
    def turnR(self):
        if (self.startTurningtrigger):
            self.startTurningtrigger = False
            move = self.faceToTurn
            if self.direction == -1: move += "'"
            if self.direction ==  2: move += "2"
            self.mul(genname(move))
        self.inicio = getTime()
        self.startTurningtrigger = True
        self.stopTurningtrigger = False
        self.faceToTurn = "R"
        self.direction = 1
        pass
    def turnr(self):
        if (self.startTurningtrigger):
            self.startTurningtrigger = False
            move = self.faceToTurn
            if self.direction == -1: move += "'"
            if self.direction ==  2: move += "2"
            self.mul(genname(move))
        self.inicio = getTime()
        self.startTurningtrigger = True
        self.stopTurningtrigger = False
        self.faceToTurn = "R"
        self.direction = -1
        pass
    def turnL(self):
        if (self.startTurningtrigger):
            self.startTurningtrigger = False
            move = self.faceToTurn
            if self.direction == -1: move += "'"
            if self.direction ==  2: move += "2"
            self.mul(genname(move))
        self.inicio = getTime()
        self.startTurningtrigger = True
        self.stopTurningtrigger = False
        self.faceToTurn = "L"
        self.direction = 1
        pass
    def turnl(self):
        if (self.startTurningtrigger):
            self.startTurningtrigger = False
            move = self.faceToTurn
            if self.direction == -1: move += "'"
            if self.direction ==  2: move += "2"
            self.mul(genname(move))
        self.inicio = getTime()
        self.startTurningtrigger = True
        self.stopTurningtrigger = False
        self.faceToTurn = "L"
        self.direction = -1
        pass
    def turnU(self):
        if (self.startTurningtrigger):
            self.startTurningtrigger = False
            move = self.faceToTurn
            if self.direction == -1: move += "'"
            if self.direction ==  2: move += "2"
            self.mul(genname(move))
        self.inicio = getTime()
        self.startTurningtrigger = True
        self.stopTurningtrigger = False
        self.faceToTurn = "U"
        self.direction = 1
        pass
    def turnu(self):
        if (self.startTurningtrigger):
            self.startTurningtrigger = False
            move = self.faceToTurn
            if self.direction == -1: move += "'"
            if self.direction ==  2: move += "2"
            self.mul(genname(move))
        self.inicio = getTime()
        self.startTurningtrigger = True
        self.stopTurningtrigger = False
        self.faceToTurn = "U"
        self.direction = -1
        pass
    def turnD(self):
        if (self.startTurningtrigger):
            self.startTurningtrigger = False
            move = self.faceToTurn
            if self.direction == -1: move += "'"
            if self.direction ==  2: move += "2"
            self.mul(genname(move))
        self.inicio = getTime()
        self.startTurningtrigger = True
        self.stopTurningtrigger = False
        self.faceToTurn = "D"
        self.direction = 1
        pass
    def turnd(self):
        if (self.startTurningtrigger):
            self.startTurningtrigger = False
            move = self.faceToTurn
            if self.direction == -1: move += "'"
            if self.direction ==  2: move += "2"
            self.mul(genname(move))
        self.inicio = getTime()
        self.startTurningtrigger = True
        self.stopTurningtrigger = False
        self.faceToTurn = "D"
        self.direction = -1
        pass
    def turnF(self):
        if (self.startTurningtrigger):
            self.startTurningtrigger = False
            move = self.faceToTurn
            if self.direction == -1: move += "'"
            if self.direction ==  2: move += "2"
            self.mul(genname(move))
        self.inicio = getTime()
        self.startTurningtrigger = True
        self.stopTurningtrigger = False
        self.faceToTurn = "F"
        self.direction = 1
        pass
    def turnf(self):
        if (self.startTurningtrigger):
            self.startTurningtrigger = False
            move = self.faceToTurn
            if self.direction == -1: move += "'"
            if self.direction ==  2: move += "2"
            self.mul(genname(move))
        self.inicio = getTime()
        self.startTurningtrigger = True
        self.stopTurningtrigger = False
        self.faceToTurn = "F"
        self.direction = -1
        pass
    def turnB(self):
        if (self.startTurningtrigger):
            self.startTurningtrigger = False
            move = self.faceToTurn
            if self.direction == -1: move += "'"
            if self.direction ==  2: move += "2"
            self.mul(genname(move))
        self.inicio = getTime()
        self.startTurningtrigger = True
        self.stopTurningtrigger = False
        self.faceToTurn = "B"
        self.direction = 1
        pass
    def turnb(self):
        if (self.startTurningtrigger):
            self.startTurningtrigger = False
            move = self.faceToTurn
            if self.direction == -1: move += "'"
            if self.direction ==  2: move += "2"
            self.mul(genname(move))
        self.inicio = getTime()
        self.startTurningtrigger = True
        self.stopTurningtrigger = False
        self.faceToTurn = "B"
        self.direction = -1
        pass
    def solve(self, dict_reps1, dict_reps2, dict_reps3, dict_reps4):
        self.toSolve = buscarsolvetw(self.copy(), dict_reps1, dict_reps2, dict_reps3, dict_reps4, False)
        self.iniciosolve = getTime()
        self.index = 0
    def getsolve(self, dict_reps1, dict_reps2, dict_reps3, dict_reps4):
        return buscarsolvetw(self.copy(), dict_reps1, dict_reps2, dict_reps3, dict_reps4, True)
ID_CUBO = Rubik333(
    [0]*8, [0]*12,
    list(range(8)), list(range(12))
)
U = Rubik333(
    v=[0, 0, 0, 0, 0, 0, 0, 0],
    w=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    rho=[1, 2, 3, 0, 4, 5, 6, 7],
    sigma=[1, 2, 3, 0, 4, 5, 6, 7, 8, 9, 10, 11]
)
R = Rubik333(
    v=[0, 1, 2, 0, 0, 1, 2, 0],
    w=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    rho=[0, 6, 1, 3, 4, 2, 5, 7],
    sigma=[0, 7, 2, 3, 4, 5, 1, 9, 8, 6, 10, 11]
)
L = Rubik333(
    v=[2, 0, 0, 1, 2, 0, 0, 1],
    w=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    rho=[3, 1, 2, 4, 7, 5, 6, 0],
    sigma=[0, 1, 2, 5, 3, 11, 6, 7, 8, 9, 10, 4]
)
D = Rubik333(
    v=[0, 0, 0, 0, 0, 0, 0, 0],
    w=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    rho=[0, 1, 2, 3, 5, 6, 7, 4],
    sigma=[0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 8]
)
F = Rubik333(
    v=[0, 0, 1, 2, 1, 2, 0, 0],
    w=[0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0],
    rho=[0, 1, 5, 2, 3, 4, 6, 7],
    sigma=[0, 1, 6, 3, 4, 2, 8, 7, 5, 9, 10, 11]
)
B = Rubik333(
    v=[1, 2, 0, 0, 0, 0, 1, 2],
    w=[1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0],
    rho=[7, 0, 2, 3, 4, 5, 1, 6],
    sigma=[4, 1, 2, 3, 10, 5, 6, 0, 8, 9, 7, 11]
)

u = U.inverso()
r = R.inverso()
l = L.inverso()
d = D.inverso()
f = F.inverso()
b = B.inverso()

U2 = U*U
R2 = R*R
L2 = L*L
D2 = D*D
F2 = F*F
B2 = B*B
def namegen(gen):
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

    return 0
def genname(name):
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
    return 0
def generar_H():
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
H = generar_H()


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

# Contribución externa
OPPOSITE = {"U": "D", "D": "U", "L": "R", "R": "L", "F": "B", "B": "F"}
ALL_COLORS = frozenset({"U", "L", "F", "R", "B", "D"})
# 12 aristas válidas
ALL_EDGE_TYPES = frozenset(
    frozenset((a, b))
    for a in ALL_COLORS for b in ALL_COLORS
    if a < b and OPPOSITE[a] != b
)

# 8 esquinas válidas
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
def _has_perfect_matching(pieces, free_types):
    if len(pieces) > len(free_types):
        return False
    match = {}   # tipo -> índice de pieza

    def augment(i, visited):
        for t in pieces[i]:
            if t in visited or t not in free_types:
                continue
            visited.add(t)
            if t not in match or augment(match[t], visited):
                match[t] = i
                return True
        return False

    return all(augment(i, set()) for i in range(len(pieces)))
# fin

class Build333:
    def __init__(self):
        self.array = [-1]*48
        self.state = [-1]*48
        self.index = 0
        self.edges = []
    # contribución externa
    def _piece_info(self, index):
        for x in edgesid:
            if index in x:
                return x, True
        for x in cornersid:
            if index in x:
                return x, False
        return None, None
    def _completable(self, pool, valid_types):
        used, incomplete = set(), []
        for p in pool:
            colors = [self.array[s] for s in p]
            if -1 in colors:
                fixed = frozenset(c for c in colors if c != -1)
                allowed = frozenset(t for t in valid_types if fixed <= t)
                if not allowed:
                    return False
                incomplete.append(allowed)
            else:
                t = frozenset(colors)
                if t not in valid_types or t in used:
                    return False
                used.add(t)
        return _has_perfect_matching(incomplete, valid_types - used)
    def _globally_completable(self):
        return (self._completable(edgesid, EDGE_TYPES)
                and self._completable(cornersid, CORNER_TYPES))

    def _piece_type_in_use(self, color_type, exclude_piece, pool):
        """¿Alguna pieza COMPLETAMENTE coloreada (≠ exclude_piece) tiene este tipo?"""
        for x in pool:
            if x == exclude_piece:
                continue
            colors = [self.array[s] for s in x]
            if -1 in colors:          # aún incompleta → no la contamos
                continue
            if frozenset(colors) == color_type:
                return True
        return False
    def get_available_colors(self, index):
        piece, is_edge = self._piece_info(index)
        if piece is None:
            return set()
        other = [self.array[s] for s in piece
                 if s != index and self.array[s] != -1]

        # filtro local rápido (color no repetido y no opuesto en la misma pieza)
        quick = {c for c in ALL_COLORS
                 if c not in other
                 and all(OPPOSITE[c] != oc for oc in other)}

        # filtro global: solo aceptamos si tras ponerlo el cubo sigue completable
        result = set()
        for c in quick:
            self.array[index] = c
            if self._globally_completable():
                result.add(c)
            self.array[index] = -1
        return result
    def is_stuck(self):
        return any(
            self.array[i] == -1 and not self.get_available_colors(i)
            for i in range(48)
        )
    def set_sticker(self, color):
        if color not in self.get_available_colors(self.index):
            return False

        if self.index % 2 == 1 and self.array[self.index] == -1:
            for x in edgesid:
                if self.index in x:
                    other = next(s for s in x if s != self.index)
                    if self.array[other] != -1:
                        self.edges.append(x)
                    break

        self.array[self.index] = color
        if self.index < 47:              # fix del bug `self.array != 47`
            self.index += 1
        return True
    def delete_sticker(self):
        if self.index > 0:
            self.array[self.index-1] = -1
            self.index -= 1
    def build(self):
        """Devuelve un Rubik333 con el estado de pegatinas actual."""
        if -1 in self.array:
            raise ValueError("Todas las pegatinas deben estar coloreadas")

        def ordered_indices(sticker_set, color_tuple):
            result, remaining = [], list(sticker_set)
            for color in color_tuple:
                for s in remaining:
                    if indextocolor(s) == color:
                        result.append(s)
                        remaining.remove(s)
                        break
                else:
                    raise ValueError(
                        f"No se encontró color {color} en {sticker_set}")
            return result

        def perm_parity(perm):
            n = len(perm)
            visited = [False] * n
            parity = 0
            for i in range(n):
                if not visited[i]:
                    j, length = i, 0
                    while not visited[j]:
                        visited[j] = True
                        j = perm[j]
                        length += 1
                    parity ^= (length - 1) & 1
            return parity

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
            if x_found is None:
                raise ValueError(
                    f"Posición {z}: colores de esquina inválidos {colors_here}")

            ordered  = ordered_indices(sset, corners[z])
            observed = tuple(self.array[s] for s in ordered)

            y_found = next(
                (y for y in range(3)
                 if tuple(corners[x_found][(y + i) % 3] for i in range(3))
                    == observed), None)
            if y_found is None:
                raise ValueError(
                    f"No se puede determinar orientación de esquina en pos {z}")

            rho[x_found] = z
            v[z]         = y_found

        # ----- Aristas -----
        for z in range(12):
            sset        = edgesid[z]
            colors_here = {self.array[s] for s in sset}

            x_found = next(
                (k for k in range(12) if set(edges[k]) == colors_here), None)
            if x_found is None:
                raise ValueError(
                    f"Posición {z}: colores de arista inválidos {colors_here}")

            ordered  = ordered_indices(sset, edges[z])
            observed = tuple(self.array[s] for s in ordered)

            y_found = next(
                (y for y in range(2)
                 if tuple(edges[x_found][(y + i) % 2] for i in range(2))
                    == observed), None)
            if y_found is None:
                raise ValueError(
                    f"No se puede determinar orientación de arista en pos {z}")

            sigma[x_found] = z
            w[z]           = y_found

        # ----- Validación de estado legal -----
        if sorted(rho) != list(range(8)):
            raise ValueError(f"Permutación de esquinas inválida: {rho}")
        if sorted(sigma) != list(range(12)):
            raise ValueError(f"Permutación de aristas inválida: {sigma}")
        if sum(v) % 3 != 0:
            raise ValueError(f"Suma de orientaciones de esquina {sum(v)} ≠ 0 mod 3")
        if sum(w) % 2 != 0:
            raise ValueError(f"Suma de orientaciones de arista {sum(w)} ≠ 0 mod 2")
        if perm_parity(rho) ^ perm_parity(sigma) != 0:
            raise ValueError("Paridades de permutación incompatibles")

        return Rubik333(v, w, rho, sigma)
   
    def diagnose(self):
        empty = [i for i in range(48) if self.array[i] == -1]
        print(f"Stickers vacíos: {empty}")

        seen_corners = {}
        for z in range(8):
            colors = tuple(sorted(self.array[s] for s in cornersid[z]))
            if any(c == -1 for c in colors):
                print(f"Esquina {z}: incompleta")
                continue
            if (OPPOSITE[colors[0]] == colors[1]
                    or OPPOSITE[colors[0]] == colors[2]
                    or OPPOSITE[colors[1]] == colors[2]):
                print(f"Esquina {z}: contiene opuestos {colors}")
            match = [k for k in range(8) if set(corners[k]) == set(colors)]
            if not match:
                print(f"Esquina {z}: {colors} no es ninguna esquina válida")
            elif len(match) == 1:
                if match[0] in seen_corners:
                    print(f"Esquina {z} y {seen_corners[match[0]]}: "
                          f"misma pieza {corners[match[0]]}")
                seen_corners[match[0]] = z

        seen_edges = {}
        for z in range(12):
            colors = tuple(sorted(self.array[s] for s in edgesid[z]))
            if any(c == -1 for c in colors):
                print(f"Arista {z}: incompleta")
                continue
            if OPPOSITE[colors[0]] == colors[1]:
                print(f"Arista {z}: contiene opuestos {colors}")
            match = [k for k in range(12) if set(edges[k]) == set(colors)]
            if not match:
                print(f"Arista {z}: {colors} no es ninguna arista válida")
            elif len(match) == 1:
                if match[0] in seen_edges:
                    print(f"Arista {z} y {seen_edges[match[0]]}: "
                          f"misma pieza {edges[match[0]]}")
                seen_edges[match[0]] = z

        print("Diagnóstico terminado.")
    # fin
    def draw_centers(self):
        for z in range(6): # DRAW CENTERS
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
                py5.fill(palette[self.array[z]]) # type: ignore
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
