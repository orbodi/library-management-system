# Guide Git - Bibliothèque en Ligne

Ce document explique comment utiliser Git pour ce projet.

## 🔧 Configuration initiale

### Configurer votre identité Git

```bash
git config user.name "Votre Nom"
git config user.email "votre.email@example.com"
```

### Voir la configuration

```bash
git config --list
```

## 📝 Workflow Git de base

### 1. Vérifier l'état des fichiers

```bash
git status
```

### 2. Ajouter des fichiers

```bash
# Ajouter tous les fichiers modifiés
git add .

# Ajouter un fichier spécifique
git add website/models.py

# Ajouter un dossier
git add website/
```

### 3. Créer un commit

```bash
git commit -m "Message descriptif du commit"
```

Exemples de messages :
```bash
git commit -m "Initial commit"
git commit -m "Ajout de la gestion des emprunts"
git commit -m "Fix: Correction du bug de redirection après login"
git commit -m "Feature: Ajout du tableau de bord bibliothécaire"
```

### 4. Voir l'historique

```bash
# Historique complet
git log

# Historique compact
git log --oneline

# Derniers 5 commits
git log -5

# Voir les changements d'un commit
git show <commit-hash>
```

## 🌿 Gestion des branches

### Créer et utiliser des branches

```bash
# Créer une nouvelle branche
git branch feature/nouvelle-fonctionnalite

# Changer de branche
git checkout feature/nouvelle-fonctionnalite

# Créer et changer de branche en une commande
git checkout -b feature/amelioration-ui

# Voir toutes les branches
git branch

# Revenir à la branche principale
git checkout main
```

### Fusionner des branches

```bash
# Se placer sur la branche de destination
git checkout main

# Fusionner une branche
git merge feature/nouvelle-fonctionnalite

# Supprimer une branche fusionnée
git branch -d feature/nouvelle-fonctionnalite
```

## 🔙 Annuler des modifications

### Annuler les modifications non commitées

```bash
# Annuler les modifications d'un fichier
git checkout -- website/views.py

# Annuler toutes les modifications
git checkout -- .

# Retirer un fichier de la staging area
git reset HEAD website/models.py
```

### Revenir à un commit précédent

```bash
# Voir l'historique
git log --oneline

# Revenir temporairement à un commit
git checkout <commit-hash>

# Revenir à la branche actuelle
git checkout main

# Annuler le dernier commit (garde les modifications)
git reset --soft HEAD~1

# Annuler le dernier commit (supprime les modifications)
git reset --hard HEAD~1
```

## 🌐 Travailler avec un dépôt distant (GitHub, GitLab, etc.)

### Ajouter un dépôt distant

```bash
# GitHub
git remote add origin https://github.com/username/repository.git

# GitLab
git remote add origin https://gitlab.com/username/repository.git
```

### Pousser vers le dépôt distant

```bash
# Première fois
git push -u origin main

# Pushes suivants
git push
```

### Récupérer les modifications

```bash
# Récupérer et fusionner
git pull

# Récupérer sans fusionner
git fetch
```

### Cloner un dépôt

```bash
git clone https://github.com/username/repository.git
```

## 📋 Fichiers ignorés

Le fichier `.gitignore` contient :

- `__pycache__/` - Cache Python
- `*.pyc` - Fichiers compilés Python
- `db.sqlite3` - Base de données locale
- `.env` - Variables d'environnement (IMPORTANT !)
- `media/` - Fichiers uploadés
- `staticfiles/` - Fichiers statiques collectés
- `venv/` - Environnement virtuel

**⚠️ IMPORTANT** : Ne jamais commiter :
- Le fichier `.env` (contient des mots de passe)
- La base de données `db.sqlite3` (contient des données utilisateurs)
- L'environnement virtuel `venv/`

## 🔍 Commandes utiles

### Voir les différences

```bash
# Différences non commitées
git diff

# Différences d'un fichier spécifique
git diff website/models.py

# Différences entre deux commits
git diff <commit1> <commit2>
```

### Rechercher dans l'historique

```bash
# Chercher dans les messages de commit
git log --grep="emprunt"

# Chercher qui a modifié une ligne
git blame website/models.py
```

### Nettoyer le dépôt

```bash
# Supprimer les fichiers non suivis
git clean -n  # Voir ce qui sera supprimé
git clean -f  # Supprimer effectivement
```

## 📦 Premier commit du projet

```bash
# 1. Vérifier les fichiers
git status

# 2. Ajouter tous les fichiers
git add .

# 3. Créer le premier commit
git commit -m "Initial commit: Système de gestion de bibliothèque complet

- Modèles: UserProfile, Book, Loan
- Vues: 14 vues (home, books, loans, dashboard, etc.)
- Templates: 13 templates HTML avec Bootstrap 5
- Admin: Interface admin complète
- Docker: Configuration Docker complète
- Documentation: README, DOCKER.md, README-ENV.md"

# 4. (Optionnel) Ajouter un dépôt distant
git remote add origin https://github.com/username/library-management.git

# 5. (Optionnel) Pousser vers GitHub
git push -u origin main
```

## 🏷️ Tags (versions)

### Créer des tags

```bash
# Tag simple
git tag v1.0.0

# Tag annoté (recommandé)
git tag -a v1.0.0 -m "Version 1.0.0 - Première release"

# Voir les tags
git tag

# Pousser un tag
git push origin v1.0.0

# Pousser tous les tags
git push --tags
```

## 🔄 Workflow recommandé

1. **Branche main** : Code stable, prêt pour la production
2. **Branche develop** : Code en développement
3. **Branches feature/** : Nouvelles fonctionnalités
4. **Branches fix/** : Corrections de bugs

```bash
# Créer une nouvelle fonctionnalité
git checkout -b feature/notifications
# ... développer ...
git add .
git commit -m "Feature: Ajout système de notifications"
git checkout main
git merge feature/notifications
git branch -d feature/notifications
```

## 📚 Bonnes pratiques

1. **Commits fréquents** : Committez régulièrement
2. **Messages clairs** : Utilisez des messages descriptifs
3. **Branches pour features** : Une branche par fonctionnalité
4. **Pull avant push** : Toujours récupérer les modifications avant de pousser
5. **Review avant merge** : Vérifier les changements avant de fusionner
6. **Ne pas commiter** :
   - Mots de passe ou clés API
   - Fichiers générés automatiquement
   - Données sensibles

## 🆘 Aide

```bash
# Aide générale
git help

# Aide sur une commande
git help commit
git help branch

# Version de Git
git --version
```

## 📖 Ressources

- [Documentation Git](https://git-scm.com/doc)
- [Git Book (français)](https://git-scm.com/book/fr/v2)
- [GitHub Guides](https://guides.github.com/)
- [GitLab Documentation](https://docs.gitlab.com/)

---

**Note** : Ce guide couvre les commandes Git de base. Pour des cas plus avancés, consultez la documentation officielle.
