import time
import json
from pathlib import Path

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
gens1 = [U2, D2, F2, B2, L2, R2, U, D, F, B, R, L, u, d, b, f, r, l]
gens2 = [U2, D2, F2, B2, L2, R2, U, D, R, L, u, d, r, l]
gens3 = [U2, D2, F2, B2, L2, R2, U, D, u, d]
gens4 = [U2, D2, F2, B2, L2, R2]
reps1 = [()]
reps2 = [()]
reps3 = [()]
reps4 = [()]
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
def getreps1():
    firma_identidad = obtener_firma_G0_G1(ID_CUBO)
    vertex = {firma_identidad}
    tovisit = [(ID_CUBO, [])]
    while tovisit:
        actual, camino = tovisit.pop(0)
        for gen in gens1:
            vecino = actual * gen
            firma = obtener_firma_G0_G1(vecino)
            if firma not in vertex:
                vertex.add(firma)
                nuevocamino = camino + [namegen(gen)]
                tovisit.append((vecino, nuevocamino))
                reps1.append(tuple(nuevocamino))
    print("Representantes de G0/G1 encontrados")
def getreps2():
    firma_identidad = obtener_firma_G1_G2(ID_CUBO)
    vertex = {firma_identidad}
    tovisit = [(ID_CUBO, [])]
    while tovisit:
        actual, camino = tovisit.pop(0)
        for gen in gens2:
            vecino = actual * gen
            firma = obtener_firma_G1_G2(vecino)
            if firma not in vertex:
                vertex.add(firma)
                nuevocamino = camino + [namegen(gen)]
                tovisit.append((vecino, nuevocamino))
                reps2.append(tuple(nuevocamino))
    print("Representantes de G1/G2 encontrados")
def getreps3():
    firma_identidad = obtener_firma_G2_G3(ID_CUBO)
    vertex = {firma_identidad}
    tovisit = [(ID_CUBO, [])]
    while tovisit:
        actual, camino = tovisit.pop(0)
        for gen in gens3:
            vecino = actual * gen
            firma = obtener_firma_G2_G3(vecino)
            if firma not in vertex:
                vertex.add(firma)
                nuevocamino = camino + [namegen(gen)]
                tovisit.append((vecino, nuevocamino))
                reps3.append(tuple(nuevocamino))
    print("Representantes de G2/G3 encontrados")
def getreps4():
    firma_identidad = obtener_firma_G3_G4(ID_CUBO)
    vertex = {firma_identidad}
    tovisit = [(ID_CUBO, [])]
    while tovisit:
        actual, camino = tovisit.pop(0)
        for gen in gens4:
            vecino = actual * gen
            firma = obtener_firma_G3_G4(vecino)
            if firma not in vertex:
                vertex.add(firma)
                nuevocamino = camino + [namegen(gen)]
                tovisit.append((vecino, nuevocamino))
                reps4.append(tuple(nuevocamino))
    print("Representantes de G3/G4 encontrados")

def get_reps1():
    inicio = time.perf_counter()
    getreps1()
    URL = str(Path(__file__).resolve().parent) + "/representantes"
    with open(f"{URL}/G0-G1.json", "w", encoding="utf-8") as file:
        file.write(json.dumps(reps1, indent=4))
    final = time.perf_counter()
    print(f"Tiempo de ejecución: {final - inicio} segundos.")
def get_reps2():
    inicio = time.perf_counter()
    getreps2()
    URL = str(Path(__file__).resolve().parent) + "/representantes"
    with open(f"{URL}/G1-G2.json", "w", encoding="utf-8") as file:
        file.write(json.dumps(reps2, indent=4))
    final = time.perf_counter()
    print(f"Tiempo de ejecución: {final - inicio} segundos.")
def get_reps3():
    inicio = time.perf_counter()
    getreps3()
    URL = str(Path(__file__).resolve().parent) + "/representantes"
    with open(f"{URL}/G2-G3.json", "w", encoding="utf-8") as file:
        file.write(json.dumps(reps3, indent=4))
    final = time.perf_counter()
    print(f"Tiempo de ejecución: {final - inicio} segundos.")
def get_reps4():
    inicio = time.perf_counter()
    getreps4()
    URL = str(Path(__file__).resolve().parent) + "/representantes"
    with open(f"{URL}/G3-G4.json", "w", encoding="utf-8") as file:
        file.write(json.dumps(reps4, indent=4))
    final = time.perf_counter()
    print(f"Tiempo de ejecución: {final - inicio} segundos.")