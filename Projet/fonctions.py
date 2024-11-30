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
        np.log10(prm.e / (3.7 * prm.D) + 1.78 / reynolds(q, prm)))


def resistance(q, prm):
    return prm.L / (944.62 * np.sign(cr(q, prm)) * (np.abs(cr(q, prm)) ** 1.8099) * (prm.D ** 4.8099))


def perte(q, prm):
    return resistance(q, prm) * q ** prm.n


def residu(Q, P, points, prm):
    """Calcul du residu du systeme d'equation"""

    cond = conduits(points)

    nb_points = len(points)
    nb_cond = len(cond)

    debits = np.zeros(nb_points)
    pressions = np.zeros(nb_cond)

    for x in points:
        for c in cond:
            if x == cond[c][0]:
                debits[x] -= Q[c]
                break
            elif x == cond[c][1]:
                debits[x] += Q[c]
                break


        if "debit" in points[x]:
            q_out = points[x]["debit"]
            debits[x] -= q_out

    for c in range(nb_cond):
        p1 = P[cond[c][0]]
        p2 = P[cond[c][1]]
        if "pression" in points[cond[c][0]]:
            p1 = points[cond[c][0]]["pression"]
        if "pression" in points[cond[c][1]]:
            p2 = points[cond[c][1]]["pression"]

        pressions[c] = np.abs(p1 - p2) - perte(Q[c], prm)

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
        Q = x[0: nb_cond]
        P = x[nb_cond:]

        R = residu(Q, P, points, prm)

        J = np.empty([size, size])

        for i in range(len(R)):
            x_p = np.copy(x)

            x_p[i] = x_p[i] + h
            R_p = residu(Q=x_p[0: nb_cond], P=x_p[nb_cond:], points=points, prm=prm)
            J[:, i] = (R_p - R) / h
        print(J)
        delta = -np.linalg.solve(J, R)
        x = x + delta
        print(x)
        n = n + 1

    return x


def calculation_sim(points, prm):
    """Fonction servant a effectuer la simulation du systeme"""

    return


def conduits(points):
    """Fonction qui renvoie les conduits et les points les connectants"""
    conduit_list = {}
    x = 0
    for n in points:
        for voisin in points[n]["voisins"]:

            if (voisin, n) not in conduit_list.values():
                conduit_list[x] = (n, voisin)
                x += 1

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
