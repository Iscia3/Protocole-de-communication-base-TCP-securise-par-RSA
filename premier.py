import subprocess

def is_prime(n):
    """
    Vérifie si un nombre est premier en utilisant la commande OpenSSL.
    
    Args:
        n (int): Nombre entier à tester.
    
    Returns:
        bool: True si le nombre est premier, False sinon.
    """
    commande="openssl prime" #Commande OpenSSL pour tester la primalité
    # Exécution de la commande OpenSSL avec le nombre donné
    r= subprocess.run(commande+str(" ")+str(n),shell=True, stdout=subprocess.PIPE) # commande+str(" ")+str(n) : Construction de la commande complète, shell=True:
    # Permet l'utilisation d'une commande shell, stdout=subprocess.PIPE: # Capture la sortie standard de la commande 
    #pour recupérer la sortie d'une commande
    resultat_openssl= r.stdout.decode('utf-8') # Récupération de la sortie d'OpenSSL sous forme de chaîne

    # Vérification si la chaîne contient "not" (indiquant que le nombre n'est pas premier)
    if "not" in resultat_openssl:
        return False # Le nombre n'est pas premier
    else : 
        return True  # Le nombre est premier
    
#print("5",is_prime(5))