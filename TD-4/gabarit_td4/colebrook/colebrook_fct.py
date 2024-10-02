# Importation des modules
import numpy as np

def f(l,cst):
    """Calcul de la fonction de lambda
    
    Entrées :
        - l : Coefficient de friction lambda [-]
        - cst : objet class constantes
            - Re : Nombre de Reynolds [-]
            - k : Rugosité [m]
            - D : diamètre de la conduite [m]
    
    Sortie :
        - Valeur numérique de la fonction
        
    """
    
    # Fonction à écrire
    
    return 2*np.log10((cst.k/(3.7*cst.D))+(2.51/(cst.Re*np.sqrt(l))))*np.sqrt(l)+1

def bissection(x1,x2,tol,N,cst):
    """Fonction calculant une racine d'une fonction grâce à la bissection
    
    Entrées :
        - x1 : estimé initial, borne inférieure
        - x2 : estimé initial, borne supérieure
        - tol : critère d'arrêt
        - N : nombre maximal d'itérations possible
        - cst : objet class constantes
            - Re : Nombre de Reynolds [-]
            - k : Rugosité [m]
            - D : diamètre de la conduite [m]
    
    Sortie :
        - Valeur numérique de la racine de la fonction
    
    """
    i = 0
    while abs(x2-x1)> tol and i < N :
        x_m = (x1+x2)/2
        if f(x2,cst)*f(x_m,cst) < 0:
            x1 = x_m
        else:
            x2 = x_m
        i+=1
    
    return x_m
   
