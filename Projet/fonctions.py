# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 09:25:47 2024

@author: tardi
"""
import numpy as np

def residu(Q, P, points, prm):
    """Calcul du residu du systeme d'equation"""
    r = np.empty(points.shape[0])

    for p in points:
        r = 0
    return r

def newton_resolution(x, tol, prm):

    N = 100

    h = tol
    delta = 1
    n = 0

    while np.linalg.norm(delta) > tol and n < N:
        R = residu(x, prm)

        J = np.empty([len(x), len(x)])

        for i in range(len(R)):
            x_p = np.copy(x)
            x_p[i] = x_p[i] + h
            R_p = residu(x_p, prm)
            J[i] = np.subtract(R_p, R) / h

        delta = np.linalg.solve(J.T, np.negative(R))
        x = x + delta
        n = n + 1

    return x

def calculation_sim(points, prm):
    """Fonction servant a effectuer la simulation du systeme"""

    return

def conduits(points):
    """Fonction qui renvoie le nombre de conduit"""
    nb_conduits = 0
    conduits = {}

    for n in points.values():
        nb_conduits += len(n["voisins"])
    nb_conduits = nb_conduits / 2

    return nb_conduits