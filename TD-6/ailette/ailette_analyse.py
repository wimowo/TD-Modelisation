# Importation des modules
import numpy as np
import matplotlib.pyplot as plt
import pytest
import ailette_corr

try:
    from ailette_fct import *
except:
    pass


# ------------------------------------------------------------------------------
# Code principal pour l'analyse des résultats
# Il faudra faire appel aux fonctions programmées dans ailette_fct.py afin de
# modéliser les pertes de chaleurs selon différentes combinaisons géométriques.
# Ensuite, il faudra identifier le meilleur rendement.
# ------------------------------------------------------------------------------

# Assignation des paramètres
# ATTENTION! Ne pas changer le nom des attributs
class parametres():
    L = 0.1  # [m] Longueur
    D = 0.0025  # [m] Diamètre
    k = 45  # [W/m*K] Conductivité thermique
    T_a = 25 + 273  # [K] Température de l'air ambiant
    T_w = 125 + 273  # [K] Température de la paroi
    h = 150  # [W/m^2*K] Coefficient de convection
    N = 1000  # [-] Nombre de points en z


prm = parametres()

# Appel des fonctions pour le calcul du profil de température

R = mdf(prm)

m = np.sqrt(4 * prm.h / (prm.k * prm.D))
y_analytique = (prm.T_w - prm.T_a) * np.cosh(m * (prm.L - R[1])) / np.cosh(m * prm.L) + prm.T_a
# Graphique

plt.style.use('dark_background')
plt.plot(R[1], R[0], label='Solution par différence finie')
plt.plot(R[1], y_analytique, "--y", label="Solution analytique")

plt.xlabel("Position z (m)")
plt.ylabel("Température (K)")
plt.title("Comparaison du profile de température le long de l'ailette")

plt.legend()
plt.savefig("Comparaison_analyse.png", dpi=300)
plt.show()

# Calcul de la dissipation pour chaque géométrie

ref = inte(R[0], R[1], prm)
err = 1

prm.N = 2
while err > 0.01:
    prm.N += 1

    calc = mdf(prm)
    comp = inte(*calc, prm)

    err = np.abs(comp - ref) / ref

print("Nombre de noeuds:", prm.N)
# Graphique
L = [0.005, 0.0075, 0.01, 0.0125, 0.015]
D = np.linspace(0.001, 0.02, 200)

Q = np.empty((len(D),1))
for l in L:
    prm.L = l
    for i in range(len(D)):
        prm.D = D[i]
        Q[i] = inte(*mdf(prm),prm)
        if abs(Q[i] - 10) < 1e-1:
            print(prm.L, prm.D)

    plt.plot(D, Q, label=f'L = {prm.L} m')
    plt.legend()


plt.xlabel("Diametre D (m)")
plt.ylabel("Dissipation de chaleur q (W)")
plt.title("Evolution de la dissipation selon le diametre et la longeur de l'ailette")
plt.hlines(y=10, xmin=0, xmax=D[-1], linestyles='dashed')
plt.savefig("Comparaison_dim.png", dpi=300)
plt.show()

L = np.array([0.0125, 0.015])
d = np.array([0.018, 0.016])
v = L * d**2 * np.pi/4
print(v)
# Correction
pytest.main(['-q', '--tb=long', 'ailette_corr.py'])
