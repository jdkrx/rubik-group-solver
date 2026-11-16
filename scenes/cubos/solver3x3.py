import json
import time
from representantes import get_reps1, get_reps2, get_reps3, get_reps4
from .cubo3x3 import U

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

# archivoreps1 = False
# archivoreps2 = False
# archivoreps3 = False
# archivoreps4 = False
def configurararchivos(cola):
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
    if True: print(f"Tiempo configurando los representantes: {finalconfig - inicioconfig} segundos")
    cola.put((dict_reps1, dict_reps2, dict_reps3, dict_reps4))

def buscarsolvetw(scramble, dict_reps1, dict_reps2, dict_reps3, dict_reps4):
    
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
        algfinal = algo1
        return (algfinal)
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
        algfinal = algo1 + algo2
        return (algfinal)
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
        algfinal = algo1 + algo2 + algo3
        return (algfinal)
    alg4 = dict_reps4[obtener_firma_G3_G4(scramble*g1.inverso()*g2.inverso()*g3.inverso())]
    str = ""
    algo4 = []
    for i in alg4[::-1]:
        gen = namegen(genname(i).inverso())
        str += gen + " "
        algo4.append(gen)
    algfinal = algo1 + algo2 + algo3 + algo4
    return (algfinal)