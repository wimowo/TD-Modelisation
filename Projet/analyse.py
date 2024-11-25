import numpy as np

try:
    from fonctions import *
except:
    pass


class parametres():
    L = 25  # Longueur des conduits (m)
    D = 0.2  # Diametre (m)
    e = 0.00026  # Rugosite (m)
    p = 1000  # Masse volumique (kg/m3)
    u = 0.00089  # Viscosite dynamique (pa/s)


prm = parametres()

reseau_6_noeuds = {0: {"voisins": [2, 3], "pression": 100},
                   1: {"voisins": [2, 3, 5], "pression": 95},
                   2: {"voisins": [0, 1], "debit": 0.3},
                   3: {"voisins": [0, 1, 4], "debit": 0.2},
                   4: {"voisins": [3, 5], "debit": 0.4},
                   5: {"voisins": [1, 4], "debit": 0.1}}


print(conduits(reseau_6_noeuds))

