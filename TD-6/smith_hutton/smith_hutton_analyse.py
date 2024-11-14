# Importation des modules
import numpy as np
import matplotlib.pyplot as plt
import smith_hutton_corr
import pytest

try:
    from smith_hutton_fct import *
except:
    pass

# ------------------------------------------------------------------------------
# Code principal pour l'analyse des résultats
# Il faudra faire appel aux fonctions programmées dans smith_hutton_fct.py afin
# de résoudre le problème de Smith Hutton selon différents nombres de Péclet.
# Ensuite, les solutions devront être affichées sur des figures pour l'analyse.
# ------------------------------------------------------------------------------

# Position et solutions de référence
x_p = np.array([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
s_p10 = np.array([1.989, 1.402, 1.146, 0.946, 0.775, 0.621, 0.480, 0.349, 0.227, 0.111, 0.000])
s_p100 = np.array([2.000, 1.940, 1.836, 1.627, 1.288, 0.869, 0.480, 0.209, 0.070, 0.017, 0.000])
s_p1000 = np.array([2.000, 2.000, 2.000, 1.985, 1.841, 0.951, 0.154, 0.001, 0.000, 0.000, 0.000])

# Paramètres
X = [-1, 1]
Y = [0, 1]

nx = 41
ny = 41

alpha = 10
Pe = [10, 100, 1000]

# Résolution

A, b = mdf_assemblage(X, Y, nx, ny, Pe[0], alpha)
c10 = np.linalg.solve(A, b)

A, b = mdf_assemblage(X, Y, nx, ny, Pe[1], alpha)
c100 = np.linalg.solve(A, b)

A, b = mdf_assemblage(X, Y, nx, ny, Pe[2], alpha)
c1000 = np.linalg.solve(A, b)


# Graphiques (utilisez les lignes suivantes pour générer la figure demandée)
c10_reshaped = c10.reshape(nx,ny).transpose()
c100_reshaped = c100.reshape(nx,ny).transpose()
c1000_reshaped = c1000.reshape(nx,ny).transpose()

x = np.linspace(X[0], X[1], nx)
y = np.linspace(Y[0], Y[1], ny)

fig, ax = plt.subplots(nrows=3, ncols=1)

fig1 = ax[0].pcolormesh(x,y, c10_reshaped)
plt.colorbar(fig1, ax=ax[0])

fig2 = ax[1].pcolormesh(x,y, c100_reshaped)
plt.colorbar(fig2, ax=ax[1])

fig3 = ax[2].pcolormesh(x,y, c1000_reshaped)
plt.colorbar(fig3, ax=ax[2])

plt.show()

# plt.plot(x_p, s_p10)
# plt.plot(x_p, s_p100)
# plt.plot(x_p, s_p1000)

# plt.show()


nx = 5
ny = 5
X = [-1, 1]
Y = [0, 2]

A, b = mdf_assemblage(X, Y, nx, ny, 1, 2)
c = np.linalg.solve(A, b)
print(c)
c = c.reshape(nx, ny).transpose()
x, y = position(X, Y, nx, ny)

fig, ax = plt.subplots(nrows=2, ncols=1)

fig1 = ax[0].pcolormesh(x[0], y.T[0], c)
plt.colorbar(fig1, ax=ax[0])

c_cor = np.array([0.035972, 0.035972, 0.035972, 0.035972, 0.035972,
                  0.035972, 0.078889, 0.217751, 0.519088, 1.000000,
                  0.035972, 0.142702, 0.357701, 0.823647, 1.964028,
                  0.035972, 0.156310, 0.275657, 0.431998, 0.484111,
                  0.035972, 0.035972, 0.035972, 0.035972, 0.035972])
c_cor = c_cor.reshape(nx, ny).transpose()

fig2 = ax[1].pcolormesh(x[0], y.T[0], c_cor)
plt.colorbar(fig2, ax=ax[1])

plt.show()

# %% Correction
pytest.main(['-q', '--tb=long', '--disable-warnings', 'smith_hutton_corr.py'])
