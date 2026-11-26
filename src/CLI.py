import json
import time
import threading
import queue
from representantes import get_reps1, get_reps2, get_reps3, get_reps4

debug = True
class Rubik333:
    def __init__(self, v, w, rho, sigma):
        self.v = v[:]
        self.w = w[:]
        self.rho = rho[:]
        self.sigma = sigma[:]
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
if debug: print(f"Grupo H generado, orden: {len(H)}")
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

archivoreps1 = False
archivoreps2 = False
archivoreps3 = False
archivoreps4 = False
def otrohilo(cola):
    print("Haciendo cosas")
    archivoreps1, archivoreps2, archivoreps3, archivoreps4 = (False, False, False, False)
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
    inicioconfig = time.perf_counter()
    pasos = [
        (repscamino1, obtener_firma_G0_G1),
        (repscamino2, obtener_firma_G1_G2),
        (repscamino3, obtener_firma_G2_G3),
        (repscamino4, obtener_firma_G3_G4),
    ]

    dict_reps1, dict_reps2, dict_reps3, dict_reps4 = (construir_dict(caminos, firma) for caminos, firma in pasos)
    finalconfig = time.perf_counter()
    if debug: print(f"Tiempo configurando los representantes: {finalconfig - inicioconfig} segundos")
    cola.put((dict_reps1, dict_reps2, dict_reps3, dict_reps4))

cola = queue.Queue()
t2 = threading.Thread(target=otrohilo, args=(cola,))
t2.start()

def buscarsolvetw(scramble, dict_reps1, dict_reps2, dict_reps3, dict_reps4):
    print()
    print("Solución: ")
    if (scramble == ID_CUBO): 
        print("Cubo ya resuelto")
        return
    alg1 = dict_reps1[obtener_firma_G0_G1(scramble)]
    str = ""
    algo1 = []
    for i in alg1[::-1]:
        gen = namegen(genname(i).inverso())
        str += gen + " "
        algo1.append(gen)
    g1 = ID_CUBO
    for i in alg1:
        g1 = g1*genname(i)
    if (scramble*g1.inverso() == ID_CUBO):
        print(str, "Cubo resuelto!")
        return
    print(str, "Edges Orientated (EO)")
    alg2 = dict_reps2[obtener_firma_G1_G2(scramble*g1.inverso())]
    algo2 = []
    str = ""
    for i in alg2[::-1]:
        gen = namegen(genname(i).inverso())
        str += gen + " "
        algo2.append(gen)
    g2 = ID_CUBO
    for i in alg2:
        g2 = g2*genname(i)

    if (scramble*g1.inverso()*g2.inverso() == ID_CUBO):
        print(str, "Cubo resuelto!")
        return
    print(str, "Domino Reduction (DR)")
    alg3 = dict_reps3[obtener_firma_G2_G3(scramble*g1.inverso()*g2.inverso())]
    str = ""
    algo3 = []
    for i in alg3[::-1]:
        gen = namegen(genname(i).inverso())
        str += gen + " "
        algo3.append(gen)
    g3 = ID_CUBO
    for i in alg3:
        g3 = g3*genname(i)

    if (scramble*g1.inverso()*g2.inverso()*g3.inverso() == ID_CUBO):
        print(str, "Cubo esuelto!")
        return
    print(str, "Half Turn Reduction (HTR)")
    alg4 = dict_reps4[obtener_firma_G3_G4(scramble*g1.inverso()*g2.inverso()*g3.inverso())]
    str = ""
    algo4 = []
    for i in alg4[::-1]:
        gen = namegen(genname(i).inverso())
        str += gen + " "
        algo4.append(gen)
    print(str, "Cubo resuelto!")
    algfinal = algo1 + algo2 + algo3 + algo4
    return (algfinal)
hasget = False
print("Bienvenido al buscador de soluciones de cubo de Rubik 3x3x3")
run = True
# L B' L' B U' F' D L' U L U2 B D2 R D2 B2 F R2 D' L' D U B2 F D'
dict_reps1 = []
dict_reps2 = []
dict_reps3 = []
dict_reps4 = []


while run:
    print("Ingrese 1 para realizar una solve, ingrese 2 para salir del programa")
    inp = input()
    if inp=="2": 
        run = False
        break
    print("Ingrese una mezcla con cada movimiento separado por un espacio ' '")
    mezclastr = input()
    partes = mezclastr.split(" ")
    mezclamoves = ID_CUBO
    if not mezclastr == "":
        for i in partes:
            mezclamoves = mezclamoves*genname(i)
    #print(mezclamoves)
    if not hasget: 
        t2.join()
        dict_reps1, dict_reps2, dict_reps3, dict_reps4 = cola.get()
        hasget = True
    buscarsolvetw(mezclamoves, dict_reps1, dict_reps2, dict_reps3, dict_reps4)
