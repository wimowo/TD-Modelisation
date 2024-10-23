# Importation des modules
import numpy as np


def residu(y, yi, prm, dt):
    """Fonction calculant le résidu de la dynamique d'une invasion de zombie
    
    Entrées:
        - y : Variables dépendantes
            - [0] : S, humains susceptibles de devenir zombies
            - [1] : Z, zombies
            - [2] : R, retirés du bassin
        - yi : Estimés initiaux (même ordre que y)
        - prm : Objet class parametres()
            - e : taux de résurrection en zombie (zeta)
            - b : taux de transformation en zombie (beta)
            - a : taux de mort de zombie (alpha)
            - d : taux de mort naturelle (delta)
            - p : taux de naissance (pi)
        - dt : Pas de temps
    
    Sortie:
        - Vecteur (array) contenant les valeurs numériques du résidu
    """
    r = np.empty((3,))
    r[0] = yi[0] - y[0] + dt * (prm.p - prm.b * y[0] * y[1] - prm.d * y[0])
    r[1] = yi[1] - y[1] + dt * (prm.b * y[0] * y[1] + prm.e * y[2] - prm.a * y[0] * y[1])
    r[2] = yi[2] - y[2] + dt * (prm.d * y[0] + prm.a * y[0] * y[1] - prm.e * y[2])

    return r


def jacobien(y, prm, dt):
    """Fonction calculant le jacobien de la dynamique d'une invasion de zombie
    
    Entrées:
        - y : Variables dépendantes
            - [0] : S, humains susceptibles de devenir zombies
            - [1] : Z, zombies
            - [2] : R, retirés du bassin
        - prm : Objet class parametres()
            - e : taux de résurrection en zombie (zeta)
            - b : taux de transformation en zombie (beta)
            - a : taux de mort de zombie (alpha)
            - d : taux de mort naturelle (delta)
            - p : taux de naissance (pi)
        - dt : Pas de temps
    
    Sortie:
        - Matrice (array) contenant les valeurs numériques du jacobien
    """

    J = np.array([[-1 + dt * (- prm.b * y[1] - prm.d), dt * (- prm.b * y[0]), 0],
                  [dt * (prm.b * y[1] - prm.a * y[1]), -1 + dt * (prm.b * y[0] - prm.a * y[0]), dt * prm.e],
                  [dt * (prm.d + prm.a * y[1]), dt * (prm.a * y[0]), -1 + dt * (- prm.e)]])

    return J


def euler_implicite(ci, dt, tf, tol, prm):
    """Fonction calculant le résidu de la dynamique d'une invasion de zombie
    
    Entrées:
        - ci : Conditions initiales
            - [0] : S, humains susceptibles de devenir zombies
            - [1] : Z, zombies
            - [2] : R, retirés du bassin
        - dt : Pas de temps
        - tf : Temps final de simulation
        - tol : Critère d'arrêt
        - prm : Objet class parametres()
            - e : taux de résurrection en zombie (zeta)
            - b : taux de transformation en zombie (beta)
            - a : taux de mort de zombie (alpha)
            - d : taux de mort naturelle (delta)
            - p : taux de naissance (pi)
    
    Sorties (dans l'ordre énuméré ci-bas):
        - Matrice (array de taille (temps, 3)) des solutions dans le temps, incluant les conditions initiales
            - Chaque ligne représente les solutions (S,Z,R) à un temps donné
            - Chaque colonne représente l'évolution d'une variable dans le temps
        - Vecteur (array) du temps de simulation
    """
    t = np.arange(0, tf+dt, dt)
    sol = np.empty((len(t), 3))

    sol[0] = ci
    yi = ci
    y = ci

    for i in range(1, len(t)):
        delta = 1
        while  np.linalg.norm(delta) > tol:
            r = residu(y,yi,prm,dt)
            j = jacobien(y, prm, dt)
            delta = -np.linalg.solve(j, r)
            y = y + delta

        sol[i] = y
        yi = y

    return sol, t
