# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 09:25:47 2024

@author: tardi
"""
L = 25
D = 0.2
e = 0.00026
rho = 1000
mu = 0.00089
import numpy as np

def Reynolds(Q) :
    return (4*rho*Q)/(np.pi*mu*D)

def Cr(Q):
    return (-2*2**0.5)/(3.83*Reynolds(Q)**0.105)*(np.log10(e/(3.7*D)+1.78/Reynolds(Q)))

def Resistance(Q) :
    return L/ (944.62*Cr(Q)**1.8099*D**4.8099)



print(Resistance(0.5))