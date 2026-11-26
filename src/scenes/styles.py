import py5
from py5ui import *
fontsize = 20 # tamaño de la letra en el menu
width = 800
height = 600

fontsize = 20

color_fondo_pantalla_cubo = py5.color(217, 244, 164)
config_barmenu1 = (
    py5.color(40, 40, 55), # Color relleno sin clickear
    py5.color(40, 40, 55), # Color relleno durante click
    py5.color(40, 40, 55), # Color relleno mouse encima
    py5.color(255), # Color texto
    py5.color(40, 40, 55),   # Color trazo
    1, # Grosor trazo (px)
    0  # Radio borde (px)
)

config_barmenu2 = ( # Menus internos
    py5.color(55, 55, 70), # Color relleno sin clickear
    py5.color(55, 55, 70), # Color relleno durante click
    py5.color(55, 55, 70), # Color relleno mouse encima
    py5.color(255), # Color texto
    py5.color(40, 40, 55),   # Color trazo
    1, # Grosor trazo (px)
    0  # Radio borde (px)
)

config_boton_inicio = ( # Boton del inicio
    py5.color(255, 118, 162), # Color relleno sin clickear
    py5.color(255, 118, 162), # Color relleno durante click
    py5.color(255, 118, 162), # Color relleno mouse encima
    py5.color(0), # Color texto
    py5.color(0),   # Color trazo
    1, # Grosor trazo (px)
    12  # Radio borde (px)
)
config_botones_principal = ( # Botones en la escena principal
    py5.color(255, 118, 162), # Color relleno sin clickear
    py5.color(255, 118, 162), # Color relleno durante click
    py5.color(255, 118, 162), # Color relleno mouse encima
    py5.color(0), # Color texto
    py5.color(0),   # Color trazo
    1, # Grosor trazo (px)
    12  # Radio borde (px)
)

config_barra = (
    py5.color(40, 40, 55), # Color relleno 
    py5.color(40, 40, 55),   # Color trazo
    1, # Grosor trazo (px)
)

def funcionvacia():
    pass