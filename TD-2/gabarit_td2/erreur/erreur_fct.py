# Importation des modules
import numpy as np

def g(x):
    """Fonction qui calcule une valeur selon la fonction demandée
    
    Entrée:
        - Valeur de x pour le calcul
     
    Sortie:
        - Valeur obtenue après calcul
    """
    
    return (2*np.sqrt(x**3)+3*np.sqrt(x))/(1+x)-3*np.atan(np.sqrt(x))

def diff_arriere_ordre1(x,h):
    """Fonction qui calcule l'approximation de la dérivée numérique, selon le
    schéma arrière d'ordre 1, pour une fonction quelconque
    
    Entrée:
        - x : Variable indépendante
        - h : le pas (dx) de différentiation [float]
    
    Sortie:
        - Valeur numérique de la différentiation
    """
    #assert isinstance(h,float), "Pas h pas du bon type."

    dg = (g(x)-g(x-h))/h

    return dg

def diff_centree_ordre2(x,h):
    """Fonction qui calcule l'approximation de la dérivée numérique, selon le
    schéma centrée d'ordre 2, pour une fonction quelconque
    
    Entrée:
        - x : Variable indépendante
        - h : le pas (dx) de différentiation [float]
    
    Sortie:
      - Valeur numérique de la différentiation
    """
    #assert isinstance(h,float), "Pas h pas du bon type."
    
    dg = (g(x+h)-g(x-h))/(2*h)
    
    return dg