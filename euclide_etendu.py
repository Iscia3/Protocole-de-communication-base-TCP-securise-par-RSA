def egcd(a, b):
    """
    Implémente l'algorithme d'Euclide étendu pour trouver le PGCD de deux nombres
    et les coefficients de Bézout (x, y) tels que : a*x + b*y = gcd(a, b).
    
    Arguments :
    - a : Premier entier
    - b : Deuxième entier
    
    Retourne :
    - gcd : Le plus grand diviseur commun (PGCD) de a et b
    - x, y : Les coefficients de Bézout
    """
    # Initialisation des coefficients pour l'algorithme
    x,y, u,v = 0,1, 1,0

    # Boucle jusqu'à ce que a devienne 0
    while a != 0:
        q, r = b//a, b%a  # Calcul du quotient et du reste
        m, n = x-u*q, y-v*q # Mise à jour des coefficients
        b,a, x,y, u,v = a,r, u,v, m,n # Mise à jour des valeurs
    gcd = b # Le PGCD est la dernière valeur non nulle de b
    return gcd, x, y # Le PGCD est la dernière valeur non nulle de b

def modinv(a, m):
    """
    Calcule l'inverse modulaire de a modulo m, c'est-à-dire x tel que (a * x) % m = 1.
    
    Arguments :
    - a : L'entier pour lequel on cherche l'inverse modulaire
    - m : Le module
    
    Retourne :
    - L'inverse modulaire x si a et m sont copremiers (gcd(a, m) = 1)
    - None si l'inverse modulaire n'existe pas
    """
    gcd, x, y = egcd(a, m)  # Appelle egcd pour obtenir le PGCD et les coefficients
    if gcd != 1:
        return None # Si gcd(a, m) ≠ 1, l'inverse modulaire n'existe pas
    return x % m # Retourne x modulo m pour s'assurer que le résultat est positif