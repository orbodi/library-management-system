# Système de Gestion de Bibliothèque en Ligne

Un système complet de gestion de bibliothèque développé avec Django, permettant la gestion des livres, des utilisateurs et des emprunts.

## Fonctionnalités

### Pour tous les utilisateurs
- 🏠 Page d'accueil avec statistiques
- 📚 Catalogue de livres avec recherche avancée
- 🔍 Détails complets des livres
- 👤 Système d'authentification (inscription/connexion)

### Pour les étudiants, professeurs et personnel
- 📖 Consultation de leurs emprunts en cours
- 📜 Historique des emprunts
- ⏰ Alertes pour les retours en retard

### Pour les bibliothécaires
- ➕ Ajout de nouveaux livres
- ✏️ Modification et suppression de livres
- 📋 Gestion des emprunts (création et retour)
- 📊 Tableau de bord avec statistiques
- ⚠️ Suivi des emprunts en retard

## Technologies utilisées

- **Backend**: Django 5.2.6
- **Base de données**: SQLite (développement) / PostgreSQL (production)
- **Frontend**: Bootstrap 5.3, Bootstrap Icons
- **Images**: Pillow pour la gestion des couvertures de livres
- **Conteneurisation**: Docker & Docker Compose

## Installation

### Prérequis
- Python 3.8 ou supérieur
- pip (gestionnaire de packages Python)
- **OU** Docker et Docker Compose (pour déploiement containerisé)

### Option 1 : Installation avec Docker (Recommandé)

Consultez le fichier [DOCKER.md](DOCKER.md) pour le guide complet Docker.

**Démarrage rapide avec Docker :**

```bash
cd web_library

# Créer le fichier .env
.\setup-env.bat  # Windows
# ou
./setup-env.sh   # Linux/Mac

# Construire et démarrer
docker-compose up --build -d

# Créer un superutilisateur
docker-compose exec web python manage.py createsuperuser
```

L'application sera accessible sur http://localhost:8000

### Option 2 : Installation traditionnelle

1. **Activer l'environnement virtuel**
   ```bash
   # Windows
   ..\venv\Scripts\activate
   
   # Linux/Mac
   source ../venv/bin/activate
   ```

2. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

3. **Appliquer les migrations** (déjà fait normalement)
   ```bash
   python manage.py migrate
   ```

4. **Créer un superutilisateur** (administrateur/bibliothécaire)
   ```bash
   python manage.py createsuperuser
   ```
   Suivez les instructions pour créer votre compte administrateur.

5. **Lancer le serveur de développement**
   ```bash
   python manage.py runserver
   ```

6. **Accéder à l'application**
   - Application principale: http://127.0.0.1:8000/
   - Interface d'administration: http://127.0.0.1:8000/admin/

## Structure du projet

```
web_library/
├── manage.py
├── requirements.txt
├── README.md
├── DOCKER.md
├── Dockerfile
├── docker-compose.yml
├── .env (créé depuis env.example)
├── web_library/          # Configuration du projet
│   ├── settings.py       # Paramètres Django
│   ├── urls.py          # URLs principales
│   └── ...
├── website/             # Application principale
│   ├── models.py        # Modèles de données
│   ├── views.py         # Vues
│   ├── forms.py         # Formulaires
│   ├── admin.py         # Configuration admin
│   ├── urls.py          # URLs de l'application
│   ├── templates/       # Templates HTML
│   └── migrations/      # Migrations de base de données
├── static/              # Fichiers statiques (CSS, JS)
└── media/               # Fichiers uploadés (couvertures)
```

## Modèles de données

### UserProfile
Extension du modèle User de Django avec:
- Type d'utilisateur (Étudiant, Professeur, Personnel, Bibliothécaire)
- Matricule, Téléphone, Adresse

### Book
Gestion des livres:
- Informations bibliographiques (titre, auteur, ISBN, éditeur, année)
- Catégorie et description
- Image de couverture
- Quantité totale et disponible
- Statut (Disponible, Emprunté, En maintenance, Perdu)

### Loan
Gestion des emprunts:
- Livre emprunté, Emprunteur, Bibliothécaire
- Dates (emprunt, retour prévu, retour effectif)
- Statut (En cours, Retourné, En retard)

## Utilisation

### Première connexion

1. Créez un superutilisateur avec `python manage.py createsuperuser`
2. Connectez-vous à l'admin (http://127.0.0.1:8000/admin/)
3. Dans l'admin, créez un profil UserProfile pour votre superutilisateur avec le type "Bibliothécaire"

### Ajouter des livres

1. Connectez-vous avec un compte bibliothécaire
2. Cliquez sur "Ajouter un livre" dans le menu
3. Remplissez les informations du livre

### Créer un emprunt

1. En tant que bibliothécaire, accédez à "Créer un emprunt"
2. Sélectionnez le livre et l'emprunteur
3. Définissez la date de retour (par défaut: 14 jours)

### Retourner un livre

1. Accédez à la liste des emprunts ou au tableau de bord
2. Cliquez sur "Retourner" pour l'emprunt concerné
3. Confirmez le retour

## Types d'utilisateurs

- **STUDENT** (Étudiant): Peut emprunter des livres
- **TEACHER** (Professeur): Peut emprunter des livres
- **STAFF** (Personnel): Peut emprunter des livres
- **LIBRARIAN** (Bibliothécaire): Gère les livres et emprunts

## Configuration

### Variables d'environnement

Consultez [README-ENV.md](README-ENV.md) pour la configuration détaillée des variables d'environnement.

### Paramètres dans `settings.py`

- `LANGUAGE_CODE = 'fr-fr'`: Interface en français
- `TIME_ZONE = 'Africa/Douala'`: Fuseau horaire
- Durée d'emprunt par défaut: 14 jours

## Pages disponibles

- `/` - Page d'accueil avec statistiques
- `/books/` - Catalogue des livres
- `/books/<id>/` - Détails d'un livre
- `/login/` et `/register/` - Authentification
- `/my-loans/` - Mes emprunts
- `/dashboard/` - Tableau de bord (bibliothécaires)
- `/loans/` - Gestion des emprunts (bibliothécaires)
- `/admin/` - Interface d'administration Django

## Dépannage

### Port déjà utilisé
```bash
# Changer le port
python manage.py runserver 8080
```

### Erreurs de migration
```bash
python manage.py makemigrations
python manage.py migrate
```

### Problèmes avec les images
```bash
pip install Pillow
```

## Contribution

Pour contribuer au projet :
1. Fork le projet
2. Créez une branche (`git checkout -b feature/amelioration`)
3. Committez vos changements (`git commit -am 'Ajout fonctionnalité'`)
4. Push vers la branche (`git push origin feature/amelioration`)
5. Créez une Pull Request

## Licence

Projet éducatif - Tous droits réservés © 2025

## Auteur

Développé avec Django pour la gestion moderne de bibliothèques.

## Support

Pour toute question ou problème :
- Consultez la [documentation Django](https://docs.djangoproject.com/)
- Consultez [DOCKER.md](DOCKER.md) pour les questions Docker
- Consultez [README-ENV.md](README-ENV.md) pour la configuration



