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
    if Q==0:
        return 100
    else:
     return abs((4*rho*Q)/(np.pi*mu*D))

def Cr(Q):
    return abs((-2*2**0.5)/(3.83*Reynolds(Q)**0.105)*(np.log10(np.exp(1)/(3.7*D)+1.78/Reynolds(Q))))

def Resistance(Q) :
    return L/ (944.62*-Cr(Q)**1.8099*D**4.8099)


# C pour conduite et N pour noeud
reseau_6_noeuds = {1: {"voisins": [3,4], "pression": 100}, 
                   2: {"voisins": [3,4,6], "pression": 95}, 
                   3: {"voisins": [1,2], "debit" : -0.3}, 
                   4: {"voisins": [1,2,5], "debit" : -0.2}, 
                   5: {"voisins": [4,6], "debit" : -0.4}, 
                   6: {"voisins": [2,5], "debit" : -0.1}}

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
        else:
            # Si pas de pression, on prend la moyenne des pressions des voisins
            voisins = details["voisins"]
            pressions_voisins = [pressions_noeud[f'P{voisin}'] for voisin in voisins if f'P{voisin}' in pressions_noeud]
            if pressions_voisins:
                pressions_noeud[f'P{noeud}'] = sum(pressions_voisins) / len(pressions_voisins)
            else:
                pressions_noeud[f'P{noeud}'] = 100  # Valeur par défaut s'il n'y a pas de voisins avec pression définie 
       
        if "debit" in details:
            debits_noeud[f'D{noeud}'] = details["debit"]
        else:
            # Si pas de débit spécifié, initialiser à 0 par défaut
            debits_noeud[f'D{noeud}'] = 0
    for noeud, details in reseau_6_noeuds.items():   
        for voisin in details["voisins"]:
            tuyau_key = (noeud,voisin)
            if tuyau_key in conduites:
                tuyau = conduites[tuyau_key]
                # Estimer un débit basé sur la différence de pression
                pression_noeud = pressions_noeud[f'P{noeud}']
                pression_voisin = pressions_noeud[f'P{voisin}']
                debit_estime = np.pi*(pression_noeud - pression_voisin)*(D/2)**4/(8*mu*L)
                
                # Ajouter l'estimation du débit pour cette conduite
                debits_tuyaux[f'D{tuyau}'] = debit_estime
            
        
        # vraiment compliqué de choisir des pression en fonction du sens des débits et pressions voisins...
           # pression_noeud = details['pression']
           # pression_moyenne = 0
           # debit_voisin = []
           # for voisin in details["voisins"]:
           #     if "debit" in reseau_6_noeuds[voisin]:
           #         print(reseau_6_noeuds[voisin]['debit'])
           #         print(voisin)
           #     if "pression" in reseau_6_noeuds[voisin]:
           #         print(reseau_6_noeuds[voisin]['pression'])
                   
           #     elif "debit" in reseau_6_noeuds[voisin]:
           #         print(reseau_6_noeuds[voisin]['debit'])    
                
    return conduites,pressions_noeud,debits_noeud,debits_tuyaux


# Ca semble être cohérent avec les valeurs initale estimées
conduites,pressions_noeud,debits_noeud,debits_tuyaux = construire_valeurs_initales(reseau_6_noeuds)
# print('Dict des conduites:', conduites)
# print('Dict des Pressions au noeud:', pressions_noeud)
# print('Dict des débits au noeud:', debits_noeud)
# print('Dict des débits par conduite:',debits_tuyaux)



# Reste a diviser les inconnus 
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
# print("Connus : ", connus)
# print("Inconnus : ", inconnus)

vec_connu = list(connus.keys())
vec_valeur_connues = list(connus.values())

vec_inconnu = list(inconnus.keys())
vec_valeur_inconnues = list(inconnus.values())

