# Importation des modules
import matplotlib.pyplot as plt
import numpy as np
import pytest

try:
    from montecarlo_fct import *
except:
    pass

import montecarlo_corr

#-----------------------------------------------------------------------------
# Code principal pour l'analyse des résultats
# Il faudra appeler les fonctions du fichier montecarlo_fct.py afin de créer
# des points aléatoires pour ensuite calculer l'erreur par rapport à la valeur
# exacte de pi.
# Ensuite, il faudra générer un graphique pour visualiser l'erreur selon
# le nombre de points utilisés. Attention de bien générer un nouvel ensemble
# de points à chaque calcul de pi.
#-----------------------------------------------------------------------------


# Code principal
## Génération de points et calcul de pi
N = 100000

pts = genXY(N)
approx_pi = monte_carlo(*pts)
print(approx_pi)

## Calcul de l'erreur et graphique


# Créer le graphique

# Créer 100 nombre de point entre 100 et 10 000
PI = np.pi
x = np.arange(100, 10001, 5)
y = np.empty(x.shape)

for i in range(len(x)):
    xy = genXY(int(x[i]))
    err = abs(monte_carlo(*xy)/PI-1)*100
    y[i] = err

plt.plot(x, y, label='Erreur absolue')

plt.legend()
plt.xlabel('Nombre de points')
plt.ylabel('Erreur absolue (%)')
plt.title("Évolution de l'erreur absolue selon le nombre de point")
plt.savefig('montecarlo_analyse.png')

plt.show()

# Correction
pytest.main(['-q', '--tb=long', 'montecarlo_corr.py'])
