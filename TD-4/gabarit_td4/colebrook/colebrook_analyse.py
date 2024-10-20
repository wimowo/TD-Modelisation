# Importation des modules
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
import pytest
try:
    from colebrook_fct import *
except:
    pass

#------------------------------------------------------------------------------
# Code principal pour l'analyse des résultats
# Il faudra faire appel aux fonctions programmées dans colebrook_fct.py afin
# de visualiser graphiquement l'intersection de la formule de Colebrook et
# ensuite trouver numériquement la valeur de lambda à l'aide de la bissection.
#------------------------------------------------------------------------------

# Données du problème
class constantes():
    # IMPORTANT: Ne pas changer le nom des variables (attributes) dans la class
    # Seulement les valeurs doivent être changées
    Re = 13743      # Nombre de Reynolds [-]
    k = 0.003375       # Rugosité [m]
    D = 0.3       # Diamètre de la conduite [m]

cst = constantes()

#%% Affichage du graphique


l = np.linspace(0.01, 1, 100) 
y = f(l,cst)

plt.plot(l, y)
plt.axhline(y=0, color='k')
plt.grid()
plt.xlabel('Coefficient de friction λ')
plt.ylabel('f(λ)')
plt.xticks(np.linspace(0, 1, 11))
plt.title("Intersection de la fonction f(λ) = 0")
plt.savefig('colebrook_fct.png', dpi=300)
plt.show()


#%% Appel de la fonction bissection()
tol = 10^-5
N = 1000
print(bissection(0.01, 0.2, tol, N, cst))

#%% Appel de la fonction scipy (Supprimez les symboles de commentaire après avoir défini f)
#l_scipy = fsolve(f,0.001,args=(cst))
#print("Le coefficient de friction trouvé par scipy est %f" % l_scipy)


# Correction
pytest.main(['-q', '--tb=long', 'colebrook_corr.py'])
