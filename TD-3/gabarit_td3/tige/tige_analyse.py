# Importation des modules
import numpy as np
import matplotlib.pyplot as plt
import pytest

try:
    from tige_fct import *
except:
    pass

#-----------------------------------------------------------------------------
# Code principal pour l'analyse des résultats
# Il faudra faire appel aux fonctions programmées dans tige_fct.py afin de
# calculer l'intégrale d'une fonction selon la quadrature de Gauss. Ensuite,
# il faudra évaluer l'erreur par rapport à la valeur analytique et afficher
# un graphique de cette erreur selon le nombre de points.
#-----------------------------------------------------------------------------

#%% Calcul de l'intégrale numérique
n = np.array([1,2,3,4,5])
integrale = np.empty(len(n))

for i in range(len(n)):
    integrale[i] = gauss(0, np.pi/2, n[i])
print(np.stack((n,integrale)))
# Affichage en tableau


#%% Calcul de l'erreur commise
t = 0.99888139
erreur = np.abs(integrale - t)

# Affichage du graphique
plt.plot(n, erreur)

plt.xlabel("Nombre de point")
plt.ylabel("Erreur")
plt.title("Évolution de l'erreur en fonction du nombre de point")
plt.xticks(np.arange(0,6,1))
plt.grid()


plt.show()

#%% Correction
pytest.main(['-q', '--tb=long', 'tige_corr.py'])
