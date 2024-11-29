# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 21:51:00 2024

@author: tardi
"""
import numpy as np
# Constantes
L = 25
D = 0.2
e = 0.00026
rho = 1000
mu = 0.00089
#fonction resistance

def Reynolds(Q) :
    
     return (4*rho*Q)/(np.pi*mu*D)

def Cr(Q):
    return (-2*2**0.5)/(3.83*Reynolds(Q)**0.105)*(np.log10(e/(3.7*D)+1.78/Reynolds(Q)))

def Resistance(Q) :
    return L/ (944.62*Cr(Q)**1.8099*D**4.8099)

# C pour conduite et N pour noeud
# reseau_6_noeuds = {1: {"voisins": [3,4], "pression": 100}, 
#                     2: {"voisins": [3,4,6], "pression": 95}, 
#                     3: {"voisins": [1,2], "debit" : -0.3}, 
#                     4: {"voisins": [1,2,5], "debit" : -0.2}, 
#                     5: {"voisins": [4,6], "debit" : -0.4}, 
#                     6: {"voisins": [2,5], "debit" : -0.1}}

# reseau_6_noeuds = {1: {"voisins": [2,3], "debit": 0.75}, 
#                     2: {"voisins": [1,3], "debit": -0.25}, 
#                     3: {"voisins": [1,2], "pression" : 10}}
                   
reseau_6_noeuds = {1: {"voisins": [2], "pression": 100}, 
                    2: {"voisins": [1], "debit": -0.5}}

def construire_conduites(reseau):
    conduites = {}
    i=1
    for noeud, details in reseau.items():
        for voisin in details["voisins"]:
            if voisin < noeud:  
                pass
            else:
                conduites[(noeud, voisin)] = f'C{i}'
                i+=1
    return conduites

                    
def construire_valeurs_initales(reseau):
    pressions_noeud = {}
    debits_noeud = {}
    debits_tuyaux = {}
    conduites = construire_conduites(reseau)
    
    for noeud, details in reseau_6_noeuds.items():
        if "pression" in details: 
            pressions_noeud[f'P{noeud}'] = details["pression"]
        if "debit" in details:
            debits_noeud[f'D{noeud}'] = details["debit"]
    
    for noeud, details in reseau_6_noeuds.items():
        
     
        # Si pas de pression, on prend la moyenne des pressions des voisins    
          
            voisins = details["voisins"]
            pressions_voisins = [pressions_noeud[f'P{voisin}'] for voisin in voisins if f'P{voisin}' in pressions_noeud]
            if pressions_voisins:
                pressions_noeud[f'P{noeud}'] = (sum(pressions_voisins) / len(pressions_voisins))*0.9
            else:
                pressions_noeud[f'P{noeud}'] = 100  # Valeur par défaut s'il n'y a pas de voisins avec pression définie 
       
            # Si pas de débit spécifié, prendre la somme des débits voisins
            voisins = details["voisins"]
           
            debits_voisins = [debits_noeud[f'D{voisin}'] for voisin in voisins if f'D{voisin}' in debits_noeud]
           
            if debits_voisins:
                debits_noeud[f'D{noeud}'] = abs(sum(debits_voisins))
            else:
                debits_noeud[f'D{noeud}'] = 100  # Valeur par défaut s'il n'y a pas de voisin
         
        
            
            
# code pour les debits initiales dans les conduites
    for noeud, details in reseau_6_noeuds.items():   
        for voisin in details["voisins"]:
            tuyau_key = (noeud,voisin)
            if tuyau_key in conduites:
                tuyau = conduites[tuyau_key]
                # Estimer un débit basé sur la différence de pression
                pression_noeud = pressions_noeud[f'P{noeud}']
                pression_voisin = pressions_noeud[f'P{voisin}']
                # Estimation avec la loi de Poiseuille
                debit_estime = abs(np.pi*(pression_noeud - pression_voisin)*(D/2)**4/(8*mu*L))
                
                # Ajouter l'estimation du débit pour cette conduite
                debits_tuyaux[f'D{tuyau}'] = debit_estime
            
    return conduites,pressions_noeud,debits_noeud,debits_tuyaux


# Ca semble être cohérent avec les valeurs initale estimées
conduites,pressions_noeud,debits_noeud,debits_tuyaux = construire_valeurs_initales(reseau_6_noeuds)
print('Dict des conduites:', conduites)
# print('Dict des Pressions au noeud:', pressions_noeud)
# print('Dict des débits au noeud:', debits_noeud)
print('Dict des débits par conduite:',debits_tuyaux)



# Diviser les inconnus et connus
connus = {}
inconnus = {}

# Séparer les pressions des noeuds connus (en fonction de reseau_6_noeuds)
for noeud, details in reseau_6_noeuds.items():
    pression_key = f'P{noeud}'
    if 'pression' in details:  # Si pression spécifiée dans reseau_6_noeuds
        connus[pression_key] = details["pression"]
    else:  # Sinon, considérer comme inconnu avec la valeur estimée
        inconnus[pression_key] = pressions_noeud.get(pression_key)  # Valeur estimée par défaut

# Séparer les débits des noeuds connus (en fonction de reseau_6_noeuds)
for noeud, details in reseau_6_noeuds.items():
    debit_key = f'D{noeud}'
    if 'debit' in details:  # Si débit spécifié dans reseau_6_noeuds
        connus[debit_key] = details["debit"]
    else:  # Sinon, considérer comme inconnu avec la valeur estimée
        inconnus[debit_key] = debits_noeud.get(debit_key)  # Valeur estimée par défaut (0 ici)

# Séparer les débits des conduites (tous considérés comme inconnus dans ce cas)
for conduite_key in debits_tuyaux.keys():
    inconnus[conduite_key] = debits_tuyaux.get(conduite_key)  # Valeur estimée par défaut

# Afficher les résultats
print("Connus : ", connus)
print("Inconnus : ", inconnus)


# # Fonction de calcul des résidus
def calcul_residu(reseau_6_noeuds, conduites, connus, inconnus):
    
    # Résidu pour les noeuds (somme des débits entrants et sortants)
    residu_noeud = []
    
    for noeud, details in reseau_6_noeuds.items():
        somme_debits = 0
        
        # Ajouter les débits connus du noeud
        if f'D{noeud}' in inconnus:
            debit_noeud = inconnus.get(f'D{noeud}')  # Débit du noeud
        else:
            debit_noeud = connus.get(f'D{noeud}')  # Débit du noeud
        somme_debits += debit_noeud
        
        # Ajouter les débits estimés des conduites
        for voisin in details['voisins']:
            
            tuyau_key = (min(noeud, voisin), max(noeud, voisin))
            tuyau_nom = conduites[tuyau_key]
            
            # Extraction correcte de l'indice de la conduite
            tuyau_indice = int(tuyau_nom[1:])  # Indice des débits dans les conduites
            
            # Récupérer les débits estimés des conduites
            if f'D{tuyau_nom}' in inconnus:
                debit_estime = inconnus.get(f'D{tuyau_nom}')
            else:
                debit_estime = connus.get(f'D{tuyau_nom}')
            # print(debit_estime)
            somme_debits += debit_estime
        
        # Le résidu pour ce noeud (la somme des débits doit être égale à zéro)
        residu_noeud.append(somme_debits)
   
    # Résidu pour les conduites (calcul de la résistance)
    residu_conduites = []
    
    for (noeud_i, noeud_j), tuyau in conduites.items():
        if f'P{noeud_i}' in inconnus:
            P_i = inconnus.get(f'P{noeud_i}')  # Pression du noeud i
        else:
            P_i = connus.get(f'P{noeud_i}')  # Pression du noeud i
           
           
        if f'P{noeud_j}' in inconnus:
           P_j = inconnus.get(f'P{noeud_j}')  # Pression du noeud j  
            
        else:   
            P_j = connus.get(f'P{noeud_j}')  # Pression du noeud j
        tuyau_indice = int(tuyau[1:])  # Indice des débits dans les conduites
        
        if f'DC{tuyau_indice}' in inconnus:
            Q = inconnus.get(f'DC{tuyau_indice}')  # Débit dans la conduite
        else:   
            Q = connus.get(f'DC{tuyau_indice}')  # Débit dans la conduite
  
        # Calcul de R(Q) pour la conduite
        RQ = Resistance(abs(Q))  # Résistance 
       
        # Calcul du résidu pour cette conduite
        residu_conduites.append(abs(P_i - P_j) - RQ * abs(Q)**1.8099)
   
    # Concaténer les résidus des noeuds et des conduites
    residu_total = np.concatenate([residu_noeud, residu_conduites])
    
    return residu_total

# Newton-Raphson
N = 100
tol =0.001
h = tol
delta = 1
n = 0 
while np.linalg.norm(delta) > tol and n < N:
    R = calcul_residu(reseau_6_noeuds, conduites, connus, inconnus) 
    # print('R',R)
    J = np.empty([len(R),len(R)])
    i=0
    for a,b in inconnus.items() :
        # print('ab',a,b)
        x_p = inconnus.copy()
        x_p[a] = b+h
        # print('xp',x_p)
        R_p = calcul_residu(reseau_6_noeuds, conduites, connus, x_p)
        # print('RP',R_p)
        # print('soustra',np.subtract(R_p,R))
        J[i] = np.subtract(R_p,R)/h
        i+=1
    # print(J)
    delta = np.linalg.solve(J.T, np.negative(R))
    
    i=0
    for a,b in inconnus.items() :
       
        inconnus[a]= b + delta[i]
        
        i+=1
    n = n + 1
print(inconnus)


