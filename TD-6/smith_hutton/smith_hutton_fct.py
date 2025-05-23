# Importation des modules
import numpy as np


def position(X, Y, nx, ny):
    """ Fonction générant deux matrices de discrétisation de l'espace

    Entrées:
        - X : Bornes du domaine en x, X = [x_min, x_max]
        - Y : Bornes du domaine en y, Y = [y_min, y_max]
        - nx : Discrétisation de l'espace en x (nombre de points)
        - ny : Discrétisation de l'espace en y (nombre de points)

    Sorties (dans l'ordre énuméré ci-bas):
        - x : Matrice (array) de dimension (ny x nx) qui contient la position en x
        - y : Matrice (array) de dimension (ny x nx) qui contient la position en y
            * Exemple d'une matrice position :
            * Si X = [-1, 1] et Y = [0, 1]
            * Avec nx = 3 et ny = 3
                x = [-1    0    1]
                    [-1    0    1]
                    [-1    0    1]

                y = [1    1    1  ]
                    [0.5  0.5  0.5]
                    [0    0    0  ]
    """
    x = np.linspace(X[0], X[1], nx)
    y = np.linspace(Y[1], Y[0], ny)

    x, y = np.meshgrid(x, y)

    return x, y


def vitesse(x, y):
    """ Fonction donnant les vitesses en x et y selon la position

    Entrées:
        - x : Matrice de dimension (ny x nx) qui contient la position en x
        - y : Matrice de dimension (ny x nx) qui contient la position en y

    Sorties (dans l'ordre énuméré ci-bas):
        - u : Matrice (array) de dimension (ny x nx) qui contient la vitesse en x
        - v : Matrice (array) de dimension (ny x nx) qui contient la vitesse en y

    """

    u = 2 * y * (1 - x ** 2)
    v = -2 * x * (1 - y ** 2)

    return u, v


def mdf_assemblage(X, Y, nx, ny, Pe, alpha):
    """ Fonction assemblant la matrice A et le vecteur b

    Entrées:
        - X : Bornes du domaine en x, X = [x_min, x_max]
        - Y : Bornes du domaine en y, Y = [y_min, y_max]
        - nx : Discrétisation de l'espace en x (nombre de points)
        - ny : Discrétisation de l'espace en y (nombre de points)
        - Pe : Nombre de Péclet
        - alpha : Constante des conditions de Dirichlet sur les frontières

    Sorties (dans l'ordre énuméré ci-bas):
        - A : Matrice (array)
        - b : Vecteur (array)
    """
    N = ny * nx
    A = np.zeros((N, N))
    b = np.zeros(N)

    dx = (X[1] - X[0]) / (nx - 1)
    dy = (Y[1] - Y[0]) / (ny - 1)
    dx2 = dx ** 2
    dy2 = dy ** 2

    px, py = position(X, Y, nx, ny)
    vx, vy = vitesse(px, py)

    for x in range(nx):
        for y in range(ny):
            k = index(x, y, ny)
            posx = px[y, x]
            posy = py[y, x]

            if posx == 0 or y == (ny - 1) or x == (nx - 1):
                A[k, k] = 1
                b[k] = 1 - np.tanh(alpha)
            elif y == 0 and x <= (nx - 1) / 2:
                A[k, k] = 1
                b[k] = 1 + np.tanh(alpha * (2 * posx + 1))
            elif y == 0:
                A[k, k] = -3
                A[k, k - 1] = 4
                A[k, k - 2] = -1

            else:
                A[k, index(x - 1, y, ny)] = 1 / dx2 + Pe * vx[y,  x] / (2*dx)
                A[k, index(x, y - 1, ny)] = 1 / dy2 -Pe * vy[y,  x] / (2*dy)
                A[k, k] = -2 * (1 / dx2 + 1 / dy2)
                A[k, index(x + 1, y, ny)] = 1 / dx2 - Pe * vx[y,  x] / (2*dx)
                A[k, index(x, y + 1, ny)] = 1 / dy2+Pe * vy[y,  x] / (2*dy)


    return A, b


def index(x, y, ny):
    return (ny - y - 1) + (x * ny)
