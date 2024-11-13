# Importation des modules
import numpy as np
import matplotlib.pyplot as plt
import pytest
import time
import conduite_corr
try:
    from conduite_fct import *
except:
    pass

#------------------------------------------------------------------------------
# Code principal pour l'analyse des résultats
# Il faudra faire appel aux fonctions programmées dans conduite_fct.py afin de
# calculer la température dans la conduite selon le rayon et de comparer les
# résultats pour plusieurs matériaux. Des graphiques devront être générés pour
# visualiser les résultats.
#------------------------------------------------------------------------------

# Assignation des paramètres
# ATTENTION! Ne pas changer le nom des attributs, seulement les valeurs
class parametres():
    Tr = 70              # Température à l'intérieur de la conduite
    Te = 25              # Température ambiante autour de la conduite
    k = 1.3              # [W*m^-1*K^-1] Conductivité thermique
    h = 12               # [W*m^-2*K^-1] Coefficient de convection thermique
    Re = 4              # [m] Rayon externe
    Ri = 2              # [m] Rayon interne
    n = 5               # [-] Nombre de noeuds
    dr = (Re-Ri)/(n-1)  # [-] Pas en espace
prm = parametres()

# Coefficients de conductivité themique
k = [1.3,50,200]

# Méthode de différences finies
prm.k = k[0]
r1,T1 = mdf(prm)
prm.k = k[1]
r2,T2 = mdf(prm)
prm.k = k[2]
r3,T3 = mdf(prm)

# Graphique
plt.style.use('dark_background')
plt.plot(r1,T3, label='Aluminium, k = 200')
plt.plot(r1,T2, label='Acier, k = 50')
plt.plot(r1,T1, label='Béton, k = 1.3')
plt.xlabel('Rayon [m]')
plt.ylabel('Température [°C]')
plt.title('Profils de température en fonction du rayon de la conduite pour différents matériaux')
plt.yticks(np.arange(20,75,5))
plt.grid()
plt.legend()
plt.savefig('plots_rayon_profils.png',dpi=300)
plt.show()

# Correction
pytest.main(['-q', '--tb=long', 'conduite_corr.py'])
