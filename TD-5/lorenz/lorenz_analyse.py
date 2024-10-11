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
ci = [10,10,20]
dt = 0.001
tf = 30

# Appel de la fonction rk4

x = rk4(ci,dt,tf,prm)
print(x)
#Graphiques
fig = plt.figure()
ax = fig.add_subplot(111,projection='3d')
ax.plot(x[0][:,0], x[0][:,1], x[0][:,2])
ax.set_xlabel('Axe X')
ax.set_ylabel('Axe Y')
ax.set_zlabel('Axe Z')
ax.set_title("Graphique 3D de l'attracteur de Lorenz")

ci = [10.0005,10.0005,20.0005]
x = rk4(ci,dt,tf,prm)
#Graphiques
fig2 = plt.figure()
ax = fig2.add_subplot(111,projection='3d')
ax.plot(x[0][:,0], x[0][:,1], x[0][:,2])
ax.set_xlabel('Axe X')
ax.set_ylabel('Axe Y')
ax.set_zlabel('Axe Z')
ax.set_title("Graphique 3D de l'attracteur de Lorenz\n C.I. légèrement modifiées (0.0005)")

# Correction
pytest.main(['-q', '--tb=long', 'lorenz_corr.py'])
