# Importation des modules
import matplotlib.pyplot as plt
import numpy as np
import pytest
try:
    from manip_vec_mat_fct import *
except:
    pass

import manip_vec_mat_corr


# Manipulation d'un vecteur

# Créer le graphique
plt.xlabel("x")
plt.ylabel("f(x)")
plt.title('Graphique de la fonction f(x)')
plt.grid(True)
plt.plot(faire_vecteur_x(),faire_vecteur_f(), label = 'f(x)')

plt.legend()
plt.show()

# Résolution d'un système linéaire
mat = faire_matrice()
b = faire_second_membre()

print(np.linalg.solve(mat, b))

# Correction
pytest.main(['-q', '--tb=long', 'manip_vec_mat_corr.py'])