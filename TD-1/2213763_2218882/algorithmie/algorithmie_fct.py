#Importation des modules
import numpy as np

# Fonction de la serie harmonique
def serie_harmonique(N):
    """Fonction qui calcule la série harmonique en sommant les N premiers termes
    
    Sortie:
        - Un nombre flottant contenant la valeur de la série
    """
    sum = 0

    for i in range(N):
        sum += 1/(i+1)
    
    return sum

# Fonction de la fonction factorielle
def factoriel(k):
    """Fonction qui calcule le factoriel de k

    Sortie:
        - Un nombre entier contenant le factoriel de k
    """
    factorial = 1
    for i in range(1, k+1):
        factorial *= i

    return factorial