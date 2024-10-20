# Importation des modules
import numpy as np


def residu(x,prm):
    """Fonction calculant le résidu du système d'équations
    
    Entrées :
        - x : Vecteur (array ou list) des estimés initiaux
            - x[0] : Vitesse d'entrée (boyau) [m/s]
            - x[1] : Vitesse de sortie (propulseur) [m/s]
            - x[2] : Angle d'inclinaison des propulseurs [rad]
        - prm : objet class parametres()
            - g : accélération gravitationnelle [m/s^2]
            - rho : masse volumique [kg/m^3]
            - D_e : diamètre d'entrée [m]
            - D_s : diamètre de sortie [m]
            - m : masse [kg]
            - F : force du vent [N]
    
    Sortie :
        - Vecteur (array) contenant les résidus
            - vecteur[0] : bilan de force par rapport à la verticale
            - vecteur[1] : bilan de force par rapport à l'horizontale
            - vecteur[2] : bilan de masse qui relie les 2 vitesses
            
    NB: - Simplifiez le bilan de masse pour qu'il ne soit fonction que des vitesses et des surfaces
    
    """
    residu = np.empty([3,])
    residu[0] = (np.pi/2)*prm.rho*(prm.D_s)**2*x[1]**2*np.cos(x[2]) + (np.pi/4)*prm.rho*prm.D_e**2*x[0]**2 - prm.m*prm.g
    residu[1] = -(np.pi/2)*prm.rho*prm.D_s**2*x[1]**2*np.sin(x[2]) + prm.F
    residu[2] = -x[0]*prm.D_e**2 + 2*x[1]*prm.D_s**2
    
    return residu

def newton_numerique(x,tol,prm):
    """Fonction résolvant le système d'équations avec la méthode de Newton et un jacobien numérique
    
    Entrées :
        - x : Vecteur (array ou list) des estimés initiaux
            - x[0] : Vitesse d'entrée (boyau) [m/s]
            - x[1] : Vitesse de sortie (propulseur) [m/s]
            - x[2] : Angle d'inclinaison des propulseurs [rad]
        - tol : critère d'arrêt
        - prm : objet class parametres()
            - g : accélération gravitationnelle [m/s^2]
            - rho : masse volumique [kg/m^3]
            - D_e : diamètre d'entrée [m]
            - D_s : diamètre de sortie [m]
            - m : masse [kg]
            - F : force du vent [N]
    
    Sortie :
        - Vecteur (array) contenant les solutions
            - vecteur[0] : solution de la vitesse d'entrée [m/s]
            - vecteur[1] : solution de la vitesse de sortie [m/s]
            - vecteur[2] : solution de la vitesse de l'angle d'inclinaison [rad]
    """
    #Faire le Jacobien
  
    N = 100
    
    h = tol
    delta = 1
    n = 0 
    while np.linalg.norm(delta) > tol and n < N:
        R = residu(x, prm)
        
        J = np.empty([3,3])
        for i in range(len(R)):
            x_p = np.copy(x)
            x_p[i] = x_p[i]+h
            R_p = residu(x_p,prm)
            J[i] = np.subtract(R_p,R)/h
        delta = np.linalg.solve(J.T, np.negative(R))
        x = x + delta
        n = n + 1

    return x