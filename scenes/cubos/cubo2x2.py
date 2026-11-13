import py5
from math import pi as PI

def getcolor(x): # en el array de estado guardamos el color con un numero, esta funcion traduce los numeros a colores
    if x==0:
        return py5.color(255, 255, 255)
    if x==1:
        return py5.color(255, 128, 0)
    if x==2:
        return py5.color(0,255,0)
    if x==3:
        return py5.color(255, 0, 0)
    if x==4:
        return py5.color(0, 0, 255)
    if x==5:
        return py5.color(255, 255, 0)
setcoord = [# un array con las instrucciones para llegar a cada pegatina del cubo
            # [ (rotacionx, rotaciony), translate(x, y, z) ] -> id de pieza en el espacio de piezas
            [(PI/2, 0), (75, 0, 75)], 
            [(PI/2, 0), (75, 75, 75)],
            [(PI/2, 0), (0, 75, 75)],
            [(PI/2, 0), (0, 0, 75)],
            [(0, 0), (75, 0, -75)],
            [(0, 0), (0, 0, -75)],
            [(0, 0), (0, 75, -75)],
            [(0, PI/2), (75, 0, -75)],
            [(0, PI/2), (0, 0, -75)],
            [(0, PI/2), (0, 75, -75)],
            [(0, PI/2), (75, 75, -75)],
            [(0, 0), (0, 0, 75)],
            [(0, 0), (75, 0, 75)],
            [(0, 0), (75, 75, 75)],
            [(0, 0), (0, 75, 75)],
            [(0, PI/2), (0, 0, 75)],
            [(0, PI/2), (75, 0, 75)],
            [(0, PI/2), (0, 75, 75)],
            [(PI/2, 0), (0, 0, -75)],
            [(PI/2, 0), (0, 75, -75)],
            [(PI/2, 0), (75, 75, -75)]
]
class cube:
    def __init__(self):
        self.state = [0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 5, 5] # inicializamos el cubo armado
        
    def display(self):
        for i in range(len(setcoord)):
            x = setcoord[i][1][0] # grabamos las coords xyz que teniamos guardadas para cada pieza
            y = setcoord[i][1][1]
            z = setcoord[i][1][2]
            py5.rotate_x(setcoord[i][0][0])
            py5.rotate_y(setcoord[i][0][1])
            py5.translate(x, y, z)
            py5.fill(getcolor(self.state[i])) # seleccionamos el color de cada pegatina
            py5.rect(-75, -75, 75, 75) # dibujamos un cuadro de ese color
            py5.translate(-x, -y, -z)
            py5.rotate_y(-setcoord[i][0][1])
            py5.rotate_x(-setcoord[i][0][0])