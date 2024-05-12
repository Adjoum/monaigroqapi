# Utilisez l'image de base Python
FROM python:3.12

# Créer un conteneur appelé ici app
WORKDIR /app
# Copiez les fichiers de votre projet dans le conteneur
COPY . /app

# Installez les dépendances
RUN pip install -r requirements.txt

# Exposez le port 8501 (port par défaut pour Streamlit)
EXPOSE 8506

# Commande pour exécuter votre application Streamlit
CMD ["streamlit", "run", "main.py"]
