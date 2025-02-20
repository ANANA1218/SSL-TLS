# Utilise l'image de base Python 3.9 avec une version allégée (slim)
FROM python:3.9-slim

# Définit le répertoire de travail dans le conteneur
WORKDIR /app

# Copie le fichier requirements.txt dans le conteneur
COPY requirements.txt .

# Installe les dépendances Python listées dans requirements.txt
RUN pip install -r requirements.txt

# Copie tout le contenu du répertoire courant dans le conteneur
COPY . .

# Commande par défaut à exécuter lorsque le conteneur démarre
CMD ["python", "vulnerability_scanner.py"]
