# Importation des modules
import numpy as np
import matplotlib.pyplot as plt
from scipy.misc import derivative
import pytest

try:
    from erreur_fct import *
except:
    pass

import erreur_corr

# -----------------------------------------------------------------------------
# Code principal pour l'analyse des résultats
# Il faudra faire appel aux fonctions programmées dans erreur_fct.py afin de
# déterminer les dérivées numériques selon des schémas aux ordres différents.
# Un graphique comparant les valeurs des dérivées sera produit, ainsi qu'un
# graphique comparant les erreurs pour chaque schéma.
# -----------------------------------------------------------------------------

# %% Dérivée première, schéma d'ordre 1

x = 0.5
h = 0.1

print("Différentiation arrière d'ordre 1:", diff_arriere_ordre1(x, h))

# Affichage


# %% Dérivée première, schéma d'ordre 2

print("Différentiation centrée d'ordre 2:", diff_centree_ordre2(x, h))

# Affichage


# %% Graphique de g'(x) selon les 2 méthodes
h = 0.1
x_1 = 0.1
x_2 = np.pi / 2

x = np.linspace(x_1, x_2, 100)
y_1 = diff_arriere_ordre1(x, h)
y_2 = diff_centree_ordre2(x, h)

plt.plot(x, y_1, label='Arrière ordre 1')
plt.plot(x, y_2, label='Centrée ordre 2')
plt.xlabel("x")
plt.ylabel("g'(x)")
plt.title('Comparaison des méthodes de différentiation numériques')
plt.legend()
plt.show()

# %% Analyse de l'erreur
x = 0.5

dg_exact = 0.157134840263677

h = np.logspace(-10, -1, 200, base=10)
err_1 = abs(diff_arriere_ordre1(x, h)-dg_exact)
err_2 = abs(diff_centree_ordre2(x, h)-dg_exact)
err_3 = abs(derivative(g, x, dx=h)-dg_exact)

# %% Graphique des erreurs

plt.loglog(h, err_1, label="Arrière ordre 1")
plt.loglog(h, err_2, label="Centrée ordre 2")
plt.loglog(h, err_3, label="Scipy derivative", linestyle="--")
plt.legend()
plt.xlabel("Pas de différentiation Δx")
plt.ylabel("Erreur")
plt.title("Comparaison de l'évolution de l'erreur")
plt.show()

# %% Correction
pytest.main(['-q', '--tb=long', 'erreur_corr.py'])
