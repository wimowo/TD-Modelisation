# Importation des modules
import numpy as np
import pytest
import jetpack_corr
try:
    from jetpack_fct import *
except:
    pass

#------------------------------------------------------------------------------
# Code principal pour l'analyse des résultats
# Il faudra faire appel aux fonctions programmées dans jetpack_fct.py afin
# de calculer les vitesses d'entrée et de sorties de l'eau ainsi que l'angle
# d'inclinaison afin d'obtenir l'équilibre désiré.
#------------------------------------------------------------------------------

# Données du problème
class parametres():
    g = 9.81       # Accélération gravitationnelle [m/s^2]
    rho = 1000     # Masse volumique [kg/m^3]
    D_e = 0.2     # Diamètre du boyau [m]
    D_s = 0.05     # Diamètre des propulseurs [m]
    m = 70      # Masse [kg]
    F = 200       # Force du vent [N]
prm = parametres()

# Appel de la fonction



# Correction
pytest.main(['-q', '--tb=long', 'jetpack_corr.py'])
