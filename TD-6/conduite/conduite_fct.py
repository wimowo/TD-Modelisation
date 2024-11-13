# Importation des modules
import numpy as np


def mdf(prm):
    """Fonction simulant avec la méthode des différences finies

    Entrées:
        - prm : Objet class parametres()
            - Tr : Température à l'intérieur de la conduite [K]
            - Te : Température ambiante autour de la conduite [K]
            - k : Conductivité thermique [W*m^-1*K^-1]
            - h : Coefficient de convection thermique [W*m^-2*K^-1]
            - Re : Rayon externe [m]
            - Ri : Rayon interne [m]
            - n : Nombre de noeuds [-]
            - dr : Pas en espace [m]

    Sortie (dans l'ordre énuméré ci-bas):
        - Vecteur (array) de dimension N composé de la position radiale à laquelle les températures sont calculées, où N le nombre de noeuds.
        - Vecteur (array) de dimension N composé de la température en fonction du rayon, où N le nombre de noeuds
    """

    A = np.zeros([prm.n, prm.n])
    b = np.zeros(prm.n)
    A[0, 0] = 1
    A[-1, -1] = (3 * prm.k / (2 * prm.dr)) + prm.h
    A[-1, -2] = -4 * prm.k / (2 * prm.dr)
    A[-1, -3] = prm.k / (2 * prm.dr)
    b[0] = prm.Tr
    b[-1] = prm.h * prm.Te
    r = np.linspace(prm.Ri, prm.Re, prm.n)
    for i in range(1, prm.n - 1):
        A[i, i - 1] = (1 - (prm.dr / (2 * r[i])))
        A[i, i] = -2
        A[i, i + 1] = ((prm.dr / (2 * r[i])) + 1)
        b[i] = 0
    T = np.linalg.solve(A, b)
    return r, T
