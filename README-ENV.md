# Configuration des variables d'environnement

Ce guide explique comment configurer les variables d'environnement pour votre projet.

## 📋 Configuration initiale

### 1. Créer le fichier .env

**Windows :**
```bash
.\setup-env.bat
```

**Linux/Mac :**
```bash
chmod +x setup-env.sh
./setup-env.sh
```

**Ou manuellement :**
```bash
# Windows
copy env.example .env

# Linux/Mac
cp env.example .env
```

### 2. Modifier les valeurs

Ouvrez le fichier `.env` et modifiez les valeurs selon vos besoins :

```env
# Base de données
POSTGRES_DB=library_db
POSTGRES_USER=library_user
POSTGRES_PASSWORD=VotreMotDePasseSecurise123!

# Django
SECRET_KEY=votre-cle-secrete-unique-et-tres-longue
DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,[::1],*

# URL de connexion (doit correspondre aux credentials ci-dessus)
DATABASE_URL=postgresql://library_user:VotreMotDePasseSecurise123!@db:5432/library_db
```

## 🔐 Variables importantes

### Django

| Variable | Description | Exemple |
|----------|-------------|---------|
| `DEBUG` | Mode debug (True en dev, False en prod) | `True` |
| `SECRET_KEY` | Clé secrète Django (unique et complexe) | `django-insecure-...` |
| `DJANGO_ALLOWED_HOSTS` | Domaines autorisés | `localhost,127.0.0.1` |

### Base de données PostgreSQL

| Variable | Description | Exemple |
|----------|-------------|---------|
| `POSTGRES_DB` | Nom de la base de données | `library_db` |
| `POSTGRES_USER` | Utilisateur PostgreSQL | `library_user` |
| `POSTGRES_PASSWORD` | Mot de passe PostgreSQL | `monMotDePasse123!` |
| `DATABASE_URL` | URL complète de connexion | `postgresql://user:pass@db:5432/dbname` |

### Localisation

| Variable | Description | Exemple |
|----------|-------------|---------|
| `TIME_ZONE` | Fuseau horaire | `Africa/Douala` |
| `LANGUAGE_CODE` | Code de langue | `fr-fr` |

## 🐳 Utilisation avec Docker

Le fichier `docker-compose.yml` utilise automatiquement les variables du fichier `.env` :

```bash
# 1. Créer le fichier .env
.\setup-env.bat

# 2. Modifier les credentials si nécessaire
# Éditez .env avec votre éditeur

# 3. Lancer les conteneurs
docker-compose up -d
```

Les variables sont injectées dans les conteneurs via :
- `env_file: - .env` : Charge toutes les variables
- `${VARIABLE}` : Référence une variable spécifique

## ⚠️ Sécurité

### ✅ À faire

- ✅ Toujours utiliser `.env` pour les credentials
- ✅ Ajouter `.env` au `.gitignore` (déjà fait)
- ✅ Utiliser des mots de passe forts en production
- ✅ Changer `SECRET_KEY` pour chaque environnement
- ✅ Garder `env.example` à jour (sans vraies valeurs)

### ❌ À ne PAS faire

- ❌ Ne jamais commiter le fichier `.env`
- ❌ Ne jamais mettre de vrais credentials dans `env.example`
- ❌ Ne pas utiliser les mêmes mots de passe en dev et prod
- ❌ Ne pas partager votre `.env` publiquement

## 🔄 Environnements multiples

Vous pouvez créer différents fichiers d'environnement :

```bash
.env.local          # Développement local
.env.docker         # Docker développement
.env.production     # Production
```

Pour utiliser un fichier spécifique avec Docker :

```bash
docker-compose --env-file .env.production up -d
```

## 🧪 Validation

Pour vérifier que vos variables sont correctement chargées :

```bash
# Afficher la configuration (sans les valeurs sensibles)
docker-compose config

# Tester la connexion à la base de données
docker-compose exec web python manage.py dbshell
```

## 📝 Exemple complet

### Pour le développement local (SQLite)

```env
DEBUG=True
SECRET_KEY=dev-key-not-secure
DJANGO_ALLOWED_HOSTS=*
# Pas besoin de PostgreSQL en dev local
```

### Pour Docker (PostgreSQL)

```env
DEBUG=True
SECRET_KEY=docker-dev-key-change-in-production
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,[::1]

POSTGRES_DB=library_db
POSTGRES_USER=library_user
POSTGRES_PASSWORD=DevPassword123!

DATABASE_URL=postgresql://library_user:DevPassword123!@db:5432/library_db
```

### Pour la production

```env
DEBUG=False
SECRET_KEY=super-long-random-string-generated-securely
DJANGO_ALLOWED_HOSTS=votre-domaine.com,www.votre-domaine.com

POSTGRES_DB=library_db_prod
POSTGRES_USER=library_user_prod
POSTGRES_PASSWORD=SuperSecureProductionPassword2024!@#

DATABASE_URL=postgresql://library_user_prod:SuperSecureProductionPassword2024!@#@db:5432/library_db_prod

# Sécurité supplémentaire
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

## 🆘 Dépannage

### Le fichier .env n'est pas chargé

```bash
# Vérifier que le fichier existe
ls -la .env  # Linux/Mac
dir .env     # Windows

# Vérifier les permissions
chmod 644 .env  # Linux/Mac
```

### Variables non reconnues dans Docker

```bash
# Reconstruire avec le nouveau .env
docker-compose down
docker-compose up --build -d
```

### Erreur de connexion à la base de données

1. Vérifier que `DATABASE_URL` correspond à `POSTGRES_*`
2. Vérifier que les conteneurs sont démarrés : `docker-compose ps`
3. Vérifier les logs : `docker-compose logs db`

## 📚 Ressources

- [Django Settings](https://docs.djangoproject.com/en/5.2/ref/settings/)
- [Docker Compose Environment Variables](https://docs.docker.com/compose/environment-variables/)
- [12 Factor App - Config](https://12factor.net/config)
