# Importation des modules
import numpy as np
import pytest
try:
    from baril_fct import *
except:
    pass

import baril_corr

#-----------------------------------------------------------------------------
# Code principal de l'analyse des résultats
# Il faudra faire appel aux fonctions programmées afin de trouver les dérivées
# premières et secondes et les comparer aux valeur théoriques.
# La class constantes() doit être remplie avec les valeurs de l'énoncé. Les
# noms des variables dans la class ne doivent pas être changé.
#-----------------------------------------------------------------------------

class constantes():
    rc = 1      # rayon du cylindre
    rv = 0.1      # rayon de la vanne
    gamma = 0.6   # Coefficient de correction
    g = 9.81       # accélération gravitationnelle
    
cst = constantes()

#%% Mesures expérimentales

h = np.array([0.6350,0.5336,0.4410,0.3572,0.2822], dtype=float)
dt=5

#%% Appel de la fonction diff1

print('diff1:', diff1(h, dt))

#%% Appel de la fonction diff2

print('diff2: ', diff2(h, dt))

#%% Calcul de la vitesse théorique

print('vitesse :',vitesse(h, cst))

#%% Calcul de l'accélération théorique

#%% Erreur commise sur la vitesse

somme = 0
i=0
while i < len(h):
    somme += abs((vitesse(h, cst)[i] - diff1(h,dt)[i])/vitesse(h, cst)[i])
    i+=1
erreur_vitesse = (100/len(h)) * somme

print('erreur vitesse :',erreur_vitesse)



#%% Erreur commise sur l'accélération

somme = 0
i=0
while i < len(h):
    somme += abs((acceleration(cst)-diff2(h,dt)[i])/acceleration(cst))
    i+=1
erreur_accel = (100/len(h)) * somme

print('Erreur acceleration :',erreur_accel)


#%% Correction
pytest.main(['-q', '--tb=long', 'baril_corr.py'])
