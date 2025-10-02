#!/usr/bin/env python3
import json
import chiffrement
import rsa_key
import rsa_key
import lpowmod
import socket
import os, sys 

#Configuration du socket et connexion au serveur
socket_connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_connexion.connect(('127.0.0.1', 8790))  # Connexion au serveur sur l'adresse et le port spécifiés

#Génération des clées RSA du client
e, d_c, n_c=rsa_key.gen_rsa_keys(10)

# Préparation du dictionnaire contenant la clé publique
dico_key={"type": "key",
      "e":e,
      "n": n_c}


#envoi direct à la connexion de la clé,  Envoi immédiat de la clé publique au serveur
socket_connexion.sendall(json.dumps(dico_key).encode())

# Création d'un pipe pour la communication entre processus
r,w=os.pipe() #c'est ce qui va permettre de récupérer une donnée (la clé publique du serveur) du côté parent dans le côté enfant,  Permet l'échange de données entre le parent et l'enfant
pid = os.fork() #ce qui permet de faire un "chat" 
if pid:
    # parent,  Processus parent : reçoit et affiche les messages du serveur
    while 1:
        ligne = socket_connexion.recv(1024)  # Réception de données du serveur (taille max 1024 octets)
        dico_message_recu = json.loads(ligne) #json.loads pour dissocier les messages reçus,  Décodage des données reçues en dictionnaire JSON

        #print(dico_message_recu)
        if dico_message_recu["type"] == "message":
            message_crypted = dico_message_recu["data"] #chiffrement et envoi du message
           # print(message_crypted)
            dechiffre=chiffrement.decrypt(d_c,message_crypted,n_c) #dechiffrement du message
           # print(dechiffre)
            print(dechiffre.decode("utf-8"))

        elif dico_message_recu["type"] == "quit": #permet de quitter si le serveur quitte
            break
        
        elif dico_message_recu["type"]=="key":
            e_s=dico_message_recu["e"]  # Exposant public du serveur
            n_s=dico_message_recu["n"]  # Modulo public du serveur
            os.close(r)  # Fermeture de l'extrémité lecture du pipe
            texte=n_s.to_bytes((n_s.bit_length() + 7)// 8,"big") # Conversion de n_s en bytes
            os.write(w,texte) #permet d'écrire la valeur n_s reçue pour ensuite la récupérer dans l'enfant , Écriture de la clé publique reçue dans le pipe
            os.close(w) # Fermeture de l'extrémité écriture du pipe    
            print(ligne)
            
        if not ligne: # Si aucune donnée reçue, fin de la boucle
            break
        
else:
    # enfant, processus enfant: réception des données du serveur; reçoit les messages et les affiches après déchiffrement 

    os.close(w)
    recu=os.read(r,1024)
    os.close(r)
    
    while 1:        
        contenu = input(">>")  # Demande à l'utilisateur de saisir un message

        if contenu == "quitter":
            # Si l'utilisateur tape "quitter", envoie un message de type "quit" au serveur
            dico_message={"type":"quit"}
            ligne=json.dumps(dico_message)
            socket_connexion.sendall(ligne.encode('utf-8'))
            break

        n_s=int.from_bytes(recu, byteorder='big')  # Conversion de la clé publique reçue en entier
        message_crypted=chiffrement.encrypt(n_s,contenu.encode("utf-8"),e)  # Chiffrement du message
        #print(message_crypted)
        dico_message={"type":"message",
                        "data":message_crypted}
        ligne=json.dumps(dico_message) # Conversion du message en JSON

        if not contenu:  # Si aucun message n'est saisi, fin de la boucle
            break

        socket_connexion.sendall(ligne.encode('utf-8')) # Envoi du message chiffré au serveur

# Fermeture propre des processus et de la connexion
os.kill(pid, 9) #pour fermer proprement quand on veut quitter
socket_connexion.close() # fermeture de la connexion