# Importation des modules
import matplotlib.pyplot as plt
import numpy as np
import pytest
try:
    from algorithmie_fct import *
except:
    pass

import algorithmie_corr

# Série harmonique

x = np.arange(50, 1001)
y = np.empty(x.shape)

for i in range(x.size):
    y[i] = serie_harmonique(x[i])

plt.plot(x, y)
plt.grid(True)
plt.title("Somme de la série harmonique")
plt.xlabel("Nombre d'éléments (N)")
plt.ylabel("S(N)")
plt.legend(['S(N)'])
plt.savefig("harmonique_somme.png")
plt.show()

# Factoriel


# Correction
pytest.main(['-q', '--tb=long', 'algorithmie_corr.py'])