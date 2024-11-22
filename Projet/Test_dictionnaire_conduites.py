# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 21:51:00 2024

@author: tardi
"""
# C pour conduite et N pour noeud
reseau_6_noeuds = {0: {"voisins": [2,3], "pression": 100}, 
                   1: {"voisins": [2,3,5], "pression": 95}, 
                   2: {"voisins": [0,1], "debit" : 0.3}, 
                   3: {"voisins": [0,1,4], "debit" : 0.2}, 
                   4: {"voisins": [3,5], "debit" : 0.4}, 
                   5: {"voisins": [1,4], "debit" : 0.1}}

def construire_conduites(reseau):
    conduites = {}
    i=1
    for noeud, details in reseau.items():
        for voisin in details["voisins"]:
            if voisin < noeud:  
                pass
            else:
                conduites[(noeud, voisin)] = f'C_{i}'
                i+=1
    return conduites

conduites = construire_conduites(reseau_6_noeuds)

for noeud, details in reseau_6_noeuds.items():
      
        somme_debits = 0
        
        # Parcourir les voisins pour calculer la somme des débits entrants et sortants
        for voisin in details["voisins"]:
                
                tuyau_key = (noeud, voisin) 
                
                if tuyau_key in conduites:
                    tuyau_nom = conduites[tuyau_key]      
        