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
    position_x = []
    position_y = []
    i=0
    r=1 
    while i < n :
        x = np.random.uniform(-r,r)
        position_x.append(x)
        i+=1
    i=0
    while i < n :
        y = np.random.uniform(-r,r)
        position_y.append(y)
        i+=1
  
   
    return position_x, position_y


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
    r=1
    x2 = np.square(x)
    y2 = np.square(y)
    xy = np.add(x2,y2)
    N = len(xy)
    Nc= 0
    
    Nc = [i for i in xy if i <= 1]
   
    Pi = float((len(Nc)/N)*4)
            
    
    return Pi

pts_x = np.linspace(100, 10000+1, 100,dtype= int)

pts_erreur = np.empty(pts_x.shape)

for i in range(len(pts_x)) :
    
    xy = genXY(pts_x[i])
    erreur_absolue = abs(np.pi - monte_carlo(xy[0], xy[1]))
    pts_erreur[i] = erreur_absolue

# Créer le graphique
plt.plot(pts_x,pts_erreur, label = 'Erreur absolue')  
plt.legend()
plt.xlabel('Nombre de points') 
plt.ylabel('Erreur absolue')
plt.title("Évolution de l'erreur absolue selon le nombre de point")
    
    
    
    
    
    
    
    
    
    