print("Variables connues : ", vec_connu)
print("Valeurs des variables connues : ", vec_valeur_connues)
print("Variables inconnues : ", vec_inconnu)
print("Valeurs des variables inconnues : ", vec_valeur_inconnues)

# Fonction de calcul des résidus
def calcul_residu(reseau_6_noeuds, conduites, variables_connues, valeurs_connues, variables_inconnues, valeurs_inconnues):
    # Créer un dictionnaire pour accéder aux valeurs par variable (connues et inconnues)
  
    variables_connues = np.array(variables_connues)
    variables_inconnues = np.array(variables_inconnues)
    valeurs_connues = np.array(valeurs_connues)
    valeurs_inconnues = np.array(valeurs_inconnues)
    
    
    variables_et_valeurs = dict(zip(np.concatenate([variables_connues, variables_inconnues]), 
                               np.concatenate([valeurs_connues, valeurs_inconnues])))
 
    # Résidu pour les noeuds (somme des débits entrants et sortants)
    residu_noeud = []
    
    for noeud, details in reseau_6_noeuds.items():
        somme_debits = 0
        
        # Ajouter les débits connus du noeud
        debit_noeud = variables_et_valeurs.get(f'D{noeud}', 0)  # Débit du noeud
        somme_debits += debit_noeud
        
        # Ajouter les débits estimés des conduites
        for voisin in details['voisins']:
            tuyau_key = (min(noeud, voisin), max(noeud, voisin))
            tuyau_nom = conduites[tuyau_key]
            
            # Extraction correcte de l'indice de la conduite
            tuyau_indice = int(tuyau_nom[1:])  # Indice des débits dans les conduites
            
            # Récupérer les débits estimés des conduites
            debit_estime = debits_tuyaux.get(f'D{tuyau_nom}', 0)  # Débit estimé pour la conduite
            somme_debits += debit_estime
        
        # Le résidu pour ce noeud (la somme des débits doit être égale à zéro)
        residu_noeud.append(somme_debits)
    
    # Résidu pour les conduites (calcul de la résistance)
    residu_conduites = []
   
    for (noeud_i, noeud_j), tuyau in conduites.items():
         P_i = variables_et_valeurs.get(f'P{noeud_i}', 0)  # Pression du noeud i
         P_j = variables_et_valeurs.get(f'P{noeud_j}', 0)  # Pression du noeud j
         tuyau_indice = int(tuyau[1:])  # Indice des débits dans les conduites
         
         Q = variables_et_valeurs.get(f'DC{tuyau_indice}', 0)  # Débit dans la conduite
    
         # Calcul de R(Q) pour la conduite
         RQ = Resistance(Q)  # Résistance (fonction que vous avez déjà définie)
         
         # Calcul du résidu pour cette conduite
         residu_conduites.append(abs(P_i - P_j) - RQ * abs(Q)**1.8099)
    
    # Concaténer les résidus des noeuds et des conduites
    residu_total = np.concatenate([residu_noeud, residu_conduites])
    
    return residu_total
print(calcul_residu(reseau_6_noeuds, conduites, vec_connu , vec_valeur_connues, vec_inconnu , vec_valeur_inconnues))
N = 100
tol =0.1
h = tol
delta = 1
n = 0 
while np.linalg.norm(delta) > tol and n < N:
    R = calcul_residu(reseau_6_noeuds, conduites, vec_connu , vec_valeur_connues, vec_inconnu , vec_valeur_inconnues) 
    
    J = np.empty([len(vec_inconnu),len(vec_inconnu)])
    for i in range(len(R)):
        x_p = np.copy(vec_valeur_inconnues)
        x_p[i] = x_p[i]+h
        R_p = calcul_residu(reseau_6_noeuds, conduites, vec_connu , vec_valeur_connues, vec_inconnu , x_p)
        J[i] = np.subtract(R_p,R)/h
    delta = np.linalg.solve(J.T, np.negative(R))
    vec_valeur_inconnues = vec_valeur_inconnues + delta
    n = n + 1

