import generer_prime as Gen
import euclide_etendu as EE

def gen_rsa_keys(length,e=65537):
    """
    Génère les clés RSA : la clé publique (e, n) et la clé privée (d, n).
    
    Arguments : 
    - length : Taille (en nombre de chiffres) des nombres premiers p et q.
    - e : Exposant public (par défaut, 65537, une valeur couramment utilisée en RSA).

    Retourne :
    - (e, d, n) où :
      - e : Exposant public
      - d : Exposant privé
      - n : Module (produit de deux nombres premiers)
    """
    
     
    while True:
        # Génération de deux nombres premiers p et q
        p=int(Gen.gen_prime(length)) # Génération d'un nombre premier de la taille spécifiée
        q=int(Gen.gen_prime(length)) # Génération d'un autre nombre premier de la même taille
        n=p*q # Calcul du module n (produit des deux nombres premiers)
        phi=(p-1)*(q-1)  # Calcul de φ(n) = (p - 1) * (q - 1)
        # Vérification que e est copremier avec φ(n) (PGCD(e, φ(n)) = 1)
        if EE.egcd(e,phi)[0] == 1:
            break

    # Calcul de l'exposant privé d tel que (d * e) % φ(n) = 1
    d=EE.modinv(e,phi)
    return(e,d,n)  # Retourne les clés RSA

#print(gen_rsa_keys(3))