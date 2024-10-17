# Importation de modules
import numpy as np


def fonc(y,prm):
    """Fonction calculant le système d'équations

    Entrées:
        - y : Variables dépendantes
            - [0] : Position x
            - [1] : Vitesse v
        - prm : objet class parametres
            - k : Constante de rappel du ressort [N/m]
            - m : Masse accroché au ressort [kg]

    Sortie:
        - Vecteur (array) composé des valeurs numériques des équations différentielles
    """

    dxdt = y[1]
    dvdt = -prm.k*y[0]/prm.m

    return np.array([dxdt, dvdt])

def euler_explicite(ci,dt,tf,prm):
    """Fonction de résolution par la méthode d'Euler explicite

    Entrées:
        - ci : Conditions initiales
            - [0] : x0
            - [1] : v0
        - dt : Pas de temps
        - tf : Temps de simulation
        - prm : objet class parametres
            - k : Constante de rappel du ressort [N/m]
            - m : Masse accroché au ressort [kg]

    Sorties (dans l'ordre énuméré ci-bas):
        - Matrice (array) des solutions en fonction du temps
            - Chaque ligne représente une solution au système à un temps donnée
            - Chaque colonne représente les solutions dans le temps d'une variable
        - Vecteur (array) du temps de simulation
    """
    temps = np.linspace(0, round((tf*100000-dt*100000))/100000,round((tf*100000)/(dt*100000)))
    matrice = np.zeros((len(temps), len(ci)))
    i=0
    while i <= len(temps)-1:
        
        f = fonc(ci,prm) 
        ci += f *dt
        print(ci)
        matrice[i] = ci
        i+=1
    return matrice, temps

def rk2(ci,dt,tf,prm):
    """Fonction de résolution par la méthode de Runge Kutta d'ordre 2

    Entrées:
        - ci : Conditions initiales
            - [0] : x0
            - [1] : v0
        - dt : Pas de temps
        - tf : Temps de simulation
        - prm : objet class parametres
            - k : Constante de rappel du ressort [N/m]
            - m : Masse accroché au ressort [kg]

    Sorties (dans l'ordre énuméré ci-bas):
        - Matrice (array) des solutions en fonction du temps
            - Chaque ligne représente une solution à un temps donnée
            - Chaque colonne représente les solutions dans le temps d'une variable
        - Vecteur (array) du temps de simulation
    """

    temps = np.linspace(0, round((tf*100000-dt*100000))/100000,round((tf*100000)/(dt*100000)))
    matrice = np.zeros((len(temps), len(ci)))

    i = 0
    while i <= len(temps)-1:
        k1 = dt * fonc(ci, prm)
        k2 = dt * fonc((ci+k1/2),prm)
        ci = ci + k2
        matrice[i] = ci
        i+=1
    
    return matrice, temps

def verlet(ci,dt,tf,prm):
    """Fonction de résolution par la méthode de Verlet

    Entrées:
        - ci : Conditions initiales
            - [0] : x0
            - [1] : v0
        - dt : Pas de temps
        - tf : Temps de simulation
        - prm : objet class parametres
            - k : Constante de rappel du ressort [N/m]
            - m : Masse accroché au ressort [kg]

    Sorties (dans l'ordre énuméré ci-bas):
        - Matrice (array) des solutions en fonction du temps
            - Chaque ligne représente une solution à un temps donnée
            - Chaque colonne représente les solutions dans le temps d'une variable
        - Vecteur (array) du temps de simulation
    """

    temps = np.linspace(0, round((tf*100000-dt*100000))/100000,round((tf*100000)/(dt*100000)))
    matrice = np.zeros((len(temps), len(ci)))
    i = 0
    a = -prm.k*ci[0]/prm.m
    while i <= len(temps)-1:
        vt = ci[1] + 0.5*dt*a
        xt1 = ci[0] + dt*vt
        a = -prm.k*xt1/prm.m
        vt1 = vt + 0.5*dt*a
        ci = np.array([xt1,vt1])
        matrice[i] = ci
        i+=1
    
    return matrice, temps

def energie(x,v,prm):
    """Fonction de calcul de l'énergie totale du système

    Entrées:
        - x : Vecteur position
        - v : Vecteur vitesse
        - prm : objet class parametres
            - k : Constante de rappel du ressort [N/m]
            - m : Masse accroché au ressort [kg]

    Sortie:
        - Vecteur (array) composé de l'énergie du système à chaque position
    """
    energie = np.zeros((len(x)))
    for i in range(len(x)):
        energie[i] = 0.5*prm.m*v[i]**2 + 0.5*prm.k*x[i]**2
        

    return energie
