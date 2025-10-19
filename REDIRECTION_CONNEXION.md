# Système de Redirection Intelligente

## 🎯 Fonctionnement

Le système de connexion redirige automatiquement les utilisateurs vers la page appropriée selon leur **type de compte** et leur **intention de navigation**.

---

## 📋 Logique de Redirection

### 1. **Connexion avec Page Demandée** (Paramètre `next`)

Quand un utilisateur non connecté tente d'accéder à une page protégée (ex: `/dashboard/`), il est redirigé vers `/login/?next=/dashboard/`.

Après connexion :
```
✅ Si l'utilisateur a les permissions → Redirigé vers la page demandée
❌ Si l'utilisateur n'a pas les permissions → Redirigé vers l'accueil avec message d'avertissement
```

**Exemple :**
```
Utilisateur étudiant essaie d'accéder à /dashboard/
    ↓
Redirigé vers /login/?next=/dashboard/
    ↓
Se connecte
    ↓
❌ N'est pas bibliothécaire
    ↓
Message : "Vous n'avez pas accès à cette page"
    ↓
Redirigé vers /home/
```

### 2. **Connexion Directe** (Sans paramètre `next`)

Quand un utilisateur se connecte directement via `/login/` :

| Type d'Utilisateur | Redirection | URL |
|-------------------|-------------|-----|
| **Bibliothécaire** | Dashboard | `/dashboard/` |
| **Admin / Staff** | Dashboard | `/dashboard/` |
| **Étudiant** | Accueil | `/` |
| **Professeur** | Accueil | `/` |
| **Personnel** | Accueil | `/` |

---

## 🔐 Vérifications de Permissions

Le système vérifie les permissions pour les pages protégées :

### Pages Réservées aux Bibliothécaires :
- `/dashboard/` - Tableau de bord
- `/books/add/` - Ajouter un livre
- `/books/<id>/edit/` - Modifier un livre
- `/books/<id>/delete/` - Supprimer un livre
- `/loans/create/` - Créer un emprunt
- `/loans/<id>/return/` - Retourner un livre

### Pages Accessibles à Tous (Connectés) :
- `/books/` - Liste des livres
- `/books/<id>/` - Détails d'un livre
- `/books/<id>/borrow/` - Emprunter (si autorisé)
- `/my-loans/` - Mes emprunts
- `/loans/` - Liste des emprunts (filtré selon permissions)

---

## 💻 Exemples de Scénarios

### Scénario 1 : Bibliothécaire se connecte

```
1. Visite : http://localhost:8000/login/
2. Entre ses identifiants
3. ✅ Connexion réussie
4. → Redirigé automatiquement vers /dashboard/
```

### Scénario 2 : Étudiant se connecte

```
1. Visite : http://localhost:8000/login/
2. Entre ses identifiants
3. ✅ Connexion réussie
4. → Redirigé automatiquement vers /home/
```

### Scénario 3 : Étudiant essaie d'accéder au dashboard

```
1. Visite : http://localhost:8000/dashboard/
2. ❌ Non connecté
3. → Redirigé vers /login/?next=/dashboard/
4. Entre ses identifiants
5. ✅ Connexion réussie
6. ⚠️ Vérification : N'est pas bibliothécaire
7. Message d'avertissement affiché
8. → Redirigé vers /home/
```

### Scénario 4 : Bibliothécaire essaie d'accéder au dashboard

```
1. Visite : http://localhost:8000/dashboard/
2. ❌ Non connecté
3. → Redirigé vers /login/?next=/dashboard/
4. Entre ses identifiants
5. ✅ Connexion réussie
6. ✅ Vérification : Est bibliothécaire
7. → Redirigé vers /dashboard/ (page demandée)
```

### Scénario 5 : Étudiant essaie d'emprunter un livre

```
1. Visite : http://localhost:8000/books/5/borrow/
2. ❌ Non connecté
3. → Redirigé vers /login/?next=/books/5/borrow/
4. Entre ses identifiants
5. ✅ Connexion réussie
6. ✅ Vérification : Peut emprunter
7. → Redirigé vers /books/5/borrow/ (page demandée)
8. Confirme l'emprunt
9. → Redirigé vers /my-loans/
```

---

## 🛠️ Implémentation Technique

### Vue de Connexion (`views.py`)

```python
def custom_login(request):
    """Connexion avec redirection intelligente"""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(...)
            login(request, user)
            
            # 1. Vérifier page demandée
            next_page = request.GET.get('next') or request.POST.get('next')
            
            if next_page:
                # Vérifier permissions pour pages protégées
                if 'dashboard' in next_page:
                    if user.profile.is_librarian():
                        return redirect(next_page)
                    else:
                        messages.warning(...)
                        return redirect('home')
                return redirect(next_page)
            
            # 2. Redirection par défaut selon type
            if user.profile.is_librarian():
                return redirect('dashboard')
            else:
                return redirect('home')
```

