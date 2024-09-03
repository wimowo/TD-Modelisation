# Importation des modules
import matplotlib.pyplot as plt
import numpy as np


def genXY(n):
    """Fonction de génération de points aléatoires
    
    Entrée:
        - n : nombre de points à générer, entier (int)
    
    Sortie:
        - Retourne 2 vecteurs, positions en x et positions en y
    """
    assert isinstance(n,int) or isinstance(n,np.int32), "n pas du bon type."
    
    ### Fonction à écrire

    rand = np.random.rand(2,n)
   
    return rand[0], rand[1]


def monte_carlo(x,y):
    """Fonction calculant pi par la méthode de Monte Carlo
    
    Entrée:
        - x : vecteur de positions en x
        - y : vecteur de positions en y
    
    Sortie:
        - Retourne 1 valeur float, approximation de pi
    """
    assert len(x)==len(y), "Grandeurs des vecteurs ne concordent pas."
    
    ### Fonction à écrire

    r = x**2+y**2

    N = len(r)
    Nc = [i for i in r if i <= 1]
   
    pi = float((len(Nc)/N)*4)
            
    return pi

    
    
    
    
    
    
    
    
    
