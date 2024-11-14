# Importation des modules
import numpy as np


def mdf(prm):
    """Fonction qui calcule le profil de température le long de l'ailette

    Entrées:
        - prm : Objet class parametres()
            - L : Longueur
            - D : Diamètre
            - k : Conductivité thermique
            - T_a : Température ambiante
            - T_w : Température du mur
            - h : Coefficient de convection
            - N : Nombre de points utilisés pour la méthode

    Sorties (dans l'ordre énuméré ci-bas):
        - Vecteur (np.array) donnant la température tout au long de l'ailette en Kelvin
        - Vecteur (np.array) donnant la position tout au long de l'ailette (axe z) en mètre
    """
    dz = prm.L / (prm.N - 1)
    z = np.linspace(0, prm.L, prm.N)
    A = np.zeros((prm.N, prm.N))

    A[0, 0] = 1
    A[-1, -3] = 1
    A[-1, -2] = -4
    A[-1, -1] = 3
    for i in range(1, prm.N - 1):
        A[i, i - 1] = 1
        A[i, i] = -2 - (4 * prm.h * dz ** 2) / (prm.k * prm.D)
        A[i, i + 1] = 1

    b = np.zeros(prm.N)
    b[0] = prm.T_w
    for i in range(1, prm.N - 1):
        b[i] = ((-4 * prm.h * dz ** 2) / (prm.k * prm.D)) * prm.T_a

    T = np.linalg.solve(A, b)

    return T, z


def inte(T, z, prm):
    """Fonction qui intègre la convection sur la surface de l'ailette.

    Entrées:
        - T : Vecteur comprenant les températures  en Kelvin sur la longueur de l'ailette
                pour une combinaison géométrique donnée
        - z : Vecteur comprenant les points sur la longueur en mètre
        - prm : Objet class parametres()
            - k : Conductivité thermique
            - T_a : Température ambiante
            - T_w : Température du mur
            - h : Coefficient de convection
            - N : Nombre de points utilisés pour la méthode

    Sortie:
        - Valeur numérique de l'intégrale résultante (perte en W)
    """

    I = 0
    dz = z[1] - z[0]
    f = lambda t: prm.h * np.pi * prm.D * (t - prm.T_a)

    for i in range(prm.N - 1):
        I += (f(T[i]) + f(T[i + 1])) * dz / 2

    return I  # à compléter
