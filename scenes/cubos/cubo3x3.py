import py5
from math import pi as PI

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
U_LAYER = {
    ("U", "B"),
    ("U", "R"),
    ("U", "F"),
    ("U", "L"),
    ("U", "B", "L"),
    ("U", "B", "R"),
    ("U", "F", "R"),
    ("U", "F", "L")
}
E_LAYER = {
    ("B", "L"),
    ("F", "L"),
    ("F", "R"),
    ("B", "R")
}
D_LAYER = {
    ("D", "F"),
    ("D", "R"),
    ("D", "B"),
    ("D", "L"),
    ("D", "F", "L"),
    ("D", "F", "R"),
    ("D", "B", "R"),
    ("D", "B", "L") 
}

# una pieza debe ser 80x80x80
def drawEdge(edge, orientation):
    if orientation == 1: edge = (edge[1], edge[0])
    # py5.stroke(255, 0, 0)
    # py5.line(0, 0, 0, 100, 0, 0) # x rojo
    # py5.stroke(0, 255, 0)
    # py5.line(0, 0, 0, 0, 100, 0) # y verde
    # py5.stroke(0, 0, 255)
    # py5.line(0, 0, 0, 0, 0, 100) # z azul

    py5.stroke(0)
    py5.rect_mode(py5.CENTER)

    
    py5.translate(0, 0, 40)
    py5.fill(palette[edge[1]])
    py5.rect(0, 0, 80, 80)
    py5.translate(0, 0, -40)
    py5.translate(0, -40, 0)
    py5.rotate_x(PI/2)

    py5.fill(palette[edge[0]])
    py5.rect(0, 0, 80, 80)

    py5.rotate_x(-PI/2)
    py5.translate(0, 40, 0)
    py5.rect_mode(py5.CORNER)
def drawCorner(corner, orientation):
    if orientation == 1:  corner = (corner[1], corner[2], corner[0])
    if orientation == 2:  corner = (corner[2], corner[0], corner[1])
    # py5.stroke(255, 0, 0)
    # py5.line(0, 0, 0, 100, 0, 0) # x rojo
    # py5.stroke(0, 255, 0)
    # py5.line(0, 0, 0, 0, 100, 0) # y verde
    # py5.stroke(0, 0, 255)
    # py5.line(0, 0, 0, 0, 0, 100) # z azul

    py5.stroke(0)
    py5.rect_mode(py5.CENTER)

    
    py5.translate(0, 0, 40)
    py5.fill(palette[corner[1]])
    py5.rect(0, 0, 80, 80)
    py5.translate(0, 0, -40)

    py5.translate(0, -40, 0)
    py5.rotate_x(PI/2)
    py5.fill(palette[corner[0]])
    py5.rect(0, 0, 80, 80)
    py5.rotate_x(-PI/2)
    py5.translate(0, 40, 0)

    py5.translate(40, 0, 0)
    py5.rotate_y(PI/2)
    py5.fill(palette[corner[2]])
    py5.rect(0, 0, 80, 80)
    py5.rotate_y(-PI/2)
    py5.translate(-40, 0, 0)

    py5.rect_mode(py5.CORNER)

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
    def display(self):
        for z in range(12):
            x = self.sigma[z]
            sigmainversa = [0]*12
            for i in range(12): sigmainversa[self.sigma[i]] = i
            x = sigmainversa[z]

            y = self.w[z]
            a = setcoordedges[z][1][0]
            b = setcoordedges[z][1][1]
            c = setcoordedges[z][1][2]
            py5.translate(a, b, c)
            py5.rotate_x(setcoordedges[z][0][0])
            py5.rotate_y(setcoordedges[z][0][1])
            drawEdge(edges[x], y)
            py5.rotate_y(-setcoordedges[z][0][1])
            py5.rotate_x(-setcoordedges[z][0][0])
            py5.translate(-a, -b, -c)
        for z in range(8):
            x = self.rho[z]
            rhoinversa = [0]*8
            for i in range(8): rhoinversa[self.rho[i]] = i
            x = rhoinversa[z]
            y = self.v[z]
            a = setcoordcorners[z][1][0]
            b = setcoordcorners[z][1][1]
            c = setcoordcorners[z][1][2]
            py5.translate(a, b, c)
            py5.rotate_x(setcoordcorners[z][0][0])
            py5.rotate_y(setcoordcorners[z][0][1])
            drawCorner(corners[x], y)
            py5.rotate_y(-setcoordcorners[z][0][1])
            py5.rotate_x(-setcoordcorners[z][0][0])
            py5.translate(-a, -b, -c)
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