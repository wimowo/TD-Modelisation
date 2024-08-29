#Importation des modules
import numpy as np
from matplotlib import pyplot as plt

# Fonctions pour construire les vecteurs x et f
def faire_vecteur_x():
    """Fonction qui génère un vecteur x allant de 0 à 5 avec 101 points
    
    Sortie:
        - Un np.array contenant 101 nombres allant de 0 à 5 inclusivement
    """
    
    x= np.linspace(0, 5,101)
    return x

def faire_vecteur_f():
   """Fonction qui génère un vecteur f(x)=x^2 en employant le vecteur f

    Sortie:
        - Un np.array contenant 101 chiffre contenant x^2 pour x appartenant à [0,5]
   """
   vecteur = np.square(faire_vecteur_x())
  
   return vecteur


# Créer le graphique
plt.xlabel("x")
plt.ylabel("f(x)")
plt.title('Graphique de la fonction f(x)')
plt.plot(faire_vecteur_x(),faire_vecteur_f(), label = 'f(x)')
plt.legend()

# Fonction pour construire la matrice du système d'équations
def faire_matrice():
    """Fonction qui génère une matrice pour le système d'équations suivant:
        2x - 5y + 3z = 8
        3x -  y + 4z = 7
         x + 3y + 2z = -3
    
    Sortie:
        - Une matrice (np.array) correspondant au système d'équations.
    """
    
   
    mat = np.array([[2,-5,3],[3,-1,4],[1,3,2]])
    
    return mat

# Fonction pour construire le membre de droite du système d'équations
def faire_second_membre():
    """Fonction qui génère le second membre pour le système d'équations suivant:
        2x - 5y + 3z = 8
        3x -  y + 4z = 7
         x + 3y + 2z = -3 

    Sortie:
        - Un np.array array contenant 3 nombres
    """


    b = np.array([8,7,-3])

    return b
    
# Printer la solution du syteme d'équation
print(np.linalg.solve(faire_matrice(),faire_second_membre()))
