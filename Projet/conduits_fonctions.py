# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 09:25:47 2024

@author: tardi
"""
import numpy as np

"""
Les fonctions suivantes servent a resoudre la perte avec l'equation de Hazen-Williams
"""


def reynolds(q, prm):
    return (4 * prm.rho * np.abs(q)) / (np.pi * prm.mu * prm.D)


def cr(q, prm):
    return (-2 * (2 ** 0.5)) / (3.83 * (reynolds(q, prm) ** 0.105)) * (
        np.log10(prm.e / (3.7 * prm.D) + 1.78 / reynolds(q, prm)))


def resistance(q, prm):
    return prm.L / (944.62 * np.abs(cr(q, prm)) ** 1.8099 * prm.D ** 4.8099)


def perte(q, prm):
    return resistance(q, prm) * np.abs(q) ** prm.n


"""
Les fonctions suivantes servent a resoudre resoudre les inconnus du système
"""


def residu(Q, P, reseau, prm):
    """Calcul du résidu du système d'équation"""

    cond = conduits(reseau)

    nb_points = len(reseau)
    nb_cond = len(cond)

    debits = np.zeros(nb_points)
    pressions = np.zeros(nb_cond)

    q = Q[:nb_points]
    qc = Q[nb_points:]

    for x in reseau:
        for c in cond:
            # verification du sense du débit : point[0] -→ point[1]
            if x in cond[c]:
                if "pression" in reseau[x]:
                    debits[x] -= qc[c]
                else:
                    debits[x] += qc[c]

        debits[x] += q[x]

    for c in range(nb_cond):
        point1 = cond[c][0]
        point2 = cond[c][1]

        p1 = P[point1]
        p2 = P[point2]

        pressions[c] = np.abs(p2 - p1) - perte(qc[c], prm)

    r = np.concatenate((debits, pressions))

    return r


def newton_resolution(reseau, prm, tol=1e-5, n=1000):
    """Resolution du réseau par la methode de Newton-Raphson"""
    N = n

    h = tol
    delta = 1
    n = 0

    nb_points = len(reseau)
    nb_cond = len(conduits(reseau))

    Q, P, inc = initialisation(reseau, prm)

    size = nb_cond + nb_points
    x = np.concatenate((Q, P))
    J = np.empty([size, size])

    sol = np.empty(size)
    x_p = np.empty(size)

    for i in range(size):
        sol[i] = x[inc[i]]

    while np.linalg.norm(delta) > tol and n < N:

        Q = x[: size]
        P = x[size:]

        R = residu(Q, P, reseau, prm)

        for i in range(len(R)):
            x_p = np.copy(x)
            x_p[inc[i]] += h

            Q_p = x_p[0: size]
            P_p = x_p[size:]

            R_p = residu(Q_p, P_p, reseau, prm)
            J[:, i] = (R_p - R) / h

        delta = np.linalg.solve(J, -R)

        sol = sol + delta

        for i in range(size):
            x[inc[i]] = sol[i]
        n = n + 1

    f = Q[:nb_points]
    Q = Q[nb_points:]

    return Q, P, f


def calculation_sim(reseau, prm, tol=1e-5, N=1000):
    """Fonction servant à effectuer la simulation du system et la retourner en trois listes"""
    Q, P, f = newton_resolution(reseau, prm, tol, N)

    nodes_result = {}
    pipes_result = {}

    for p in reseau:
        nodes_result[p] = {"pression": P[p], "debit": f[p]}

    cond = conduits(reseau)
    for c in cond:
        point1 = cond[c][0] + 1
        point2 = cond[c][1] + 1

        pipes_result[c] = {"noeuds": (point1, point2), "debit": Q[c]}

    return nodes_result, pipes_result


def conduits(reseau):
    """Fonction qui renvoie les conduits et les points les connectants"""
    conduit_list = {}
    x = 0
    for n in reseau:
        for voisin in reseau[n]["voisins"]:
            # n1 = max(n, voisin)
            # n2 = min(n, voisin)
            if (voisin, n) not in conduit_list.values():  # Verifie si le conduit existe deja
                conduit_list[x] = (n, voisin)
                x += 1

    return conduit_list


def initialisation(reseau, prm):
    cond = conduits(reseau)

    nb_point = len(reseau)
    nb_cond = len(cond)
    size = nb_point + nb_cond

    Q = np.zeros(size)
    P = np.zeros(nb_point)
    inconnues = []  # Création d'une liste des indices des données inconnues

    pressions_noeud = {}
    debits_noeud = {}

    for noeud, details in reseau.items():
        if "pression" in details:
            pressions_noeud[noeud] = details["pression"]
        if "debit" in details:
            debits_noeud[noeud] = details["debit"]

    for p in range(nb_point):  # Initialization des débits des points
        voisins = reseau[p]["voisins"]
        debits_voisins = [debits_noeud[voisin] for voisin in voisins if voisin in debits_noeud]
        pressions_voisins = [pressions_noeud[voisin] for voisin in voisins if voisin in pressions_noeud]

        if "debit" in reseau[p]:
            Q[p] = -reseau[p]["debit"]  # Debit sortant lorsque la valeur est donnée
        else:
            inconnues.append(p)  # ajout du nœud a la liste des inconnus
            if debits_voisins:
                Q[p] = np.average(debits_voisins)*0.6
            else:
                Q[p] = np.random.uniform()

        if "pression" in reseau[p]:
            P[p] = reseau[p]["pression"]
        else:
            inconnues.append(p + size)  # ajout du nœud a la liste des inconnus
            if pressions_voisins:
                P[p] = np.average(pressions_voisins)*0.6
            else:
                P[p] = np.random.uniform()*100

    for n in cond:  # Initialization des debits des conduits
        inconnues.append(n + nb_point)  # tous les conduits sont inconnus
        point1 = cond[n][0]
        point2 = cond[n][1]

        # moyenne = np.average((Q[point1], Q[point2]))

        # Estimation avec la loi de Poiseuille
        debit_estime = abs(np.pi * (P[point2] - P[point1] + 2) * (prm.D / 2) ** 4 / (8 * prm.mu * prm.L))

        Q[n + nb_point] = debit_estime

    return Q, P, inconnues


def sortie_console(noeuds, conduits=0):
    """Génère une belle sortie des données dans la console"""
    for p in noeuds:
        print("Noeud " + str(p + 1), ":")
        print("Pression :", noeuds[p]["pression"], "mmH2O")
        print("Debit :", noeuds[p]["debit"], "m³/s")
        print("-------------------------------")

    if conduits != 0:
        for c in conduits:
            print("Conduit " + str(c + 1), ":")
            print("Noeuds :", conduits[c]["noeuds"])
            print("Debit :", conduits[c]["debit"], "m³/s")
            print("-------------------------------")
