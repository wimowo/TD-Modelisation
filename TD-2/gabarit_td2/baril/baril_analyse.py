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
    rc = 0      # rayon du cylindre
    rv = 0      # rayon de la vanne
    gamma = 0   # Coefficient de correction
    g = 0       # accélération gravitationnelle


#%% Mesures expérimentales


#%% Appel de la fonction diff1



#%% Appel de la fonction diff2



#%% Calcul de la vitesse théorique



#%% Calcul de l'accélération théorique


#%% Erreur commise sur la vitesse



#%% Erreur commise sur l'accélération



#%% Correction
pytest.main(['-q', '--tb=long', 'baril_corr.py'])
