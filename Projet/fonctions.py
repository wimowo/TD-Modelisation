# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 09:25:47 2024

@author: tardi
"""
import numpy as np


def Reynolds(q, prm):
    return (4 * prm.rho * q) / (np.pi * prm.mu * prm.D)


def Cr(q, prm):
    return (-2 * (2 ** 0.5)) / (3.83 * (Reynolds(q, prm) ** 0.105)) * (
        np.log10(np.e / (3.7 * prm.D) + 1.78 / Reynolds(q, prm)))


def Resistance(q, prm):
    return prm.L / (944.62 * (Cr(q, prm) ** 1.8099) * (prm.D ** 4.8099))


def residu(Q, P, points, prm):
    """Calcul du residu du systeme d'equation"""

    cond = conduits(points)

    nb_points = len(points)
    nb_cond = len(cond)

    debits = np.zeros(nb_points)
    pressions = np.zeros(nb_cond)

    for x in points:
        for voisins in points[x]["voisins"]:
            debits[x] += Q[voisins]

        if "debit" in points[x]:
            q_out = points[x]["debit"]
            debits[x] -= q_out

    for c in range(nb_cond):
        p1 = P[cond[c][0]]
        p2 = P[cond[c][1]]
        if "pression" in points[cond[c][0]]:
            pressions[c] = abs(points[cond[c][0]]["pression"] - p2) - Resistance(Q[cond[c][0]], prm) * Q[cond[c][0]]
        else:
            pressions[c] = abs(p1 - p2) - Resistance(Q[cond[c][0]], prm) * Q[cond[c][0]]**prm.n

    r = np.concatenate((debits, pressions))

    return r


def newton_resolution(Q, P, tol, points, prm):
    N = 100

    h = tol
    delta = 1
    n = 0

    nb_points = len(points)
    nb_cond = len(conduits(points))

    size = nb_cond + nb_points
    x = np.concatenate((Q, P))

    while np.linalg.norm(delta) > tol and n < N:
        Q = x[0: nb_points]
        P = x[nb_points: size]
        R = residu(Q, P, points, prm)

        J = np.empty([size, size])

        for i in range(len(R)):
            x_p = np.copy(x)
            x_p[i] = x_p[i] + h
            R_p = residu(Q=x_p[0: nb_points], P=x_p[nb_points: size], points=points, prm=prm)
            J[i] = np.subtract(R_p, R) / h

        delta = -np.linalg.solve(J.T, R)
        x = x + delta
        n = n + 1

    return x


def calculation_sim(points, prm):
    """Fonction servant a effectuer la simulation du systeme"""

    return


def conduits(points):
    """Fonction qui renvoie le nombre de conduit"""
    conduit_list = []

    for n in points:
        for voisin in points[n]["voisins"]:
            if (voisin, n) not in conduit_list:
                conduit_list.append((n, voisin))

    return conduit_list


def initiales(points):
    nb_point = len(points)

    q = 0
    p = 0

    Q = np.zeros(len(points))
    P = np.zeros(len(conduits(points)))

    for p in points:
        if "debit" in points[p]:
            Q[p] = points[p]["debit"]
        if "pression" in points[p]:
            P += points[p]["pression"]

    P /= nb_point
    Q /= nb_point

    P = np.a
    return Q, P
