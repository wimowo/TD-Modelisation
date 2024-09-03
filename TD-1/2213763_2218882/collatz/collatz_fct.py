import numpy as np

# Fonction de la conjecture de Collatz
def collatz(i):
    """Fonction de calcul du nombre d'itération pour la conjecture de Collatz
    
    Entrée:
        - i : nombre entier en entrée (int)
    
    Sortie:
        - Un nombre entier correspondant au nombre d'itération
    """
    assert type(i) != float, "Pas le bon type."
    assert type(i) != str, "Pas le bon type."
    assert type(i) != np.float64, "Pas le bon type."
    
    ### Fonction à écrire
    num = i
    cnt = 0

    while num != 1:
        if num % 2 == 0:
            num /= 2
        else:
            num = num * 3 + 1
        cnt += 1

    return cnt