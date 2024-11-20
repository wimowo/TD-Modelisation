# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 09:25:47 2024

@author: tardi
"""

import numpy as np

def Reynolds(Q) :
    return (4*rho*Q)/(np.pi*mu*D)

def Cr(Q):
    return (-2*2**0.5)/(3.83*Reynolds(Q)**0.105)*(np.log10(np.exp(1)/(3.7*D))+1.78/Reynolds(Q))

def Resistance(Q) :
    return L/ (944.62*Cr(Q)**1.8099*D**4.8099)

