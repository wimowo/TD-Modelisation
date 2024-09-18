# Importation des modules
import numpy as np
import pytest
try:
    from decollage_fct import *
except:
    pass

#-----------------------------------------------------------------------------
# Code principale pour l'analyse des résultats
# Il faudra faire appel aux fonctions programmées dans le fichier decollage_fct.py
# afin de calculer l'accélération de l'avion, la force de poussée développée
# et finalement le travail fourni par les moteurs.
#-----------------------------------------------------------------------------

#%% Données du problème
class constantes():
    rho = 1.341         # Densité de l'air [kg/m^3]
    S = 580           # Surface de référence [m^2]
    C = 0.027           # Coefficient de friction [-]
    m = 250*1000           # Masse de l'avion [kg]

t = np.arange(0,33,2)
v = np.array([0,4,17,33,50,67,83,100,117,133,150,167,183,200,217,233,250])/3.6
cst = constantes()



#%% Accélération en fonction du temps
dt = 2
a = acc(v, dt)
# print('Acceleration :',a)
#%% Force de poussée de l'avion
force = force_poussee(v, a, cst)
travail = force_poussee(v, a, cst)* v

#%% Travail fourni par les moteurs
print('Le travail est??? fois 32 secondes??? :',trapeze(t,force_poussee(v, a, cst)* v) *1e-06)
print('Le travail est??? fois 32 secondes??? :',simpson(t,force_poussee(v, a, cst)* v)*1e-06)

# Affichage (optionnel)
# print("Les moteurs doivent fournir un travail de %.2f MJ." % (???))

#%% Correction
pytest.main(['-q', '--tb=long', 'decollage_corr.py'])
