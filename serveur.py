#!/usr/bin/env python3
import json
import rsa_key
import lpowmod
import chiffrement
import rsa_key
import socket
import os

# Création d'un socket en mode écoute
socket_attente = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
socket_attente.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #pour pouvoir réeutiliser le port après la fin de connexion , Permet de réutiliser le port immédiatement après la fin d'une connexion précédente
socket_attente.bind(('', 8790))  # Attache le socket au port 8790
socket_attente.listen(socket.SOMAXCONN)  # Écoute avec le nombre maximal de connexions en attente

# Acceptation de la connexion entrante
(socket_connectee, TSAP_client) = socket_attente.accept()
#print(TSAP_client)

#Génération des clés RSA pour le serveur
e, d_s, n_s=rsa_key.gen_rsa_keys(10) #récupération de la clé RSA pour le serveur

#print(d_s)

# Préparation de la clé publique du serveur sous forme de dictionnaire
dico_key={"type":"key",
          "e":e,
          "n":n_s}

# Création d'un pipe pour la communication entre processus parent et enfant
r,w=os.pipe() #c'est ce qui va permettre de récupérer une donnée (clé privée) du côté parent dans le côté enfant
pid = os.fork() #ce qui permet de faire un "chat" 

if pid:
    # parent, Code du processus parent : gestion des messages entrants du client
    while 1:
        
        ligne = socket_connectee.recv(1024) # Réception des données du client
        dico_message_recu = json.loads(ligne) # Décodage JSON des données reçues
        if dico_message_recu["type"]=="key": # Si le client envoie sa clé publique
            e_c=dico_message_recu["e"] # Récupération de l'exposant public
            n_c=dico_message_recu["n"]  # Récupération du module public
            os.close(r) #on ferme car on n'en a pas besoin ici, Fermeture du côté lecture du pipe
            texte=n_c.to_bytes((n_c.bit_length() + 7)// 8,"big") # Conversion en bytes
            os.write(w,texte) #permet d'écrire la valeur n_c reçue pour ensuite la récupérer dans l'enfant
            os.close(w) # Fermeture du côté écriture du pipe
            print(ligne) # Affichage des informations de la clé publique
            socket_connectee.sendall(json.dumps(dico_key).encode()) # Envoi de la clé publique du serveur

        elif dico_message_recu["type"] == "quit": #permet de quitter si le client quitte, Si le client envoie une commande de sortie
            break

        else: # Si le client envoie un message chiffré
            message_crypted = dico_message_recu["data"] #récupération du message du client,  Récupération du message chiffré
            #print(message_crypted)
            dechiffre=chiffrement.decrypt(d_s,message_crypted,n_s)  # Déchiffrement du message
            #print(dechiffre)
            print(dechiffre.decode('utf-8')) # Affichage du message déchiffré

        if not ligne: # Si aucune donnée n'est reçue, on sort de la boucle
            break

else:
    # enfant,  Si aucune donnée n'est reçue, on sort de la boucle
    os.close(w) #on n'a pas besoin d'écrire, Fermeture du côté écriture du pipe
    recu=os.read(r,1024) #on récupère la valeur reçue du parent,  Lecture des données du parent (clé publique du client)
    os.close(r) #on ferme car on n'en a plus besoin, Lecture des données du parent (clé publique du client)
   
    while 1:
        contenu = input(">>")  # Lecture des données du parent (clé publique du client)

        if contenu == "quitter": # Si l'utilisateur veut quitter
            dico_message={"type":"quit"}  # Préparation du message de sortie
            ligne=json.dumps(dico_message)
            socket_connectee.sendall(ligne.encode('utf-8')) # Envoi du message au client
            break

        n_c=int.from_bytes(recu, byteorder='big') #passage de bytes à int, Conversion de la clé publique du client en entier
        message_crypted=chiffrement.encrypt(n_c,contenu.encode("utf-8"),e) #chiffrement pour l'envoi au client
        #print(message_crypted)
        dico_message={"type":"message",
                        "data":message_crypted} # Préparation du message à envoyer
        ligne=json.dumps(dico_message)
    
        if not contenu: # Si aucun contenu n'est saisi, on sort de la boucle
            break

        socket_connectee.sendall(ligne.encode('utf8')) # Envoi du message au client

# Fermeture propre des processus et du socket
os.kill(pid, 9) #pour fermer proprement quand on veut quitter
socket_connectee.close() # Fermeture de la connexion avec le client