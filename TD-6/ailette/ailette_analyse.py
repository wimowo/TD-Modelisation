# Importation des modules
import numpy as np
import matplotlib.pyplot as plt
import pytest
import ailette_corr

try:
    from ailette_fct import *
except:
    pass


# ------------------------------------------------------------------------------
# Code principal pour l'analyse des résultats
# Il faudra faire appel aux fonctions programmées dans ailette_fct.py afin de
# modéliser les pertes de chaleurs selon différentes combinaisons géométriques.
# Ensuite, il faudra identifier le meilleur rendement.
# ------------------------------------------------------------------------------

# Assignation des paramètres
# ATTENTION! Ne pas changer le nom des attributs
class parametres():
    L = 0.1  # [m] Longueur
    D = 0.0025  # [m] Diamètre
    k = 45  # [W/m*K] Conductivité thermique
    T_a = 25 + 273  # [K] Température de l'air ambiant
    T_w = 125 + 273  # [K] Température de la paroi
    h = 150  # [W/m^2*K] Coefficient de convection
    N = 1000  # [-] Nombre de points en z


prm = parametres()

# Appel des fonctions pour le calcul du profil de température

R = mdf(prm)

m = np.sqrt(4 * prm.h / (prm.k * prm.D))
y_analytique = (prm.T_w - prm.T_a) * np.cosh(m * (prm.L - R[1])) / np.cosh(m * prm.L) + prm.T_a
# Graphique

plt.plot(R[1],R[0], label='Solution par différence finie')
plt.plot(R[1],y_analytique, "--y", label="Solution analytique")

plt.legend()
plt.show()

# Calcul de la dissipation pour chaque géométrie


# Graphique


# Correction
pytest.main(['-q', '--tb=long', 'ailette_corr.py'])
