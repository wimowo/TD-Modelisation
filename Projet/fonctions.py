# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 09:25:47 2024

@author: tardi
"""
import numpy as np


def reynolds(q, prm):
    return (4 * prm.rho * q) / (np.pi * prm.mu * prm.D)


def cr(q, prm):
    return (-2 * (2 ** 0.5)) / (3.83 * (reynolds(q, prm) ** 0.105)) * (
        np.log(prm.e / (3.7 * prm.D) + 1.78 / reynolds(q, prm)))


def resistance(q, prm):
    return prm.L / (944.62  * np.abs(cr(q, prm)) ** 1.8099 * prm.D ** 4.8099)


def perte(q, prm):
    return resistance(q, prm) * q ** prm.n


def residu(Q, P, reseau, prm):
    """Calcul du residu du systeme d'equation"""

    cond = conduits(reseau)

    nb_points = len(reseau)
    nb_cond = len(cond)

    debits = np.zeros(nb_points)
    pressions = np.zeros(nb_cond)

    q = Q[:nb_points]
    qc = Q[nb_points:]

    for x in reseau:
        for c in cond:
            if x == cond[c][0]:
                debits[x] -= qc[c]
            if x == cond[c][1]:
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


def newton_resolution(Q, P, tol, reseau, prm):
    N = 1000

    h = tol
    delta = 1
    n = 0

    nb_points = len(reseau)
    nb_cond = len(conduits(reseau))

    Q, P, inc = initialisation(reseau)

    size = nb_cond + nb_points
    x = np.concatenate((Q, P))
    J = np.empty([size, size])

    sol = np.empty(size)

    for i in range(size):
        sol[i] = x[inc[i]]

    while np.linalg.norm(delta) > tol and n < N:

        Q = x[: size]
        P = x[size:]

        R = residu(Q, P, reseau, prm)

        for i in range(len(R)):
            x_p = np.copy(x)

            x_p[i] += h
            R_p = residu(Q=x_p[0: size], P=x_p[size:], reseau=reseau, prm=prm)
            J[:, i] = (R_p - R) / h

        delta = np.linalg.solve(J.T, -R)

        sol = sol + delta

        for i in range(size):
            x[inc[i]] = sol[i]

        print("sol=", sol)
        n = n + 1

    return sol


def calculation_sim(reseau, prm):
    """Fonction servant a effectuer la simulation du systeme"""

    return


def conduits(reseau):
    """Fonction qui renvoie les conduits et les points les connectants"""
    conduit_list = {}
    x = 0
    for n in reseau:
        for voisin in reseau[n]["voisins"]:

            if (voisin, n) not in conduit_list.values():
                conduit_list[x] = (n, voisin)
                x += 1

    return conduit_list


def initialisation(reseau):
    cond = conduits(reseau)

    nb_point = len(reseau)
    nb_cond = len(cond)
    size = nb_point + nb_cond

    Q = np.zeros(size)
    P = np.zeros(nb_point)
    inconnues = []

    for p in range(nb_point):  # Initialization des debits des points
        if "debit" in reseau[p]:
            Q[p] -= reseau[p]["debit"]
        else:
            inconnues.append(p)
            Q[p] = np.random.uniform()

    for n in range(nb_point, size):  # Initialization des debits des conduits
        inconnues.append(n)
        Q[n] = np.random.uniform()

    for p in range(nb_point):  # Initialization des pressions
        if "pression" in reseau[p]:
            P[p] = reseau[p]["pression"]
        else:
            inconnues.append(p + size)
            P[p] = np.random.uniform(1, 100)

    return Q, P, inconnues
