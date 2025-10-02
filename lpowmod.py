def lpowmod(x, y, n):
    """
    Calcul de la puissance modulaire : (x ** y) % n, où x, y, et n sont des entiers.
    
    Args:
        x (int): Base de la puissance.
        y (int): Exposant.
        n (int): Modulo.
    
    Returns:
        int: Résultat de (x ** y) % n.
    """
    result = 1  # Initialisation du résultat à 1 (élément neutre de la multiplication)
    while y>0: # Tant que l'exposant y n'est pas réduit à 0
        if y&1>0: # Vérifie si le bit de poids faible de y est 1 (y est impair)
            result = (result*x)%n  # Multiplie result par x modulo n
        y >>= 1 # Décale les bits de y d'une position vers la droite (division par 2)
        x = (x*x)%n # Remplace x par son carré modulo n
    return result  # Retourne le résultat final