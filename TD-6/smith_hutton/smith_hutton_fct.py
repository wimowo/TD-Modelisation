# Importation des modules
import numpy as np

def position(X,Y,nx,ny):
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

    x = np.zeros((ny,nx))
    y = np.zeros((nx,ny))

    for i in range(ny):
        x[i] = np.linspace(X[0],X[1],nx)

    for i in range(nx):
        y[i] = np.linspace(Y[1],Y[0],ny)

    return x, y.T

def vitesse(x,y):
    """ Fonction donnant les vitesses en x et y selon la position

    Entrées:
        - x : Matrice de dimension (ny x nx) qui contient la position en x
        - y : Matrice de dimension (ny x nx) qui contient la position en y

    Sorties (dans l'ordre énuméré ci-bas):
        - u : Matrice (array) de dimension (ny x nx) qui contient la vitesse en x
        - v : Matrice (array) de dimension (ny x nx) qui contient la vitesse en y

    """

    u = 2*y*(1-x**2)
    v = -2*x*(1-y**2)

    return u,v

def mdf_assemblage(X,Y,nx,ny,Pe,alpha):
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
    N = ny*nx
    A = np.zeros((N,N))
    b = np.zeros((N,1))

    dx = (X[1] - X[0])/(nx-1)
    dy = (Y[1] - Y[0])/(ny-1)

    px,py  = position(X,Y,nx,ny)
    vx,vy = vitesse(px, py)

    for k in range(N):
        y = k%(ny-1)
        x = k//ny

        if(x==0 or y==(ny-1) or x==(nx-1)):
            A[k, k] = 1
            b[k] = 1-np.tanh(alpha)
        elif (y == 0 and x <= (nx-1)/2):
            A[k, k] = 1
            b[k] = 1 + np.tanh(alpha*(2*px[x,y]+1))
        elif(y==0):
            continue
        else:
            A[k-y-x, k] = y**-2+Pe*vy[x,y-1]/(dy*2)
            A[k,k-1] = dx**-2+Pe*vx[x-1,y]/(dx*2)
            A[k,k] = -2*(dx**-2+dy**-2)
            A[k, k + 1] = dx ** -2 - Pe * vx[x+1,y] / (dx * 2)
            A[k+y+(nx-x),k] = y ** -2 - Pe * vy[x,y+1] / (dy * 2)

    return A, b
