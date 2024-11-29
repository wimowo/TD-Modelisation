import numpy as np

try:
    from fonctions import *
except:
    pass


class parametres():
    L = 25  # Longueur des conduits (m)
    D = 0.2  # Diametre (m)
    e = 0.00026  # Rugosite (m)
    rho = 1000  # Masse volumique (kg/m3)
    mu = 0.00089  # Viscosite dynamique (pa/s)
    n = 1.8099


prm = parametres()

tol = 0.01

reseau_2_noeuds = {0: {"voisins": [1], "pression": 100},
                   1: {"voisins": [0], "debit": 0.5},
                   }

reseau_6_noeuds = {0: {"voisins": [2, 3], "pression": 100},
                   1: {"voisins": [2, 3, 5], "pression": 95},
                   2: {"voisins": [0, 1], "debit": 0.3},
                   3: {"voisins": [0, 1, 4], "debit": 0.2},
                   4: {"voisins": [3, 5], "debit": 0.4},
                   5: {"voisins": [1, 4], "debit": 0.1}}

print("Conduits 6 noeuds:", conduits(reseau_6_noeuds))
print("Conduits 2 noeuds:", conduits(reseau_2_noeuds))

Q = np.array([0.3,0.2,0.3,0.2,0.4,0.1,0.4])
P = np.array([100,95,97,97,90,93])


print(residu(Q, P, reseau_6_noeuds, prm))
print(newton_resolution(Q, P, tol,reseau_6_noeuds, prm))

Q = np.array([0.5])
P = np.array([100,95])
print(residu(Q, P, reseau_2_noeuds, prm))
