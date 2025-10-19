# Documentation Technique - Web Library Management System

## Table des Matières

1. [Introduction à Django](#1-introduction-à-django)
2. [Architecture Globale](#2-architecture-globale)
3. [Structure du Projet](#3-structure-du-projet)
4. [Les Modules Django](#4-les-modules-django)
5. [Guide Étape par Étape](#5-guide-étape-par-étape)
6. [Commandes Essentielles](#6-commandes-essentielles)
7. [Flux de Données](#7-flux-de-données)
8. [Bonnes Pratiques](#8-bonnes-pratiques)

---

## 1. Introduction à Django

### Qu'est-ce que Django ?

Django est un **framework web Python** qui suit le pattern **MVT** (Model-View-Template) :
- **Model** : Gère les données et la logique métier (base de données)
- **View** : Gère la logique de traitement des requêtes
- **Template** : Gère la présentation (HTML)

### Pourquoi Django ?

✅ Batteries incluses : admin, authentification, ORM
✅ Sécurité intégrée (CSRF, SQL Injection, XSS)
✅ Scalable et maintenable
✅ Grande communauté et documentation

---

## 2. Architecture Globale

```
┌─────────────┐      HTTP Request      ┌──────────────┐
│   Browser   │ ──────────────────────> │  Django URL  │
│   (Client)  │                         │   Routing    │
└─────────────┘                         └──────┬───────┘
      ↑                                        │
      │                                        ↓
      │                                 ┌──────────────┐
      │                                 │     View     │
      │                                 │  (Logique)   │
      │                                 └──────┬───────┘
      │                                        │
      │                                   ┌────┴────┐
      │                                   ↓         ↓
      │                            ┌──────────┐ ┌─────────┐
      │                            │  Model   │ │Template │
      │                            │   (DB)   │ │ (HTML)  │
      │                            └──────────┘ └─────┬───┘
      │                                               │
      └───────────────────────────────────────────────┘
                    HTTP Response (HTML)
```

### Flux d'une requête Django

1. **L'utilisateur** accède à une URL (ex: `/books/`)
2. **urls.py** analyse l'URL et route vers la bonne vue
3. **views.py** traite la requête :
   - Interroge les **models** (base de données)
   - Prépare les données (context)
   - Rend un **template**
4. **template** génère le HTML final
5. **Django** renvoie la réponse HTTP au navigateur

---

## 3. Structure du Projet

### Structure Complète

```
Web Library Management System/
│
├── venv/                          # Environnement virtuel Python
│
└── web_library/                   # Dossier racine du projet Django
    │
    ├── manage.py                  # Script de gestion Django
    │
    ├── web_library/               # Configuration du projet
    │   ├── __init__.py
    │   ├── settings.py            # Configuration globale
    │   ├── urls.py                # URLs racine du projet
    │   ├── wsgi.py                # Déploiement WSGI
    │   └── asgi.py                # Déploiement ASGI (async)
    │
    ├── website/                   # Application "website"
    │   ├── __init__.py
    │   ├── admin.py               # Interface d'administration
    │   ├── apps.py                # Configuration de l'app
    │   ├── models.py              # Modèles de données
    │   ├── views.py               # Logique de traitement
    │   ├── urls.py                # URLs de l'application
    │   ├── forms.py               # Formulaires Django
    │   ├── tests.py               # Tests unitaires
    │   ├── migrations/            # Migrations de base de données
    │   │   ├── __init__.py
    │   │   └── 0001_initial.py
    │   └── templates/             # Templates HTML
    │       └── website/
    │           ├── base.html
    │           ├── home.html
    │           ├── book_list.html
    │           └── ...
    │
    ├── static/                    # Fichiers statiques (CSS, JS, images)
    │   ├── css/
    │   └── js/
    │
    ├── media/                     # Fichiers uploadés par les utilisateurs
    │   └── book_covers/
    │
    ├── db.sqlite3                 # Base de données SQLite
    └── requirements.txt           # Dépendances Python
```

### Différence : Projet vs Application

#### Projet Django (`web_library/`)
- **Un seul par système**
- Contient la **configuration globale** (settings.py)
- Gère le **routing principal** (urls.py)
- Peut contenir **plusieurs applications**

#### Application Django (`website/`)
- **Plusieurs par projet**
- Module **réutilisable** avec une fonctionnalité spécifique
- Contient ses propres models, views, templates, urls
- Exemples : blog, boutique, forum, bibliothèque

---

## 4. Les Modules Django

### 4.1 Models (models.py)

**Rôle** : Définir la structure des données et interagir avec la base de données.

#### Concepts Clés

- **ORM** (Object-Relational Mapping) : Manipuler la DB avec du Python au lieu de SQL
- **Classe = Table** en base de données
- **Attribut = Colonne** de la table
- **Instance = Ligne** dans la table

#### Exemple : Modèle Book

```python
from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    """Modèle pour les livres"""
    
    # Types de champs
    title = models.CharField(max_length=200, verbose_name="Titre")
    author = models.CharField(max_length=200, verbose_name="Auteur")
    isbn = models.CharField(max_length=13, unique=True, verbose_name="ISBN")
    publication_year = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    cover_image = models.ImageField(upload_to='book_covers/', blank=True, null=True)
    quantity = models.IntegerField(default=1)
    
    # Relation ForeignKey (plusieurs livres -> un utilisateur)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    # Choix prédéfinis
    STATUS_CHOICES = [
        ('AVAILABLE', 'Disponible'),
        ('BORROWED', 'Emprunté'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='AVAILABLE')
    
    # Timestamps automatiques
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Livre"
        verbose_name_plural = "Livres"
        ordering = ['-created_at']  # Tri par défaut
    
    def __str__(self):
        """Représentation textuelle"""
        return f"{self.title} par {self.author}"
    
    def is_available(self):
        """Méthode personnalisée"""
        return self.available_quantity > 0
```

#### Types de Champs Courants

| Type | Usage | Exemple |
|------|-------|---------|
| `CharField` | Texte court | Nom, titre |
| `TextField` | Texte long | Description |
| `IntegerField` | Nombre entier | Âge, quantité |
| `DecimalField` | Nombre décimal | Prix |
| `BooleanField` | Vrai/Faux | is_active |
| `DateField` | Date | Date de naissance |
| `DateTimeField` | Date + heure | Horodatage |
| `EmailField` | Email | Email validé |
| `ImageField` | Image | Photo |
| `FileField` | Fichier | Document |
| `ForeignKey` | Relation 1-N | Livre -> Auteur |
| `OneToOneField` | Relation 1-1 | User -> Profil |
| `ManyToManyField` | Relation N-N | Livre <-> Tags |

#### Gestion des Quantités dans le Système

Le système gère intelligemment les quantités de livres avec deux champs :

```python
class Book(models.Model):
    quantity = models.IntegerField(default=1, verbose_name="Quantité totale")
    available_quantity = models.IntegerField(default=1, verbose_name="Quantité disponible")
    
    def borrowed_count(self):
        """Retourne le nombre d'exemplaires actuellement empruntés"""
        return self.quantity - self.available_quantity
    
    def borrow_book(self):
        """Décrémente la quantité disponible lors d'un emprunt"""
        if self.is_available():
            self.available_quantity -= 1
            if self.available_quantity == 0:
                self.status = 'BORROWED'
            self.save()
            return True
        return False
    
    def return_book(self):
        """Incrémente la quantité disponible lors d'un retour"""
        self.available_quantity += 1
        if self.available_quantity > 0:
            self.status = 'AVAILABLE'
        self.save()
```

**Logique de gestion automatique :**

1. **Ajout d'un nouveau livre** :
   - `quantity` = nombre d'exemplaires (ex: 5)
   - `available_quantity` = `quantity` (ex: 5)
   - Tous les exemplaires sont disponibles

2. **Emprunt d'un livre** :
   - `available_quantity` -= 1
   - Si `available_quantity` == 0 → `status` = 'BORROWED'
   - Exemple : 5 exemplaires → emprunt → 4 disponibles

3. **Retour d'un livre** :
   - `available_quantity` += 1
   - Si `available_quantity` > 0 → `status` = 'AVAILABLE'
   - Exemple : 4 disponibles → retour → 5 disponibles

4. **Modification de la quantité totale** :
   - **Augmentation** : nouveaux exemplaires ajoutés à `available_quantity`
     - Avant : quantity=5, available=3 (2 empruntés)
     - Modification : quantity=7
     - Après : available=5 (2 toujours empruntés)
   
   - **Réduction** : vérifie qu'on ne descend pas sous le nombre emprunté
     - Avant : quantity=5, available=3 (2 empruntés)
     - Modification : quantity=4 ✅ (OK, 2 empruntés)
     - Modification : quantity=1 ❌ (ERREUR, 2 déjà empruntés)

**Exemple pratique :**

```python
# Créer un livre avec 5 exemplaires
book = Book.objects.create(
    title="Python Avancé",
    author="John Doe",
    isbn="1234567890123",
    quantity=5,              # 5 exemplaires au total
    available_quantity=5     # 5 disponibles
)

# Emprunter un exemplaire
book.borrow_book()
# → quantity=5, available_quantity=4 (1 emprunté)

# Emprunter deux autres exemplaires
book.borrow_book()
book.borrow_book()
# → quantity=5, available_quantity=2 (3 empruntés)

# Retourner un exemplaire
book.return_book()
# → quantity=5, available_quantity=3 (2 empruntés)

# Ajouter 3 nouveaux exemplaires
book.quantity = 8
book.available_quantity = 6  # 3 nouveaux + 3 qui étaient disponibles
book.save()
# → quantity=8, available_quantity=6 (2 toujours empruntés)

# Vérifier les quantités
print(f"Total : {book.quantity}")                    # 8
print(f"Disponibles : {book.available_quantity}")    # 6
print(f"Empruntés : {book.borrowed_count()}")        # 2
```

#### Relations entre Modèles

```python
# 1. ForeignKey (Un-à-Plusieurs)
class Loan(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    # Un livre peut avoir plusieurs emprunts

# 2. OneToOneField (Un-à-Un)
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Un utilisateur a un seul profil

# 3. ManyToManyField (Plusieurs-à-Plusieurs)
class Book(models.Model):
    tags = models.ManyToManyField('Tag')
    # Un livre peut avoir plusieurs tags
    # Un tag peut être sur plusieurs livres
```

#### Options de `on_delete`

- `CASCADE` : Supprime en cascade (si book supprimé → loans supprimés)
- `SET_NULL` : Met à NULL (si user supprimé → added_by devient NULL)
- `PROTECT` : Empêche la suppression
- `SET_DEFAULT` : Met une valeur par défaut

---

### 4.2 Views (views.py)

**Rôle** : Contenir la logique métier et gérer les requêtes HTTP.

#### Types de Vues

##### 1. Function-Based Views (FBV)

```python
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Book
from .forms import BookForm

# Vue simple
def home(request):
    """Page d'accueil"""
    recent_books = Book.objects.filter(status='AVAILABLE')[:6]
    context = {
        'recent_books': recent_books,
    }
    return render(request, 'website/home.html', context)

# Vue avec recherche
def book_list(request):
    """Liste des livres avec filtre"""
    books = Book.objects.all()
    
    # Récupérer les paramètres GET
    query = request.GET.get('query', '')
    if query:
        books = books.filter(title__icontains=query)
    
    return render(request, 'website/book_list.html', {'books': books})

# Vue avec détail
def book_detail(request, pk):
    """Afficher un livre spécifique"""
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'website/book_detail.html', {'book': book})

# Vue protégée avec authentification
@login_required
def add_book(request):
    """Ajouter un livre (nécessite authentification)"""
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.added_by = request.user
            book.save()
            messages.success(request, f'Le livre "{book.title}" a été ajouté.')
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookForm()
    
    return render(request, 'website/book_form.html', {'form': form})

# Vue avec permission personnalisée
from django.contrib.auth.decorators import user_passes_test

def is_librarian(user):
    return user.is_authenticated and user.profile.is_librarian()

@login_required
@user_passes_test(is_librarian)
def dashboard(request):
    """Tableau de bord réservé aux bibliothécaires"""
    stats = {
        'total_books': Book.objects.count(),
        'available_books': Book.objects.filter(status='AVAILABLE').count(),
    }
    return render(request, 'website/dashboard.html', stats)
```

##### 2. Class-Based Views (CBV)

```python
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

# Liste
class BookListView(ListView):
    model = Book
    template_name = 'website/book_list.html'
    context_object_name = 'books'
    paginate_by = 10

# Détail
class BookDetailView(DetailView):
    model = Book
    template_name = 'website/book_detail.html'
    context_object_name = 'book'

# Création
class BookCreateView(LoginRequiredMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = 'website/book_form.html'
    success_url = reverse_lazy('book_list')
    
    def form_valid(self, form):
        form.instance.added_by = self.request.user
        return super().form_valid(form)
```

#### Méthodes HTTP

- **GET** : Récupérer des données (afficher une page)
- **POST** : Envoyer des données (soumettre un formulaire)
- **PUT/PATCH** : Modifier des données
- **DELETE** : Supprimer des données

```python
def my_view(request):
    if request.method == 'POST':
        # Traiter le formulaire
        pass
    else:  # GET
        # Afficher le formulaire
        pass
```

---

### 4.3 URLs (urls.py)

**Rôle** : Router les URLs vers les vues appropriées.

#### URLs du Projet (web_library/urls.py)

```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),           # Interface admin
    path('', include('website.urls')),         # Inclure les URLs de l'app
]

# Servir les fichiers media en développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

#### URLs de l'Application (website/urls.py)

```python
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Pages publiques
    path('', views.home, name='home'),                              # /
    path('books/', views.book_list, name='book_list'),              # /books/
    path('books/<int:pk>/', views.book_detail, name='book_detail'), # /books/5/
    
    # Authentification
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='website/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # CRUD Livres
    path('books/add/', views.add_book, name='add_book'),
    path('books/<int:pk>/edit/', views.edit_book, name='edit_book'),
    path('books/<int:pk>/delete/', views.delete_book, name='delete_book'),
    
    # Emprunts
    path('loans/', views.loan_list, name='loan_list'),
    path('loans/create/', views.create_loan, name='create_loan'),
    path('my-loans/', views.my_loans, name='my_loans'),
]
```

#### Patterns d'URL

| Pattern | Signification | Exemple URL |
|---------|---------------|-------------|
| `''` | URL vide (racine) | `/` |
| `'books/'` | URL fixe | `/books/` |
| `'<int:pk>/'` | Paramètre entier | `/books/5/` |
| `'<str:slug>/'` | Paramètre chaîne | `/books/django-tutorial/` |
| `'<slug:slug>/'` | Slug (URL-friendly) | `/books/mon-livre/` |
| `'<uuid:id>/'` | UUID | `/books/123e4567-e89b/` |

#### Nommage des URLs

Les URLs nommées permettent de générer des liens dynamiques :

```html
<!-- Dans les templates -->
<a href="{% url 'book_detail' pk=book.id %}">Voir le livre</a>
<a href="{% url 'home' %}">Accueil</a>

<!-- Dans les vues Python -->
from django.urls import reverse
url = reverse('book_detail', kwargs={'pk': 5})  # /books/5/
```

---

### 4.4 Templates (templates/)

**Rôle** : Générer le HTML dynamique envoyé au navigateur.

#### Structure des Templates

```
templates/
└── website/
    ├── base.html              # Template parent
    ├── home.html              # Hérite de base.html
    ├── book_list.html
    └── book_detail.html
```

#### Template de Base (base.html)

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Bibliothèque{% endblock %}</title>
    
    {% load static %}
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
    
    {% block extra_css %}{% endblock %}
</head>
<body>
    <!-- Navigation -->
    <nav>
        <ul>
            <li><a href="{% url 'home' %}">Accueil</a></li>
            <li><a href="{% url 'book_list' %}">Livres</a></li>
            
            {% if user.is_authenticated %}
                <li><a href="{% url 'my_loans' %}">Mes Emprunts</a></li>
                {% if user.profile.is_librarian %}
                    <li><a href="{% url 'dashboard' %}">Dashboard</a></li>
                {% endif %}
                <li><a href="{% url 'logout' %}">Déconnexion</a></li>
            {% else %}
                <li><a href="{% url 'login' %}">Connexion</a></li>
                <li><a href="{% url 'register' %}">Inscription</a></li>
            {% endif %}
        </ul>
    </nav>
    
    <!-- Messages Flash -->
    {% if messages %}
        <div class="messages">
            {% for message in messages %}
                <div class="alert alert-{{ message.tags }}">
                    {{ message }}
                </div>
            {% endfor %}
        </div>
    {% endif %}
    
    <!-- Contenu principal -->
    <main>
        {% block content %}{% endblock %}
    </main>
    
    <!-- Footer -->
    <footer>
        <p>&copy; 2025 Bibliothèque</p>
    </footer>
    
    {% block extra_js %}{% endblock %}
</body>
</html>
```

#### Template Enfant (home.html)

```html
{% extends 'website/base.html' %}

{% block title %}Accueil - Bibliothèque{% endblock %}

{% block content %}
<h1>Bienvenue à la Bibliothèque</h1>

<div class="stats">
    <p>Livres totaux : {{ total_books }}</p>
    <p>Livres disponibles : {{ available_books }}</p>
</div>

<h2>Livres Récents</h2>
<div class="book-grid">
    {% for book in recent_books %}
        <div class="book-card">
            {% if book.cover_image %}
                <img src="{{ book.cover_image.url }}" alt="{{ book.title }}">
            {% endif %}
            
            <h3>{{ book.title }}</h3>
            <p>Par {{ book.author }}</p>
            <p>
                <span class="badge {% if book.is_available %}badge-success{% else %}badge-danger{% endif %}">
                    {{ book.get_status_display }}
                </span>
            </p>
            
            <a href="{% url 'book_detail' pk=book.pk %}" class="btn">Voir détails</a>
        </div>
    {% empty %}
        <p>Aucun livre disponible.</p>
    {% endfor %}
</div>
{% endblock %}
```

#### Syntaxe des Templates Django

##### Variables

```html
{{ variable }}              <!-- Afficher une variable -->
{{ book.title }}            <!-- Attribut d'objet -->
{{ book.author|upper }}     <!-- Avec filtre -->
{{ user.get_full_name }}    <!-- Méthode (sans parenthèses) -->
```

##### Filtres

```html
{{ text|lower }}                    <!-- En minuscules -->
{{ text|upper }}                    <!-- En majuscules -->
{{ text|title }}                    <!-- Première lettre en majuscule -->
{{ text|truncatewords:10 }}         <!-- Tronquer à 10 mots -->
{{ date|date:"d/m/Y" }}             <!-- Formater une date -->
{{ number|floatformat:2 }}          <!-- Formater un nombre (2 décimales) -->
{{ value|default:"N/A" }}           <!-- Valeur par défaut si vide -->
{{ list|length }}                   <!-- Longueur d'une liste -->
{{ html|safe }}                     <!-- Ne pas échapper le HTML -->
```

##### Conditions

```html
{% if user.is_authenticated %}
    <p>Bienvenue {{ user.username }}</p>
{% elif user.is_anonymous %}
    <p>Veuillez vous connecter</p>
{% else %}
    <p>Statut inconnu</p>
{% endif %}

{% if book.is_available and user.profile.can_borrow %}
    <button>Emprunter</button>
{% endif %}
```

##### Boucles

```html
{% for book in books %}
    <li>{{ book.title }}</li>
{% empty %}
    <li>Aucun livre trouvé.</li>
{% endfor %}

<!-- Variables de boucle -->
{% for book in books %}
    <p>{{ forloop.counter }}. {{ book.title }}</p>  <!-- Index (commence à 1) -->
    {% if forloop.first %}<p>Premier élément</p>{% endif %}
    {% if forloop.last %}<p>Dernier élément</p>{% endif %}
{% endfor %}
```

##### Inclusion de Templates

```html
{% include 'website/book_card.html' %}
{% include 'website/book_card.html' with book=book %}
```

##### Fichiers Statiques

```html
{% load static %}

<link rel="stylesheet" href="{% static 'css/style.css' %}">
<script src="{% static 'js/main.js' %}"></script>
<img src="{% static 'images/logo.png' %}" alt="Logo">
```

---

### 4.5 Forms (forms.py)

**Rôle** : Gérer et valider les formulaires HTML.

#### Types de Formulaires

##### 1. ModelForm (basé sur un modèle)

```python
from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    """Formulaire pour créer/modifier un livre"""
    
    class Meta:
        model = Book
        fields = ['title', 'author', 'isbn', 'publisher', 'publication_year', 
                  'category', 'description', 'cover_image', 'quantity']
        
        # Personnaliser les widgets (apparence)
        widgets = {
            'description': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Description du livre...'
            }),
            'publication_year': forms.NumberInput(attrs={
                'min': 1900,
                'max': 2025
            }),
        }
        
        # Messages d'erreur personnalisés
        error_messages = {
            'title': {
                'required': 'Le titre est obligatoire.',
            },
        }
    
    # Validation personnalisée
    def clean_isbn(self):
        isbn = self.cleaned_data.get('isbn')
        if len(isbn) not in [10, 13]:
            raise forms.ValidationError('L\'ISBN doit contenir 10 ou 13 caractères.')
        return isbn
```

##### 2. Form (formulaire personnalisé)

```python
class BookSearchForm(forms.Form):
    """Formulaire de recherche de livres"""
    
    query = forms.CharField(
        max_length=200,
        required=False,
        label='Rechercher',
        widget=forms.TextInput(attrs={
            'placeholder': 'Titre, auteur, ISBN...',
            'class': 'form-control'
        })
    )
    
    category = forms.CharField(
        max_length=100,
        required=False,
        label='Catégorie'
    )
    
    STATUS_CHOICES = [
        ('', 'Tous'),
        ('AVAILABLE', 'Disponible'),
        ('BORROWED', 'Emprunté'),
    ]
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        required=False,
        label='Statut'
    )
```

#### Utilisation dans les Vues

```python
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)  # request.FILES pour les images
        if form.is_valid():
            book = form.save(commit=False)  # Ne pas sauvegarder immédiatement
            book.added_by = request.user    # Modifier avant sauvegarde
            book.save()                     # Sauvegarder maintenant
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookForm()
    
    return render(request, 'website/book_form.html', {'form': form})

def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookForm(instance=book)  # Pré-remplir le formulaire
    
    return render(request, 'website/book_form.html', {'form': form, 'book': book})
```

#### Affichage dans les Templates

```html
<form method="post" enctype="multipart/form-data">
    {% csrf_token %}
    
    <!-- Affichage automatique -->
    {{ form.as_p }}
    
    <!-- OU affichage manuel -->
    <div class="form-group">
        {{ form.title.label_tag }}
        {{ form.title }}
        {% if form.title.errors %}
            <span class="error">{{ form.title.errors }}</span>
        {% endif %}
    </div>
    
    <button type="submit">Enregistrer</button>
</form>
```

---

### 4.6 Admin (admin.py)

**Rôle** : Interface d'administration automatique de Django.

```python
from django.contrib import admin
from .models import Book, Loan, UserProfile

# Enregistrement simple
admin.site.register(UserProfile)

# Enregistrement personnalisé
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'isbn', 'status', 'available_quantity', 'created_at']
    list_filter = ['status', 'category', 'publication_year']
    search_fields = ['title', 'author', 'isbn']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = [
        ('Informations Principales', {
            'fields': ['title', 'author', 'isbn']
        }),
        ('Détails', {
            'fields': ['publisher', 'publication_year', 'category', 'description', 'cover_image']
        }),
        ('Disponibilité', {
            'fields': ['quantity', 'available_quantity', 'status']
        }),
        ('Metadata', {
            'fields': ['added_by', 'created_at', 'updated_at'],
            'classes': ['collapse']
        }),
    ]

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ['book', 'borrower', 'borrow_date', 'due_date', 'status']
    list_filter = ['status', 'borrow_date']
    search_fields = ['book__title', 'borrower__username']
    date_hierarchy = 'borrow_date'
    
    def get_queryset(self, request):
        """Optimiser les requêtes avec select_related"""
        qs = super().get_queryset(request)
        return qs.select_related('book', 'borrower', 'librarian')
```

**Accès** : `http://localhost:8000/admin/`

---

### 4.7 Migrations (migrations/)

**Rôle** : Versionner les changements de la base de données.

Les migrations sont des fichiers Python qui décrivent les changements à appliquer à la base de données.

#### Fichier de Migration (0001_initial.py)

```python
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    
    dependencies = []
    
    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('author', models.CharField(max_length=200)),
                # ...
            ],
        ),
    ]
```

---

## 5. Guide Étape par Étape

### 5.1 Installation et Configuration Initiale

#### Étape 1 : Installer Python

```bash
# Vérifier l'installation
python --version  # Python 3.10+ recommandé
```

#### Étape 2 : Créer un Environnement Virtuel

```bash
# Windows
python -m venv venv
activate         # Activer l'environnement

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### Étape 3 : Installer Django

```bash
pip install django pillow  # Pillow pour les images
pip freeze > requirements.txt  # Sauvegarder les dépendances
```

#### Étape 4 : Créer un Projet Django

```bash
django-admin startproject web_library
cd web_library
```

**Structure créée :**
```
web_library/
├── manage.py
└── web_library/
    ├── __init__.py
    ├── settings.py
    ├── urls.py
    ├── asgi.py
    └── wsgi.py
```

#### Étape 5 : Créer une Application

```bash
python manage.py startapp website
```

**Structure créée :**
```
website/
├── __init__.py
├── admin.py
├── apps.py
├── models.py
├── tests.py
└── views.py
```

#### Étape 6 : Enregistrer l'Application

**web_library/settings.py**
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'website',  # ← Ajouter ici
]
```

---

### 5.2 Créer des Modèles

#### Étape 1 : Définir les Modèles

**website/models.py**
```python
from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True)
    status = models.CharField(
        max_length=20,
        choices=[('AVAILABLE', 'Disponible'), ('BORROWED', 'Emprunté')],
        default='AVAILABLE'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
```

#### Étape 2 : Créer une Migration

```bash
python manage.py makemigrations
```

**Résultat :**
```
Migrations for 'website':
  website/migrations/0001_initial.py
    - Create model Book
```

#### Étape 3 : Appliquer la Migration

```bash
python manage.py migrate
```

**Résultat :**
```
Running migrations:
  Applying website.0001_initial... OK
```

#### Étape 4 : Interagir avec les Modèles (Shell Django)

```bash
python manage.py shell
```

```python
# Importer le modèle
from website.models import Book

# Créer un livre
book = Book.objects.create(
    title="Python pour les Nuls",
    author="John Doe",
    isbn="1234567890123"
)

# Récupérer tous les livres
books = Book.objects.all()

# Filtrer
available_books = Book.objects.filter(status='AVAILABLE')

# Récupérer un livre par ID
book = Book.objects.get(id=1)

# Modifier
book.status = 'BORROWED'
book.save()

# Supprimer
book.delete()

# Recherche avancée
books = Book.objects.filter(title__icontains='python')  # Contient "python"
books = Book.objects.filter(created_at__year=2025)      # Année 2025
books = Book.objects.exclude(status='BORROWED')         # Exclure empruntés
books = Book.objects.order_by('-created_at')            # Tri descendant
```

---

### 5.3 Créer des Vues

#### Étape 1 : Créer une Vue Simple

**website/views.py**
```python
from django.shortcuts import render
from .models import Book

def home(request):
    """Page d'accueil"""
    books = Book.objects.filter(status='AVAILABLE')[:6]
    context = {
        'books': books,
        'total_books': Book.objects.count(),
    }
    return render(request, 'website/home.html', context)

def book_list(request):
    """Liste de tous les livres"""
    books = Book.objects.all()
    return render(request, 'website/book_list.html', {'books': books})

def book_detail(request, pk):
    """Détails d'un livre"""
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'website/book_detail.html', {'book': book})
```

---

### 5.4 Configurer les URLs

#### Étape 1 : Créer les URLs de l'Application

**website/urls.py** (créer ce fichier)
```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('books/', views.book_list, name='book_list'),
    path('books/<int:pk>/', views.book_detail, name='book_detail'),
]
```

#### Étape 2 : Inclure dans les URLs du Projet

**web_library/urls.py**
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('website.urls')),  # ← Ajouter
]
```

---

### 5.5 Créer des Templates

#### Étape 1 : Créer la Structure

```bash
mkdir -p website/templates/website
```

#### Étape 2 : Template de Base

**website/templates/website/base.html**
```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}Bibliothèque{% endblock %}</title>
</head>
<body>
    <nav>
        <a href="{% url 'home' %}">Accueil</a>
        <a href="{% url 'book_list' %}">Livres</a>
    </nav>
    
    <main>
        {% block content %}{% endblock %}
    </main>
</body>
</html>
```

#### Étape 3 : Template Enfant

**website/templates/website/home.html**
```html
{% extends 'website/base.html' %}

{% block title %}Accueil{% endblock %}

{% block content %}
<h1>Bienvenue</h1>
<p>Total de livres : {{ total_books }}</p>

<div class="books">
    {% for book in books %}
        <div class="book-card">
            <h3>{{ book.title }}</h3>
            <p>{{ book.author }}</p>
            <a href="{% url 'book_detail' pk=book.pk %}">Détails</a>
        </div>
    {% endfor %}
</div>
{% endblock %}
```

**website/templates/website/book_list.html**
```html
{% extends 'website/base.html' %}

{% block content %}
<h1>Liste des Livres</h1>

<ul>
    {% for book in books %}
        <li>
            <a href="{% url 'book_detail' pk=book.pk %}">
                {{ book.title }} - {{ book.author }}
            </a>
        </li>
    {% empty %}
        <li>Aucun livre disponible.</li>
    {% endfor %}
</ul>
{% endblock %}
```

---

### 5.6 Créer des Formulaires

#### Étape 1 : Créer un ModelForm

**website/forms.py** (créer ce fichier)
```python
from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'isbn', 'status']
```

#### Étape 2 : Vue avec Formulaire

**website/views.py**
```python
from django.shortcuts import render, redirect
from .forms import BookForm

def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    
    return render(request, 'website/book_form.html', {'form': form})
```

#### Étape 3 : Template de Formulaire

**website/templates/website/book_form.html**
```html
{% extends 'website/base.html' %}

{% block content %}
<h1>Ajouter un Livre</h1>

<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Enregistrer</button>
</form>
{% endblock %}
```

#### Étape 4 : Ajouter l'URL

**website/urls.py**
```python
urlpatterns = [
    # ... URLs existantes
    path('books/add/', views.add_book, name='add_book'),
]
```

---

### 5.7 Configurer l'Admin

#### Étape 1 : Enregistrer les Modèles

**website/admin.py**
```python
from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'isbn', 'status']
    list_filter = ['status']
    search_fields = ['title', 'author', 'isbn']
```

#### Étape 2 : Créer un Superutilisateur

```bash
python manage.py createsuperuser
```

**Suivre les instructions :**
```
Username: admin
Email: admin@example.com
Password: ********
Password (again): ********
```

#### Étape 3 : Accéder à l'Admin

1. Lancer le serveur : `python manage.py runserver`
2. Aller sur : `http://localhost:8000/admin/`
3. Se connecter avec les identifiants créés

---

### 5.8 Configurer les Fichiers Statiques et Media

#### Étape 1 : Configuration dans settings.py

**web_library/settings.py**
```python
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Fichiers statiques (CSS, JS, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Pour la production
STATICFILES_DIRS = [BASE_DIR / 'static']  # Pour le développement

# Fichiers uploadés par les utilisateurs
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

#### Étape 2 : Créer les Dossiers

```bash
mkdir static
mkdir media
```

#### Étape 3 : Servir les Fichiers Media en Développement

**web_library/urls.py**
```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... URLs existantes
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

#### Étape 4 : Utiliser les Fichiers Statiques

**website/templates/website/base.html**
```html
{% load static %}

<link rel="stylesheet" href="{% static 'css/style.css' %}">
<script src="{% static 'js/main.js' %}"></script>
```

---

## 6. Commandes Essentielles

### Commandes de Base

```bash
# Lancer le serveur de développement
python manage.py runserver
python manage.py runserver 8080  # Sur un port spécifique

# Créer un nouveau projet
django-admin startproject nom_projet

# Créer une nouvelle application
python manage.py startapp nom_app

# Créer un superutilisateur
python manage.py createsuperuser
```

### Commandes de Base de Données

```bash
# Créer une migration après modification des models
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate

# Voir les migrations d'une app
python manage.py showmigrations website

# Annuler une migration (revenir à la migration 0002)
python manage.py migrate website 0002

# Voir le SQL d'une migration sans l'appliquer
python manage.py sqlmigrate website 0001

# Shell interactif Django
python manage.py shell

# Réinitialiser la base de données (ATTENTION : perte de données)
python manage.py flush
```

### Commandes de Gestion des Fichiers

```bash
# Collecter les fichiers statiques (pour la production)
python manage.py collectstatic

# Vérifier les problèmes du projet
python manage.py check

# Voir toutes les URLs du projet
python manage.py show_urls  # (nécessite django-extensions)
```

### Commandes de Test

```bash
# Lancer tous les tests
python manage.py test

# Lancer les tests d'une app spécifique
python manage.py test website

# Lancer un test spécifique
python manage.py test website.tests.BookTestCase
```

### Commandes Utiles

```bash
# Vider le cache
python manage.py clear_cache

# Exporter les données (backup)
python manage.py dumpdata > backup.json
python manage.py dumpdata website > website_backup.json

# Importer les données
python manage.py loaddata backup.json

# Créer des données de test
python manage.py shell
>>> from website.models import Book
>>> Book.objects.create(title="Test", author="Auteur", isbn="123")
```

---

## 7. Flux de Données

### Exemple 1 : Afficher la Liste des Livres

```
1. L'utilisateur visite : http://localhost:8000/books/

2. Django consulte web_library/urls.py
   ↓
   path('', include('website.urls'))
   
3. Django consulte website/urls.py
   ↓
   path('books/', views.book_list, name='book_list')
   
4. Django exécute website/views.py → book_list()
   ↓
   books = Book.objects.all()  # Requête à la base de données
   return render(request, 'website/book_list.html', {'books': books})
   
5. Django charge le template book_list.html
   ↓
   Remplace {{ books }} par les données
   
6. Django renvoie le HTML généré au navigateur
```

### Exemple 2 : Ajouter un Livre (avec Formulaire)

```
1. GET /books/add/
   ↓
   Vue : form = BookForm()
   Template : Affiche le formulaire vide
   
2. L'utilisateur remplit le formulaire et clique sur "Enregistrer"
   ↓
   POST /books/add/ avec les données
   
3. Vue : form = BookForm(request.POST, request.FILES)
   ↓
   if form.is_valid():  # Validation
       form.save()  # Sauvegarde en DB
       return redirect('book_list')
   
4. Redirection vers la liste des livres
```

### Exemple 3 : Emprunter un Livre (Processus Complet)

Le système d'emprunt dans cette application fonctionne selon deux modes :
- **Mode Utilisateur** : Les utilisateurs (étudiants, professeurs, personnel) peuvent emprunter directement
- **Mode Bibliothécaire** : Les bibliothécaires peuvent créer des emprunts pour n'importe quel utilisateur

#### A. Emprunt Direct par l'Utilisateur

```
┌─────────────────────────────────────────────────────────────────┐
│                    PROCESSUS D'EMPRUNT COMPLET                   │
└─────────────────────────────────────────────────────────────────┘

1. L'utilisateur consulte un livre
   GET /books/5/
   ↓
   Vue : book_detail(request, pk=5)
   ↓
   Template affiche :
   - Détails du livre
   - Bouton "Emprunter ce livre" (si disponible et user.profile.can_borrow())

2. L'utilisateur clique sur "Emprunter ce livre"
   GET /books/5/borrow/
   ↓
   Vue : borrow_book(request, pk=5)
   ↓
   Vérifications :
   ✓ Utilisateur authentifié (@login_required)
   ✓ Utilisateur peut emprunter (@user_passes_test(can_borrow))
   ✓ Livre disponible (book.is_available())
   ✓ Pas d'emprunt actif de ce livre par cet utilisateur
   ↓
   Template : borrow_confirm.html
   - Affiche les détails du livre
   - Conditions d'emprunt (durée : 14 jours)
   - Boutons "Confirmer" / "Annuler"

3. L'utilisateur confirme l'emprunt
   POST /books/5/borrow/
   ↓
   Vue : borrow_book(request, pk=5)
   ↓
   Création de l'emprunt :
   a) Loan.objects.create(
        book=book,
        borrower=request.user,
        borrow_date=now,
        due_date=now + 14 jours,
        status='ACTIVE'
      )
   
   b) book.borrow_book()  # Décrémente available_quantity
      ↓
      available_quantity -= 1
      if available_quantity == 0:
          status = 'BORROWED'
      book.save()
   
   c) messages.success("Emprunt confirmé")
   
   d) redirect('my_loans')

4. Redirection vers "Mes Emprunts"
   GET /my-loans/
   ↓
   Vue : my_loans(request)
   ↓
   Affiche :
   - Emprunts actifs/en retard
   - Historique des emprunts
```

#### B. Création d'Emprunt par le Bibliothécaire

```
1. Le bibliothécaire accède au formulaire
   GET /loans/create/
   ↓
   Vue : create_loan(request)
   Permissions : @user_passes_test(is_librarian)
   ↓
   LoanForm affiche :
   - Liste déroulante des livres disponibles
   - Liste déroulante des utilisateurs autorisés à emprunter
   - Date de retour prévue (pré-remplie : +14 jours)
   - Notes (optionnel)

2. Le bibliothécaire sélectionne le livre et l'emprunteur
   POST /loans/create/
   ↓
   form.is_valid()
   ↓
   loan = form.save(commit=False)
   loan.librarian = request.user  # Traçabilité
   
   if loan.book.is_available():
       loan.save()
       loan.book.borrow_book()
       redirect('loan_list')
   else:
       messages.error("Livre non disponible")
```

#### C. Retour d'un Livre

```
1. Le bibliothécaire consulte la liste des emprunts
   GET /loans/
   ↓
   Vue : loan_list(request)
   Affiche tous les emprunts (filtrés par statut si nécessaire)

2. Le bibliothécaire clique sur "Retourner"
   GET /loans/12/return/
   ↓
   Vue : return_book(request, loan_id=12)
   Permissions : @user_passes_test(is_librarian)
   ↓
   Template : loan_return_confirm.html
   - Détails de l'emprunt
   - Calcul des jours de retard (si applicable)
   - Confirmation

3. Confirmation du retour
   POST /loans/12/return/
   ↓
   loan.return_book()
   ↓
   a) loan.return_date = now
      loan.status = 'RETURNED'
      loan.save()
   
   b) loan.book.return_book()
      ↓
      book.available_quantity += 1
      if available_quantity > 0:
          book.status = 'AVAILABLE'
      book.save()
   
   c) messages.success("Livre retourné")
   d) redirect('loan_list')
```

#### D. Diagramme de Base de Données (Relations)

```
┌─────────────┐       ┌──────────────┐       ┌─────────────┐
│    User     │       │     Loan     │       │    Book     │
├─────────────┤       ├──────────────┤       ├─────────────┤
│ id (PK)     │───┐   │ id (PK)      │   ┌───│ id (PK)     │
│ username    │   │   │ book_id (FK) │───┘   │ title       │
│ email       │   │   │ borrower_id  │       │ author      │
│ ...         │   │   │ librarian_id │       │ isbn        │
└─────────────┘   │   │ borrow_date  │       │ quantity    │
                  │   │ due_date     │       │ available_* │
┌─────────────┐   │   │ return_date  │       │ status      │
│ UserProfile │   │   │ status       │       └─────────────┘
├─────────────┤   │   │ notes        │
│ id (PK)     │   │   └──────────────┘
│ user_id(FK) │───┤
│ user_type   │   └───── ForeignKey relations
│ matricule   │
│ phone       │
└─────────────┘

Relations:
- User ──< Loan (Un utilisateur peut avoir plusieurs emprunts)
- Book ──< Loan (Un livre peut être emprunté plusieurs fois)
- User ─── UserProfile (One-to-One : Un utilisateur a un profil)
```

#### E. Vérifications et Validations

**Avant de créer un emprunt :**
```python
# 1. Vérifier que le livre est disponible
if not book.is_available():
    # is_available() vérifie :
    # - available_quantity > 0
    # - status == 'AVAILABLE'
    return error

# 2. Vérifier que l'utilisateur peut emprunter
if not user.profile.can_borrow():
    # can_borrow() vérifie :
    # - user_type in ['STUDENT', 'TEACHER', 'STAFF']
    return error

# 3. Éviter les doublons (même livre déjà emprunté)
existing_loan = Loan.objects.filter(
    book=book,
    borrower=user,
    status__in=['ACTIVE', 'OVERDUE']
).exists()

if existing_loan:
    return warning("Vous avez déjà emprunté ce livre")
```

**Détection automatique des retards :**
```python
# Dans le modèle Loan.save()
if self.status == 'ACTIVE' and timezone.now() > self.due_date:
    self.status = 'OVERDUE'
```

#### F. Commandes pour Tester le Système d'Emprunt

```bash
# 1. Créer un utilisateur étudiant
python manage.py shell
```

```python
from django.contrib.auth.models import User
from website.models import UserProfile, Book, Loan
from django.utils import timezone
from datetime import timedelta

# Créer un utilisateur
user = User.objects.create_user(
    username='etudiant1',
    email='etudiant@example.com',
    password='password123',
    first_name='Jean',
    last_name='Dupont'
)

# Créer son profil
profile = UserProfile.objects.create(
    user=user,
    user_type='STUDENT',
    matricule='ETU2025001'
)

# Créer un livre
book = Book.objects.create(
    title='Django pour les débutants',
    author='John Doe',
    isbn='9781234567890',
    quantity=3,
    available_quantity=3,
    status='AVAILABLE'
)

# Créer un emprunt manuellement
loan = Loan.objects.create(
    book=book,
    borrower=user,
    borrow_date=timezone.now(),
    due_date=timezone.now() + timedelta(days=14),
    status='ACTIVE'
)

# Mettre à jour le livre
book.borrow_book()

# Vérifier
print(f"Emprunts actifs de {user.username}: {user.loans.filter(status='ACTIVE').count()}")
print(f"Exemplaires disponibles: {book.available_quantity}/{book.quantity}")
```

#### G. Permissions et Sécurité

**Matrice de Permissions :**

| Action | Anonyme | Étudiant | Professeur | Personnel | Bibliothécaire |
|--------|---------|----------|------------|-----------|----------------|
| Voir les livres | ✅ | ✅ | ✅ | ✅ | ✅ |
| Voir détails | ✅ | ✅ | ✅ | ✅ | ✅ |
| Emprunter | ❌ | ✅ | ✅ | ✅ | ❌ (crée pour autres) |
| Voir ses emprunts | ❌ | ✅ | ✅ | ✅ | ✅ (tous) |
| Créer emprunt (pour autres) | ❌ | ❌ | ❌ | ❌ | ✅ |
| Retourner un livre | ❌ | ❌ | ❌ | ❌ | ✅ |
| Ajouter/Modifier/Supprimer livre | ❌ | ❌ | ❌ | ❌ | ✅ |
| Dashboard | ❌ | ❌ | ❌ | ❌ | ✅ |

**Décorateurs utilisés :**
```python
@login_required  # Nécessite authentification
@user_passes_test(is_librarian)  # Réservé aux bibliothécaires
@user_passes_test(can_borrow)  # Réservé aux emprunteurs
```

---

## 8. Bonnes Pratiques

### 8.1 Structure du Projet

✅ **Un projet = Une application principale**
- Créer des apps modulaires et réutilisables
- Exemple : `blog`, `shop`, `forum`

✅ **Organisation des fichiers**
```
app/
├── models/
│   ├── __init__.py
│   ├── book.py
│   └── loan.py
├── views/
│   ├── __init__.py
│   ├── book_views.py
│   └── loan_views.py
└── templates/
    └── app/
        └── ...
```

### 8.2 Modèles

✅ **Utiliser `__str__` pour représentation lisible**
```python
def __str__(self):
    return self.title
```

✅ **Utiliser `Meta` pour les options**
```python
class Meta:
    ordering = ['-created_at']
    verbose_name = "Livre"
```

✅ **Ajouter des méthodes métier**
```python
def is_available(self):
    return self.status == 'AVAILABLE'
```

❌ **Éviter la logique complexe dans les modèles**
- Utiliser des services ou managers personnalisés

### 8.3 Vues

✅ **Une vue = Une responsabilité**
- Garder les vues simples et lisibles

✅ **Utiliser les décorateurs**
```python
@login_required
@user_passes_test(is_admin)
def admin_view(request):
    ...
```

✅ **Gérer les erreurs**
```python
book = get_object_or_404(Book, pk=pk)  # 404 si non trouvé
```

❌ **Éviter la duplication de code**
- Créer des fonctions utilitaires

### 8.4 Templates

✅ **Toujours étendre un template de base**
```html
{% extends 'base.html' %}
```

✅ **Utiliser des noms de blocs explicites**
```html
{% block sidebar %}...{% endblock %}
```

✅ **Charger les tags nécessaires**
```html
{% load static %}
{% load custom_tags %}
```

❌ **Éviter la logique complexe**
- Faire le traitement dans les vues

### 8.5 URLs

✅ **Toujours nommer les URLs**
```python
path('books/', views.book_list, name='book_list')
```

✅ **Utiliser `include()` pour modulariser**
```python
path('api/', include('api.urls'))
```

✅ **Utiliser des patterns explicites**
```python
path('books/<int:pk>/', ...)  # Mieux que <pk>/
```

### 8.6 Sécurité

✅ **Toujours utiliser `{% csrf_token %}`**
```html
<form method="post">
    {% csrf_token %}
    ...
</form>
```

✅ **Valider les entrées utilisateur**
```python
if form.is_valid():
    ...
```

✅ **Utiliser les permissions**
```python
@login_required
@permission_required('website.add_book')
```

❌ **Ne jamais mettre le `SECRET_KEY` dans le code**
- Utiliser des variables d'environnement

```python
# settings.py
import os
SECRET_KEY = os.environ.get('SECRET_KEY')
```

### 8.7 Performance

✅ **Utiliser `select_related()` et `prefetch_related()`**
```python
# Éviter N+1 queries
books = Book.objects.select_related('author').all()
loans = Loan.objects.prefetch_related('borrower').all()
```

✅ **Paginer les listes longues**
```python
from django.core.paginator import Paginator

paginator = Paginator(books, 25)  # 25 par page
page_obj = paginator.get_page(page_number)
```

✅ **Utiliser le cache**
```python
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)  # Cache 15 minutes
def book_list(request):
    ...
```

### 8.8 Développement

✅ **Utiliser `DEBUG = True` en développement**
```python
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
```

✅ **Utiliser des fixtures pour les données de test**
```bash
python manage.py dumpdata website > fixtures.json
python manage.py loaddata fixtures.json
```

✅ **Écrire des tests**
```python
from django.test import TestCase

class BookTestCase(TestCase):
    def test_book_creation(self):
        book = Book.objects.create(title="Test", author="Author", isbn="123")
        self.assertEqual(book.title, "Test")
```

---

## 9. Dépannage

### Erreur : "No module named 'django'"

**Solution :**
```bash
pip install django
# ou
activate  # Activer l'environnement virtuel
```

### Erreur : "You have unapplied migrations"

**Solution :**
```bash
python manage.py migrate
```

### Erreur : "TemplateDoesNotExist"

**Solution :**
- Vérifier que l'app est dans `INSTALLED_APPS`
- Vérifier le chemin du template : `app/templates/app/template.html`

### Erreur : "CSRF verification failed"

**Solution :**
```html
<form method="post">
    {% csrf_token %}  <!-- Ajouter cette ligne -->
    ...
</form>
```

### Base de données corrompue

**Solution :**
```bash
# Supprimer la base de données
del db.sqlite3  # Windows
rm db.sqlite3   # Linux/Mac

# Réappliquer les migrations
python manage.py migrate
python manage.py createsuperuser
```

---

## 10. Ressources Complémentaires

### Documentation Officielle
- [Django Documentation](https://docs.djangoproject.com/)
- [Django Tutorial](https://docs.djangoproject.com/en/stable/intro/tutorial01/)

### Tutoriels en Français
- [Django Girls Tutorial](https://tutorial.djangogirls.org/fr/)
- [OpenClassrooms - Django](https://openclassrooms.com/)

### Packages Utiles
```bash
pip install django-debug-toolbar  # Outil de débogage
pip install django-extensions     # Extensions utiles
pip install django-crispy-forms   # Formulaires stylisés
pip install pillow                # Gestion des images
```

---

## Conclusion

Ce guide couvre les bases de Django et les concepts essentiels pour développer une application web. Le système de gestion de bibliothèque est un excellent exemple pratique qui illustre :

✅ Les modèles et relations (Book, Loan, UserProfile)
✅ Les vues (FBV et authentification)
✅ Les templates (héritage, conditions, boucles)
✅ Les formulaires (ModelForm)
✅ L'interface admin
✅ Les URLs et le routing
✅ La gestion des fichiers media

**Prochaines étapes suggérées :**
1. Ajouter l'authentification avec permissions avancées
2. Créer une API REST avec Django REST Framework
3. Déployer sur un serveur (Heroku, PythonAnywhere, VPS)
4. Ajouter des tests unitaires et d'intégration
5. Améliorer l'interface utilisateur avec Bootstrap ou Tailwind CSS

Bon développement ! 🚀


