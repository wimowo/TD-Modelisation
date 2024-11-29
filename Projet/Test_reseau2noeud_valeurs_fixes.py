# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 18:59:49 2024

@author: tardi
"""
import numpy as np

L = 25
D = 0.2
e = 0.00026
rho = 1000
mu = 0.00089

def Reynolds(Q) :
    # if Q==0:
    #     return 100
    # else:
     return (4*rho*Q)/(np.pi*mu*D)

def Cr(Q):
    return (-2*2**0.5)/(3.83*Reynolds(Q)**0.105)*(np.log10(e/(3.7*D)+1.78/Reynolds(Q)))


def Resistance(Q) :
    return L/ (944.62*(Cr(Q)**1.8099)*(D**4.8099))

#[D1, R1, P2]
x = [0.75, 0.5, 200]
def residu(x):
    residu = np.empty([3,])
    residu[0] = x[0]+x[1]
    residu[1] = 0.5+x[1]
    residu[2] = abs(x[2]-100 ) - Resistance(abs(x[1])) * abs(x[1])**1.8099
    return residu

N = 100
tol = 0.1
h = tol
delta = 1
n = 0 
while np.linalg.norm(delta) > tol and n < N:
    R = residu(x)

    J = np.empty([3,3])
    for i in range(len(R)):
        x_p = np.copy(x)
        x_p[i] = x_p[i]+h
        R_p = residu(x_p)
      
        J[i] = np.subtract(R_p,R)/h
    print(J)
    delta = np.linalg.solve(J.T, np.negative(R))
    x = x + delta
    n = n + 1
print(x)
