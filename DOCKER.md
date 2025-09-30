# Guide Docker - Bibliothèque en Ligne

Ce guide explique comment utiliser Docker pour déployer l'application de gestion de bibliothèque.

## 📋 Prérequis

- Docker installé sur votre machine ([Télécharger Docker](https://www.docker.com/get-started))
- Docker Compose (généralement inclus avec Docker Desktop)

## 🚀 Démarrage rapide

### 1. Construction de l'image Docker

```bash
cd web_library
docker-compose build
```

### 2. Lancement de l'application

```bash
docker-compose up
```

L'application sera accessible sur : **http://localhost:8000**

### 3. Lancement en arrière-plan

```bash
docker-compose up -d
```

### 4. Arrêt de l'application

```bash
docker-compose down
```

## 🔧 Commandes utiles

### Créer un superutilisateur

```bash
docker-compose exec web python manage.py createsuperuser
```

### Appliquer les migrations

```bash
docker-compose exec web python manage.py migrate
```

### Collecter les fichiers statiques

```bash
docker-compose exec web python manage.py collectstatic --noinput
```

### Voir les logs

```bash
docker-compose logs -f web
```

### Accéder au shell Django

```bash
docker-compose exec web python manage.py shell
```

### Accéder au conteneur

```bash
docker-compose exec web bash
```

### Redémarrer le conteneur

```bash
docker-compose restart web
```

## 📁 Structure Docker

### Dockerfile
Construit l'image Docker avec :
- Python 3.13-slim comme base
- Installation des dépendances système pour Pillow
- Installation des packages Python
- Configuration des dossiers static et media
- Script d'entrée pour les migrations automatiques

### docker-compose.yml
Définit le service web avec :
- Port 8000 exposé
- Volumes pour le code, static et media
- Variables d'environnement depuis .env
- Configuration du réseau

### .dockerignore
Exclut les fichiers inutiles du build Docker :
- Environnement virtuel (venv)
- Base de données de développement
- Fichiers cache Python
- Fichiers IDE

## 🔄 Workflow de développement

1. **Modifier le code** : Les modifications sont synchronisées automatiquement grâce au volume monté
2. **Redémarrer si nécessaire** : `docker-compose restart web`
3. **Nouvelles dépendances** : Reconstruire l'image avec `docker-compose build`

## 🌐 Variables d'environnement

Dans `docker-compose.yml`, vous pouvez modifier :

```yaml
environment:
  - DEBUG=True
  - DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,[::1],*
```

Pour la production, créez un fichier `.env` :

```env
DEBUG=False
SECRET_KEY=votre-cle-secrete-ici
DJANGO_ALLOWED_HOSTS=votre-domaine.com,www.votre-domaine.com
```

## 📦 Volumes Docker

Les volumes persistants stockent :
- **static_volume** : Fichiers statiques (CSS, JS)
- **media_volume** : Fichiers uploadés (couvertures de livres)

Pour supprimer les volumes :

```bash
docker-compose down -v
```

## 🐛 Dépannage

### Le port 8000 est déjà utilisé

Modifiez le port dans `docker-compose.yml` :
```yaml
ports:
  - "8080:8000"  # Utilise le port 8080 au lieu de 8000
```

### Les modifications ne sont pas prises en compte

1. Reconstruire l'image : `docker-compose build`
2. Redémarrer : `docker-compose up`

### Erreur de permission sur les fichiers

```bash
docker-compose exec web chown -R $(id -u):$(id -g) /app
```

### Réinitialiser complètement

```bash
docker-compose down -v
docker-compose build --no-cache
docker-compose up
```

## 🚢 Déploiement en production

Pour la production, utilisez la configuration complète avec PostgreSQL et Nginx :

### 1. Configuration de production

Le projet inclut des fichiers spécifiques pour la production :
- `Dockerfile.prod` : Image optimisée avec Gunicorn
- `docker-compose.prod.yml` : Stack complète (Django + PostgreSQL + Nginx)
- `nginx.conf` : Configuration Nginx
- `requirements-prod.txt` : Dépendances de production

### 2. Variables d'environnement de production

Créez un fichier `.env.prod` :

```env
DEBUG=False
SECRET_KEY=votre-cle-secrete-tres-longue-et-complexe
DJANGO_ALLOWED_HOSTS=votre-domaine.com,www.votre-domaine.com
POSTGRES_DB=library_db
POSTGRES_USER=library_user
POSTGRES_PASSWORD=mot-de-passe-securise
DATABASE_URL=postgresql://library_user:mot-de-passe-securise@db:5432/library_db
```

### 3. Lancer en production

```bash
# Construire les images
docker-compose -f docker-compose.prod.yml build

# Démarrer les services
docker-compose -f docker-compose.prod.yml up -d

# Créer un superutilisateur
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
```

### 4. Stack de production

La configuration production inclut :
- **PostgreSQL** : Base de données robuste
- **Gunicorn** : Serveur WSGI performant (3 workers)
- **Nginx** : Reverse proxy et serveur de fichiers statiques
- **Volumes persistants** : Données, static, media

### 5. Sécurité en production

⚠️ **Important avant le déploiement :**

1. Changez `SECRET_KEY` dans `.env.prod`
2. Utilisez des mots de passe forts pour PostgreSQL
3. Configurez `ALLOWED_HOSTS` avec vos vrais domaines
4. Activez HTTPS avec Let's Encrypt
5. Limitez les permissions des volumes Docker

### 6. Commandes de production

```bash
# Voir les logs
docker-compose -f docker-compose.prod.yml logs -f

# Arrêter les services
docker-compose -f docker-compose.prod.yml down

# Backup de la base de données
docker-compose -f docker-compose.prod.yml exec db pg_dump -U library_user library_db > backup.sql

# Restaurer la base de données
docker-compose -f docker-compose.prod.yml exec -T db psql -U library_user library_db < backup.sql
```

## 📚 Ressources

- [Documentation Docker](https://docs.docker.com/)
- [Documentation Django avec Docker](https://docs.djangoproject.com/en/5.2/howto/deployment/)
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)

## ✅ Vérification de l'installation

Testez que tout fonctionne :

```bash
# 1. Construire et démarrer
docker-compose up -d

# 2. Vérifier les logs
docker-compose logs web

# 3. Créer un superutilisateur
docker-compose exec web python manage.py createsuperuser

# 4. Accéder à l'application
# http://localhost:8000
```

## 🎯 Commandes courantes résumées

| Commande | Description |
|----------|-------------|
| `docker-compose build` | Construire l'image |
| `docker-compose up` | Démarrer les services |
| `docker-compose up -d` | Démarrer en arrière-plan |
| `docker-compose down` | Arrêter les services |
| `docker-compose logs -f` | Voir les logs en temps réel |
| `docker-compose exec web bash` | Accéder au shell du conteneur |
| `docker-compose restart` | Redémarrer les services |
| `docker-compose ps` | Voir l'état des conteneurs |
