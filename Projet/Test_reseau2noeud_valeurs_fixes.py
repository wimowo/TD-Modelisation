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
    
     return (4*rho*Q)/(np.pi*mu*D)

def Cr(Q):
    return (-2*2**0.5)/(3.83*Reynolds(Q)**0.105)*(np.log10(e/(3.7*D)+1.78/Reynolds(Q)))


def Resistance(Q) :
    return L/ (944.62*(Cr(Q)**1.8099)*(D**4.8099))

#[D1, R1, P2]
# x = [0.75, 0.5, 200]
# def residu(x):
#     residu = np.empty([3,])
#     residu[0] = x[0]+x[1]
#     residu[1] = 0.5+x[1]
#     residu[2] = abs(x[2]-100 ) - Resistance(abs(x[1])) * abs(x[1])**1.8099
#     return residu

# N = 100
# tol = 0.1
# h = tol
# delta = 1
# n = 0 
# while np.linalg.norm(delta) > tol and n < N:
#     R = residu(x)

#     J = np.empty([3,3])
#     for i in range(len(R)):
#         x_p = np.copy(x)
#         x_p[i] = x_p[i]+h
#         R_p = residu(x_p)
      
#         J[i] = np.subtract(R_p,R)/h
#     print(J)
#     delta = np.linalg.solve(J.T, np.negative(R))
#     x = x + delta
#     n = n + 1
# print(x)

#[P3, P4, P5, P6, D1, D2, DC1, DC2, DC3, DC4, DC5, DC6, DC7]
inconnus = {'P3': 90.0, 'P4': 90.0, 'P5': 81.0, 'P6': 81.45, 'D1': 0.5, 'D2': 0.6, 'DC1': 0.01764939693027974, 'DC2': 0.01764939693027974, 'DC3': 0.01764939693027974, 'DC4': 0.01764939693027974, 'DC5': 0.03273963130566891, 'DC6': 0.015884457237251768, 'DC7': 0.0007942228618625934}
vec_inconnu = []
for a,b in  inconnus.items():
    vec_inconnu.append(b)
# Connus :  {'P1': 100, 'P2': 95, 'D3': -0.3, 'D4': -0.2, 'D5': -0.4, 'D6': -0.1}
print(vec_inconnu)
x = [90.0, 90.0, 81.0, 81.45, 0.5, 0.6, 0.01764939693027974, 0.01764939693027974, 0.01764939693027974, 0.01764939693027974, 0.03273963130566891, 0.015884457237251768, 0.0007942228618625934]
def residu(x):
    residu = np.empty([13,])
    residu[0] = x[4]+x[6]+x[7]
    residu[1] = x[5]+x[8]+x[9]+x[10]
    residu[2] = 0.3+x[6]+x[3]
    residu[3] = 0.2+x[7]+x[9]+x[11]
    residu[4] = 0.4+x[11]+x[12]
    residu[5] = 0.1+x[10]+x[12]
    
    residu[6] = abs(x[0]-100 ) - Resistance(abs(x[6])) * abs(x[6])**1.8099
    residu[7] = abs(x[1]-100 ) - Resistance(abs(x[7])) * abs(x[7])**1.8099
    residu[8] = abs(x[0]-95 ) - Resistance(abs(x[8])) * abs(x[8])**1.8099
    residu[9] = abs(x[1]-95 ) - Resistance(abs(x[9])) * abs(x[9])**1.8099
    residu[10] = abs(x[3]-95 ) - Resistance(abs(x[10])) * abs(x[10])**1.8099
    residu[11] = abs(x[1]-x[2] ) - Resistance(abs(x[11])) * abs(x[11])**1.8099
    residu[12] = abs(x[2]-x[3] ) - Resistance(abs(x[12])) * abs(x[12])**1.8099
    return residu

N = 100
tol = 0.1
h = tol
delta = 1
n = 0 
while np.linalg.norm(delta) > tol and n < N:
    R = residu(x)

    J = np.empty([13,13])
    for i in range(len(R)):
        x_p = np.copy(x)
        x_p[i] = x_p[i]+h
        R_p = residu(x_p)
      
        J[i] = np.subtract(R_p,R)/h
 
    delta = np.linalg.solve(J.T, np.negative(R))
    x = x + delta
    n = n + 1
print(x)

inconnu_resolu = [ 1.98625978e+05 , 1.08533203e+02, 1.21507423e+02,  2.94409532e+01,
  2.99358291e+01,  2.94464519e+01, -2.97409532e+01, -1.94875867e-01,
 -2.97413277e+01, -2.45438251e-01 , 5.40314118e-01,  2.40314118e-01,
 -6.40314118e-01]
i=0
for a,b in  inconnus.items():
    b = inconnu_resolu[i]
    print(b)
    i+=1
    
print(inconnus)