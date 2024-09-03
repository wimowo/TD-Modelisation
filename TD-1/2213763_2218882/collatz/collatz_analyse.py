# Importation des modules
import matplotlib.pyplot as plt
import numpy as np
import pytest
try:
    from collatz_fct import *
except:
    pass

import collatz_corr

#-----------------------------------------------------------------------------
# Code principal pour l'analyse des résultats des fonctions
# Il faudra appeler la fonction collatz programmée dans collatz_fct.py afin
# de calculer le nombre d'itérations pour les entiers de 1 à 5000 et générer
# 2 graphiques pour la visualisation des résultats.
#-----------------------------------------------------------------------------

# Code principal


#Graphiques

N = 5000

x = np.arange(1, N+1)
y = np.empty(x.shape)

for i in range(N):
    y[i] = collatz(i+1)

plt.scatter(x,y, s=2)
plt.title('Nombre d\'itérations selon l\'entier initial')
plt.xlabel("Entier initial")
plt.ylabel("Nombre d'itérations")
plt.grid(True)
plt.savefig('collatz.png')
plt.show()

# Fréquence d'itération

plt.hist(y, 25)
plt.title("Fréquence du nombre d'itération")
plt.xlabel("Nombre d'itéraions")
plt.ylabel("Fréquence")
plt.savefig('collatz_frq.png')
plt.show()


#Correction
pytest.main(['-q', '--tb=long', 'collatz_corr.py'])