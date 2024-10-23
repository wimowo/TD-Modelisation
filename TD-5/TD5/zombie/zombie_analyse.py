# Importation des modules
import numpy as np
import matplotlib.pyplot as plt
import pytest
import zombie_corr

try:
    from zombie_fct import *
except:
    pass


# ------------------------------------------------------------------------------
# Code principal pour l'analyse des résultats
# Il faudra faire appel aux fonctions programmées dans zombie_fct.py afin d'évaluer
# l'évolution des populations humaines et zombies à travers les années suivant
# une invasion de zombies. Un graphique sera généré afin de visualiser cette
# évolution temporelle.
# ------------------------------------------------------------------------------

# Assignation des paramètres
# Attention! Ne pas changer le nom des attributs
class parametres():
    e = 0.0001  # Taux de résurrection en zombie (zeta)
    b = 0.0095  # Taux de transformation en zombie (beta)
    a = 0.005  # Taux de mort de zombie (alpha)
    d = 0.0001  # Taux de mort naturelle (delta)
    p = 0.0001  # Taux de naissance (pi)


prm = parametres()

# Résolution des EDO

# Conditions initiales
ci = np.array([500., 0., 0.])

# Euler implicite
sim = euler_implicite(ci, 0.01, 20, 1e-7, prm)
print(sim[0])
# Graphique
plt.plot(sim[1], sim[0])
plt.xlabel("Années")
plt.ylabel("Population")
plt.title("Évolution de l'invasion zombie")
plt.legend(("Humains","Zombies","Morts"))

plt.savefig("zombie_analyse.png", dpi=300)

plt.show()

# Correction
pytest.main(['-q', '--tb=long', 'zombie_corr.py'])
