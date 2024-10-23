# Importation des modules
import numpy as np
import matplotlib.pyplot as plt
import pytest
import oscillateur_corr
try:
    from oscillateur_fct import *
except:
    pass

#------------------------------------------------------------------------------
# Code principal pour l'analyse des résultats
# Il faudra faire appel aux fonctions programmées dans oscillateur_fct.py afin
# d'évaluer la solution d'un système d'équations différentielles ordinaires
# avec différentes méthodes numériques et comparer les résultats
# graphiquement.
#------------------------------------------------------------------------------

# Assignation des paramètres et conditions initiales
# ATTENTION! Ne pas changer le nom des attributs
class parametres():
    k = 2       # Constante de rappel du ressort [kg]
    m = 0.05       # Masse accroché au ressort [N/m]
prm = parametres()

dt = 0.01
tf = 3.0
ci = np.array([2.0, 0.0])
# Euler explicite
E = euler_explicite(ci, dt, tf, prm)
ener_E = energie(E[0][:,0], E[0][:,1], prm)

# Runge-Kutta 2dt = 0.01
ci = np.array([2.0, 0.0])
RK = rk2(ci, dt, tf, prm)
ener_RK = energie(RK[0][:,0], RK[0][:,1], prm)

# Verletdt = 0.01
ci = np.array([2.0, 0.0])
V = verlet(ci, dt, tf, prm)
ener_V = energie(V[0][:,0], V[0][:,1], prm)

# Solution analytique
t = np.linspace(0, round((tf*100000-dt*100000))/100000,round((tf*100000)/(dt*100000)))
y_a = 2*np.cos(np.sqrt(prm.k/prm.m)*t)

# Graphiques

fig, axs = plt.subplots(3, 2, figsize=(12, 10))
axs[0, 0].plot(E[1], E[0][:,0], 'r-', label='Euler')
axs[0, 0].plot(E[1], y_a, 'b-', label='Analytique')
axs[0, 0].set_title('Graphique 1: Euler - Position de la masse en fonction du temps')
axs[0, 0].set_xlabel('Temps [s]') 
axs[0, 0].set_ylabel('Position de la masse [m]')  
axs[0, 0].legend()

axs[0, 1].plot(E[1], ener_E)
axs[0, 1].set_title('Graphique 2: Euler - Energie du système en fonction du temps')
axs[0, 1].set_xlabel('Temps [s]') 
axs[0, 1].set_ylabel('Énergie [J]') 

axs[1, 0].plot(RK[1], RK[0][:,0], 'r-', label='Runge Kutta')
axs[1, 0].plot(RK[1], y_a, 'b-', label='Analytique', linestyle='--')
axs[1, 0].set_title('Graphique 3: Runge kutta - Position de la masse en fonction du temps')
axs[1, 0].set_xlabel('Temps [s]') 
axs[1, 0].set_ylabel('Position de la masse [m]')  
axs[1, 0].legend()

axs[1, 1].plot(RK[1], ener_RK)
axs[1, 1].set_title('Graphique 4: Runge kutta - Energie du système en fonction du temps')
axs[1, 1].set_xlabel('Temps [s]') 
axs[1, 1].set_ylabel('Énergie [J]') 

axs[2, 0].plot(V[1], V[0][:,0], 'r-', label='Verlet')
axs[2, 0].plot(V[1], y_a, 'b-', label='Analytique', linestyle='--')
axs[2, 0].set_title('Graphique 5: Verlet - Position de la masse en fonction du temps')
axs[2, 0].set_xlabel('Temps [s]') 
axs[2, 0].set_ylabel('Position de la masse [m]')  
axs[2, 0].legend()

axs[2, 1].plot(V[1], ener_V)
axs[2, 1].set_title('Graphique 6: Verlet - Energie du système en fonction du temps')
axs[2, 1].set_xlabel('Temps [s]') 
axs[2, 1].set_ylabel('Énergie [J]') 

plt.tight_layout()
plt.show()

# Correction
pytest.main(['-q', '--tb=long', 'oscillateur_corr.py'])
