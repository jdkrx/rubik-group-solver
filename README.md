# Rubik's Cube & Twisty Puzzles Group Theory Solver

Implementación en Python de algoritmos basados en **Teoría de Grupos** y cadenas de subgrupos con el método de Thistlethwaite para la resolución eficiente del Cubo de Rubik 3x3, además de solvers basados en BFS para 2x2, Skewb y Pyraminx.

**Autores:** Santiago Santander, Leyla Sanhueza, Valentina Paillahueque

---

## Características y Rendimiento

* **Cubo 3x3 (Método de Thistlethwaite):** Resolución en complejidad $O(1)$ (< 1 segundo) mediante tablas de representantes de clase precalculadas.
* **Generación de Representantes:** Algoritmo en $O(n)$ que calcula y serializa en `.json` el total de $1,777,565$ representantes de clase en ~3 minutos.
* **Otros Rompecabezas (2x2, Skewb, Pyraminx):** Resolución en tiempo real mediante Búsqueda en Anchura (BFS) y reducción por subgrupos (< 1s para 2x2/Skewb, < 2s para Pyraminx).

---

## Instalación y Uso

### 1. Requisitos y dependencias
* Python 3.8 o superior.
* Java-17 o superior*

### 2. Clonar el repositorio
```bash
git clone https://github.com/jdkrx/rubik-group-solver.git
cd rubik-group-solver
```

### 3. Configuración de entorno virtual y librerías
```bash
python3 -m venv venv
source venv/bin/activate
pip install .
```
Antes de ir al siguiente paso es necesario tener instalado el JDK de Java 17 o superior y tener configurada la variable global JAVA_HOME

### 4. Ejecutar el proyecto
Con interfaz gráfica
```bash
python3 src/main.py
```
o alternativamente se puede ejecutar una CLI.
```bash
python3 src/CLI.py
```
---

## Aspectos Matemáticos

### Modelado del Grupo Legal ($3 \times 3 \times 3$)
A diferencia de los rompecabezas menores (modelados con permutaciones de pegatinas en $S_{48}$ [[1]][RotationGroup]), el grupo legal $G$ del cubo $3 \times 3$ se modela mediante el teorema fundamental de la teoría de cubos [[2]][Adventures in Group Theory] como el producto semidirecto:

$$G = (\mathbb{Z}_3^8 \times \mathbb{Z}_2^{12})_* \rtimes (S_8 \times S_{12})^+$$

con las restricciones de conservación de orientación y paridad:

$$(\mathbb{Z}_3^8 \times \mathbb{Z}_2^{12})_* = \left\\{ (v, w) \in \mathbb{Z}_3^8 \times \mathbb{Z}_2^{12} : \sum_{i=0}^7 v_i \equiv 0 \pmod 3, \; \sum_{j=0}^{11} w_j \equiv 0 \pmod 2 \right\\}$$

$$(S_8 \times S_{12})^+ = \\{ (\rho, \sigma) \in S_8 \times S_{12} : sgn(\rho) = sgn(\sigma) \\}$$

### Cadena de Subgrupos (Thistlethwaite)
El solver reduce cualquier estado $g_0 \in G$ al estado resuelto $id_G$ atravesando la cadena de subgrupos:

$$G_0 > EO > DR > HTR > G_4 = \\{id_G\\}$$

| Paso | Subgrupo | Generadores | Firma de Clase Lateral | Representantes encontrados |
| :--- | :--- | :--- | :--- | :--- |
| **1** | $G_0 / EO$ | $\langle U, D, R, L, F, B \rangle$ | Vector de orientación de aristas $w$ | $2,048$ |
| **2** | $EO / DR$ | $\langle U, D, R, L, F^2, B^2 \rangle$ | Orientación de esquinas y piezas en capa E $(v, \text{sorted}(\sigma[4:8]))$ | $1,082,565$ |
| **3** | $DR / HTR$ | $\langle U, D, R^2, L^2, F^2, B^2 \rangle$ | Órbita $O_1 = \\{0,2,8,10\\}$ y clase lateral de $\rho$ por $H \le S_8$ | $29,400$ |
| **4** | $HTR / G_4$ | $\langle U^2, D^2, R^2, L^2, F^2, B^2 \rangle$ | Tupla completa $(v, w, \rho, \sigma)$ | $663,552$ |

*(Los conteos obtenidos coinciden exactamente con la demostración original de Thistlethwaite de 1981, comprobando que el método utilizado es correcto)*.

---

## Referencias y Documentación
* **Bitácora de investigación:** El desarrollo teórico copmpleto está disponible en el [repositorio de investigación](https://github.com/jdkrx/Proyectoprogra).
* Oliver Knill, [*Rotation Group of Rubik's Cube*.](https://people.math.harvard.edu/~knill/offprints/sigsam1987.pdf
)
* David Joyner, [*Adventures in Group Theory: Rubik's Cube, Merlin's Machine, and Other Mathematical Toys*.](https://www.sandal.tw/upload/Adventures%20in%20Group%20Theory_%20Rubik%27s%20Cube,%20Merlin%27s%20Machine,%20and%20Other%20Mathematical%20Toys%20by%20David%20Joyner.pdf)

[Adventures in Group Theory]: https://www.sandal.tw/upload/Adventures%20in%20Group%20Theory_%20Rubik%27s%20Cube,%20Merlin%27s%20Machine,%20and%20Other%20Mathematical%20Toys%20by%20David%20Joyner.pdf
[RotationGroup]: https://people.math.harvard.edu/~knill/offprints/sigsam1987.pdf
