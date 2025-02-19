# Scanner de vulnérabilités SSL/TLS

## Description
Ce projet est un scanner de vulnérabilités SSL/TLS développé en Python. Il permet d'analyser la configuration SSL/TLS d'un serveur cible, de détecter les vulnérabilités potentielles et de générer un rapport détaillé. De plus, il intègre une fonctionnalité de scan de ports ouverts en utilisant Nmap.

## Fonctionnalités
- Analyse de la configuration SSL/TLS d'un serveur
- Détection de protocoles obsolètes et de suites de chiffrement faibles
- Génération de rapports détaillés
- Scan des ports ouverts sur le serveur cible
- Recommandations pour améliorer la sécurité

## Diagramme de séquence
![alt text](images/Diagramme_sequence.png)

Acteurs principaux :

   -Utilisateur : Lance le scan et reçoit le rapport.
   -Scanner SSL/TLS : Exécute l'analyse et détecte les vulnérabilités.
   -Nmap : Scanne les ports ouverts.
   -Base de Données des Vulnérabilités : Fournit la liste des vulnérabilités connues.


## Prérequis
- Python 3.6+
- pip (gestionnaire de paquets Python)
- Nmap
- Docker (pour la conteneurisation)

## Installation de Nmap (Windows)
1. Téléchargez l'installateur Nmap pour Windows depuis le site officiel : https://nmap.org/download.html#windows
2. Exécutez l'installateur en tant qu'administrateur.
3. Suivez les instructions d'installation, en acceptant les options par défaut.
4. Une fois l'installation terminée, redémarrez votre invite de commande ou PowerShell.
5. Vérifiez l'installation en tapant `nmap --version` dans l'invite de commande

## Installation
1. Clonez ce dépôt :
   ```
   git clone https://github.com/ANANA1218/SSL-TLS.git
   cd SSL-TLS
   ```

2. Installez les dépendances requises :
   ```
   pip install -r requirements.txt
   ```

## Utilisation de ssl-tls-scanner
1. Assurez-vous que Nmap est correctement installé et accessible depuis la ligne de commande.
2. Exécutez le script principal :
   ```
   python ssl_tls_scanner.py
   ```

3. Suivez les instructions à l'écran pour entrer le nom de domaine et le port à scanner.

Exemple 1 :
![alt text](images/image.png)

Exemple 2 :

![alt text](images/image1.png)

4. Le script effectuera l'analyse et affichera les résultats dans la console.

## Utilisation de vulnerability_scanner
1. Assurez-vous que Nmap est correctement installé et accessible depuis la ligne de commande.
2. Exécutez le script principal :
   ```
   python vulnerability_scanner.py
   ```

3. Suivez les instructions à l'écran pour entrer le nom de domaine et le port à scanner.

Exemple 1 :

![alt text](images/scan1.png)

Exemple 2 :

![alt text](images/scan2.png)

4. Le script effectuera l'analyse et affichera les résultats dans la console.

## Conteneurisation avec Docker

### Prérequis
- Docker installé sur votre système

### Fichiers de configuration Docker
Vous aurez besoin de deux fichiers :
- `Dockerfile` : Définit l'environnement et les instructions pour construire l'image Docker.
- `docker-compose.yml` : Définit les services, les volumes et la configuration réseau pour l'application.

Consultez les exemples de `Dockerfile` et `docker-compose.yml` dans le dépôt.

### Construction et exécution du conteneur
1. Construisez l'image Docker :
   ```
   docker-compose build
   ```
Resultat au lancement de la commande :

![alt text](images/compose-build.png)

Resultat dans le docker desktop:

![alt text](images/docker-image.png)

2. Exécutez le conteneur :
   ```
   docker-compose up
   ```

Resultat au lancement de la commande :

![alt text](images/compose-up.png)

Resultat dans le docker desktop:

![alt text](images/up.png)

![alt text](images/console.png)

Ces commandes vont construire et lancer le conteneur Docker avec votre scanner SSL/TLS.

## Publication sur Docker Hub

1. **Créez un compte Docker Hub** : Si vous n'en avez pas déjà un, créez un compte sur [Docker Hub](https://hub.docker.com/).

2. **Connectez-vous à Docker Hub** depuis votre terminal :

   ```
   docker login
   ```

![alt text](images/)


3. **Taguez votre image** avec votre nom d'utilisateur Docker Hub :

   ```
   docker tag votre-image:tag votre-username/votre-repo:tag
   ```

![alt text](images/)

Remplacez `<image-id>` par l'ID de votre image Docker, `<votre-nom-d'utilisateur>` par votre nom d'utilisateur Docker Hub, `<nom-du-repo>` par le nom de votre repository, et `<tag>` par le tag de votre image (par exemple, `latest`).

4. **Poussez l'image** taguée vers Docker Hub :

   ```
   docker push votre-username/votre-repo:tag
   ```

![alt text](images/)


5. **Vérifiez la publication** : Sur le site Docker Hub, vérifiez que votre image a bien été publiée dans votre repository.

![alt text](images/)


## Test Unitaire 


## GitHub Action


## Avertissement
Ce scanner est conçu à des fins éducatives et de test. Assurez-vous d'avoir l'autorisation appropriée avant de scanner des systèmes qui ne vous appartiennent pas.
