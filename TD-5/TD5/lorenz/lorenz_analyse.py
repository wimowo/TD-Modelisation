# Importation des modules
import numpy as np
import matplotlib.pyplot as plt
import pytest
from mpl_toolkits.mplot3d.art3d import Line3DCollection
import lorenz_corr
from mpl_toolkits import mplot3d

try:
    from lorenz_fct import *
except:
    pass


# ------------------------------------------------------------------------------
# Code principal pour l'analyse des résultats
# Il faudra faire appel aux fonctions programmées dans lorenz_fct.py afin de
# générer les graphiques représentant un attracteur de Lorenz selon deux
# ensembles de conditions initiales et de les comparer.
# ------------------------------------------------------------------------------

# Assignation des paramètres
# ATTENTION! Ne pas changer le nom des attributs
class parametres():
    o = 10  # sigma
    b = 8 / 3  # beta
    p = 28  # rho


prm = parametres()

# Conditions initiales
ci = [10, 10, 20]
dt = 0.001
tf = 30

# Appel de la fonction rk4

x = rk4(ci, dt, tf, prm)

# Graphiques
fig = plt.figure()
plt.style.use('dark_background')
ax = fig.add_subplot(111, projection='3d')
ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
ax.zaxis.pane.fill = False

ax.plot(x[0][:, 0], x[0][:, 1], x[0][:, 2], "#3912b8", label='Conditions initiales',linewidth=1.5)

ci = [10.0001, 10.0002, 20.0003]
x = rk4(ci, dt, tf, prm)

ax.plot(x[0][:, 0], x[0][:, 1], x[0][:, 2], "#b81273",label='Conditions initiales modifiées', linewidth=1.5)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.legend()
ax.set_title("Graphique 3D de l'attracteur de Lorenz")

plt.savefig('Lorenz.png', dpi=300)
plt.show()
# Correction
pytest.main(['-q', '--tb=long', 'lorenz_corr.py'])
