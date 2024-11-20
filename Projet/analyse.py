import numpy as np

try:
    from fonctions import *
except:
    pass

class parametres():
    L = 25  # Longueur des conduits (m)
    D = 0.0095  # Taux de transformation en zombie (beta)
    e = 0.005  # Taux de mort de zombie (alpha)
    p = 0.0001  # Taux de mort naturelle (delta)
    u = 0.0001  # Taux de naissance (pi)


prm = parametres()

