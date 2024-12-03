import numpy as np

try:
    from Test_dictionnaire_conduites import *
except:
    pass

# Ca semble être cohérent avec les valeurs initale estimées
conduites, pressions_noeud, debits_noeud, debits_tuyaux = construire_valeurs_initales(reseau_6_noeuds)
# print('Dict des conduites:', conduites)
# print('Dict des Pressions au noeud:', pressions_noeud)
# print('Dict des débits au noeud:', debits_noeud)
# print('Dict des débits par conduite:',debits_tuyaux)


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
print('conduites', conduites)

# Newton-Raphson
N = 100
tol = 0.01
h = tol
delta = 1
n = 0

while np.linalg.norm(delta) > tol and n < N:
    R = calcul_residu(reseau_6_noeuds, conduites, connus, inconnus)
    # print('R',R)
    J = np.empty([len(R), len(R)])
    i = 0
    for a, b in inconnus.items():
        # print('ab',a,b)
        x_p = inconnus.copy()
        x_p[a] = b + h
        # print('xp',x_p)
        R_p = calcul_residu(reseau_6_noeuds, conduites, connus, x_p)
        # print('RP',R_p)
        # print('soustra',np.subtract(R_p,R))
        J[i] = np.subtract(R_p, R) / h
        i += 1

    # print(J.T)
    delta = np.linalg.solve(J.T, np.negative(R))

    i = 0
    for a, b in inconnus.items():
        inconnus[a] = b + delta[i]

        i += 1
    n = n + 1

print('Résolution inconnus:', inconnus)