### Template de Connexion (`login.html`)

```html
<form method="post">
    {% csrf_token %}
    
    <!-- Conserver le paramètre next -->
    {% if request.GET.next %}
        <input type="hidden" name="next" value="{{ request.GET.next }}">
    {% endif %}
    
    <!-- Champs du formulaire -->
    ...
</form>
```

### Protection des Vues (`views.py`)

```python
@login_required
@user_passes_test(is_librarian)
def dashboard(request):
    """Accessible uniquement aux bibliothécaires"""
    ...
```

---

## 🔍 Débogage

### Vérifier le Type d'Utilisateur

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User

# Vérifier un utilisateur
user = User.objects.get(username='votre_username')
print(f"Username: {user.username}")
print(f"Has profile: {hasattr(user, 'profile')}")

if hasattr(user, 'profile'):
    print(f"User type: {user.profile.user_type}")
    print(f"Is librarian: {user.profile.is_librarian()}")
    print(f"Can borrow: {user.profile.can_borrow()}")

print(f"Is staff: {user.is_staff}")
print(f"Is superuser: {user.is_superuser}")
```

### Vérifier les Redirections

1. **Déconnectez-vous** : http://localhost:8000/logout/
2. **Essayez d'accéder au dashboard** : http://localhost:8000/dashboard/
3. **Vous devriez être redirigé vers** : http://localhost:8000/login/?next=/dashboard/
4. **Connectez-vous** avec un compte bibliothécaire
5. **Vous devriez être redirigé vers** : http://localhost:8000/dashboard/

---

## ⚙️ Configuration

### Settings.py

```python
# URLs de connexion/déconnexion
LOGIN_URL = 'login'              # Où rediriger si non connecté
LOGIN_REDIRECT_URL = 'home'      # Par défaut (surchargé par la logique)
LOGOUT_REDIRECT_URL = 'home'     # Après déconnexion
```

### URLs.py

```python
urlpatterns = [
    path('login/', views.custom_login, name='login'),  # Vue personnalisée
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
```

---

## 📊 Matrice des Redirections

| Depuis | Type Utilisateur | Destination | Remarque |
|--------|-----------------|-------------|----------|
| `/login/` | Bibliothécaire | `/dashboard/` | Redirection auto |
| `/login/` | Étudiant | `/home/` | Redirection auto |
| `/login/?next=/dashboard/` | Bibliothécaire | `/dashboard/` | Page demandée |
| `/login/?next=/dashboard/` | Étudiant | `/home/` | Permission refusée |
| `/login/?next=/books/5/borrow/` | Étudiant | `/books/5/borrow/` | Page demandée |
| `/dashboard/` (non connecté) | N/A | `/login/?next=/dashboard/` | Demande connexion |
| `/books/` (non connecté) | N/A | `/books/` | Page publique |
| `/logout/` | Tous | `/home/` | Après déconnexion |

---

## ✅ Tests de Validation

### Test 1 : Bibliothécaire
```
1. Se connecter comme bibliothécaire
2. ✅ Doit arriver sur /dashboard/
```

### Test 2 : Étudiant
```
1. Se connecter comme étudiant
2. ✅ Doit arriver sur /home/
```

### Test 3 : Protection du Dashboard
```
1. Se déconnecter
2. Aller sur /dashboard/
3. ✅ Doit être redirigé vers /login/?next=/dashboard/
4. Se connecter comme bibliothécaire
5. ✅ Doit arriver sur /dashboard/
```

### Test 4 : Refus d'Accès
```
1. Se déconnecter
2. Aller sur /dashboard/
3. Se connecter comme étudiant
4. ✅ Doit voir un message d'avertissement
5. ✅ Doit être redirigé vers /home/
```

---

## 🚀 Avantages du Système

1. **UX Améliorée** : Redirection automatique vers la page appropriée
2. **Sécurité** : Vérification des permissions avant redirection
3. **Flexibilité** : Gestion du paramètre `next` pour retour après connexion
4. **Feedback** : Messages clairs si accès refusé
5. **Intelligent** : S'adapte au type d'utilisateur

---

## 📝 Notes Importantes

- Les **superusers** et **staff** sont toujours redirigés vers le dashboard
- Les pages **publiques** restent accessibles sans connexion
- Le **paramètre next** est préservé dans le formulaire
- Les **messages d'erreur** sont affichés en cas de problème
- La **session** est conservée après redirection

---

**Date de création :** Octobre 2025  
**Version :** 1.0  
**Système :** Redirection intelligente selon profil utilisateur

