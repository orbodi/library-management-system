# Utiliser Python 3.13 comme image de base
FROM python:3.13-slim

# Définir les variables d'environnement
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Créer et définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système nécessaires pour Pillow
RUN apt-get update && apt-get install -y \
    gcc \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Copier le fichier requirements.txt
COPY requirements.txt /app/

# Installer les dépendances Python
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copier le projet Django
COPY . /app/

# Créer les dossiers pour les fichiers statiques et média
RUN mkdir -p /app/static /app/media/book_covers

# Collecter les fichiers statiques
RUN python manage.py collectstatic --noinput || true

# Exposer le port 8000
EXPOSE 8000

# Créer un script d'entrée
RUN echo '#!/bin/bash\n\
python manage.py migrate --noinput\n\
python manage.py collectstatic --noinput\n\
exec python manage.py runserver 0.0.0.0:8000' > /app/entrypoint.sh

RUN chmod +x /app/entrypoint.sh

# Définir le script d'entrée comme commande par défaut
CMD ["/app/entrypoint.sh"]
