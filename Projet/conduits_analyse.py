import numpy as np

try:
    from conduits_fonctions import *
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

# Definition des reseaux de noeuds a analyser
reseau_2_noeuds = {0: {"voisins": [1], "pression": 100},
                   1: {"voisins": [0], "debit": 0.5},
                   }

reseau_3_noeuds = {0: {"voisins": [1], "pression": 100},
                   1: {"voisins": [0, 2], "debit": 0.1},
                   2: {"voisins": [1], "debit": 0.1},
                   }

reseau_4_noeuds = {0: {"voisins": [2, 3], "pression": 100},
                   1: {"voisins": [2, 3], "pression": 95},
                   2: {"voisins": [0, 1], "debit": 0.3},
                   3: {"voisins": [0, 1], "debit": 0.2}
                   }

reseau_6_noeuds = {0: {"voisins": [2, 3], "pression": 100},
                   1: {"voisins": [2, 3, 5], "pression": 95},
                   2: {"voisins": [0, 1], "debit": 0.3},
                   3: {"voisins": [0, 1, 4], "debit": 0.2},
                   4: {"voisins": [3, 5], "debit": 0.4},
                   5: {"voisins": [1, 4], "debit": 0.1}}
reseau_7_noeuds = {0: {"voisins": [2, 3], "pression": 100},
                   1: {"voisins": [2, 3, 5], "pression": 95},
                   2: {"voisins": [0, 1], "debit": 0.3},
                   3: {"voisins": [0, 1, 4], "debit": 0.2},
                   4: {"voisins": [3, 6], "debit": 0.4},
                   5: {"voisins": [1, 6], "debit": 0.1},
                   6: {"voisins": [4, 5], "debit": 2}
                   }
reseau_8_noeuds = {0: {"voisins": [1], "pression": 100},
                   1: {"voisins": [0, 2], "debit": 0.2},
                   2: {"voisins": [1, 3, 6], "debit": 0.15},
                   3: {"voisins": [2, 4, 5], "debit": 0.2},
                   4: {"voisins": [3, 5], "pression": 123.89},
                   5: {"voisins": [3, 4, 7], "debit": 0.86334},
                   6: {"voisins": [2, 7], "debit": 0.1981},
                   7: {"voisins": [5, 6], "pression": 80.11},
                   }

reseau_pression = {0: {"voisins": [2, 3], "pression": 100},
                   1: {"voisins": [2, 3], "pression": 95},
                   2: {"voisins": [0, 1], "pression": 80},
                   3: {"voisins": [0, 1], "pression": 20}
                   }

# Resolution du probleme
tol = 1e-5
N = 10000

noeuds, conduits = calculation_sim(reseau_6_noeuds, prm)
for p in noeuds:
    print(p,":")
    print("Pression :", noeuds[p]["pression"], "mmH2O")
    print("Debit :", noeuds[p]["debit"], "m³/s")
    print("-------------------------------")

for c in conduits:
    print(c,":")
    print("Noeuds :", conduits[c]["noeuds"])
    print("Debit :", conduits[c]["debit"], "m³/s")
    print("-------------------------------")
