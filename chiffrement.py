import rsa_key
import lpowmod

#Fonction de chiffrement
def encrypt(n, message :bytes,e) -> list[int]:
    """
    Chiffre un message en utilisant la clé publique (n, e).
    
    Args:
        n (int): Le modulo public.
        message (bytes): Le message à chiffrer sous forme d'octets.
        e (int): L'exposant public.
    
    Returns:
        list[int]: Liste des entiers représentant le message chiffré.
    """
    L=[] # Liste pour stocker les blocs chiffrés
    for b in message: # Parcours de chaque octet du message
        L.append(lpowmod.lpowmod(int(b),e,n))
    return L

#Fonction de déchiffrement
def decrypt(d, message_crypted:list[int],n) -> bytes: # la clée publique est un paramètre explicite
    """
    Déchiffre un message en utilisant la clé privée (n, d).
    
    Args:
        d (int): L'exposant privé.
        message_crypted (list[int]): Liste des entiers représentant le message chiffré.
        n (int): Le modulo public.
    
    Returns:
        bytes: Le message déchiffré sous forme d'octets.
    """
    result=b""  # Variable pour stocker le message déchiffré
    for b in message_crypted: # Parcours de chaque bloc chiffré
        B=lpowmod.lpowmod(int(b),d,n)  #Application de l'opération de déchiffrement : m = (c^d) mod n
        byte = B.to_bytes((B.bit_length()+7)//8,byteorder="big")  # Conversion de l'entier déchiffré en bytes
        result+=byte # Ajout du bloc déchiffré au résultat final
    return result

if __name__ == "__main__":   # Exemple d'utilisation des fonctions de chiffrement et de déchiffrement
#return result.decode("utf-8")
    #print(n,d,e)
    mot="oui" # Message à chiffrer
    print(mot.encode("utf-8"))  # Encodage du message en bytes (UTF-8)
    codee=encrypt(6140966077,mot.encode("utf-8"),65537) # Chiffrement du message avec la clé publique (n, e)
    print(codee) # Affiche le message chiffré sous forme de liste d'entiers
    code=decrypt(2668853717,codee,6140966077)  # Déchiffrement du message avec la clé privée (n, d)
    print(code.decode("utf-8"))  # Décodage du message déchiffré en chaîne de caractères