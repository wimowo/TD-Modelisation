# Importation des modules
import numpy as np
import matplotlib.pyplot as plt
import pytest
import lorenz_corr
try:
    from lorenz_fct import *
except:
    pass

#------------------------------------------------------------------------------
# Code principal pour l'analyse des résultats
# Il faudra faire appel aux fonctions programmées dans lorenz_fct.py afin de
# générer les graphiques représentant un attracteur de Lorenz selon deux
# ensembles de conditions initiales et de les comparer.
#------------------------------------------------------------------------------

# Assignation des paramètres
# ATTENTION! Ne pas changer le nom des attributs
class parametres():
    o = 10      # sigma
    b = 8/3      # beta
    p = 28      # rho
prm = parametres()

# Conditions initiales
ci = [9,5,3]
dt = 0.001
tf = 0.004

# Appel de la fonction rk4
x = rk4(ci,dt,tf,prm)

# Graphiques
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.plot(x, y, z)


plt.show()

# Correction
pytest.main(['-q', '--tb=long', 'lorenz_corr.py'])
