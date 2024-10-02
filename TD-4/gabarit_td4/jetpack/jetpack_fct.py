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
   # np.empty([3,1]) fonctionne pas avec la correction...
    residu = [0,0,0]
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
    df1_ve = 2*(np.pi/4)*prm.rho*prm.D_e**2*x[0]
    df1_vs = 2*(np.pi/2)*prm.rho*(prm.D_s)**2*x[1]*np.cos(x[2]) 
    df1_theta = -(np.pi/2)*prm.rho*(prm.D_s)**2*x[1]**2*np.sin(x[2])
       
    df2_ve = 0
    df2_vs = -2*(np.pi/2)*prm.rho*prm.D_s**2*x[1]*np.sin(x[2])
    df2_theta = -(np.pi/2)*prm.rho*prm.D_s**2*x[1]**2*np.cos(x[2])
       
    df3_ve = -prm.D_e**2
    df3_vs = 2*prm.D_s**2
    df3_theta = 0
       
    jacobien = np.empty([3,3])
    jacobien[0][0] = df1_ve 
    jacobien[0][1] = df1_vs
    jacobien[0][2] = df1_theta
    jacobien[1][0] = df2_ve 
    jacobien[1][1] = df2_vs
    jacobien[1][2] = df2_theta
    jacobien[2][0] = df3_ve 
    jacobien[2][1] = df3_vs
    jacobien[2][2] = df3_theta
    
    delta = np.linalg.solve(jacobien, residu(x,prm))
   
    while np.linalg.norm(delta) > tol :
        delta = np.linalg.solve(jacobien, residu(x,prm))
        x += delta
    
    return x
