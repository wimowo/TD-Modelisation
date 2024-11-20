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

    return

def calculation_sim(points, prm):
    """Fonction servant a effectuer la simulation du systeme"""

    return

def nb_conduit(points):
    """Fonction qui renvoie le nombre de conduit"""

    nb_voisins = 0

    for p in points:
        p.get("neighbors")