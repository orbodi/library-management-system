from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Book, Loan, UserProfile
from datetime import timedelta
from django.utils import timezone


class UserRegistrationForm(UserCreationForm):
    """Formulaire d'inscription avec profil utilisateur"""
    email = forms.EmailField(required=True, label="Email")
    first_name = forms.CharField(required=True, label="Prénom")
    last_name = forms.CharField(required=True, label="Nom")
    user_type = forms.ChoiceField(
        choices=UserProfile.USER_TYPE_CHOICES,
        required=True,
        label="Type d'utilisateur"
    )
    matricule = forms.CharField(required=False, label="Matricule")
    phone = forms.CharField(required=False, label="Téléphone")
    address = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 3}), label="Adresse")
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            # Créer le profil utilisateur
            UserProfile.objects.create(
                user=user,
                user_type=self.cleaned_data['user_type'],
                matricule=self.cleaned_data.get('matricule'),
                phone=self.cleaned_data.get('phone'),
                address=self.cleaned_data.get('address')
            )
        return user


class BookForm(forms.ModelForm):
    """Formulaire pour ajouter/modifier un livre"""
    
    class Meta:
        model = Book
        fields = [
            'title', 'author', 'isbn', 'publisher', 'publication_year',
            'category', 'description', 'cover_image', 'quantity', 'status'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titre du livre'}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom de l\'auteur'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ISBN'}),
            'publisher': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Éditeur'}),
            'publication_year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '2024'}),
            'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Science, Histoire, etc.'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Description du livre'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si c'est un nouveau livre, définir available_quantity = quantity
        if not self.instance.pk:
            self.instance.available_quantity = self.instance.quantity


class LoanForm(forms.ModelForm):
    """Formulaire pour créer un emprunt"""
    
    class Meta:
        model = Loan
        fields = ['book', 'borrower', 'due_date', 'notes']
        widgets = {
            'book': forms.Select(attrs={'class': 'form-control'}),
            'borrower': forms.Select(attrs={'class': 'form-control'}),
            'due_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ne montrer que les livres disponibles
        self.fields['book'].queryset = Book.objects.filter(
            available_quantity__gt=0,
            status='AVAILABLE'
        )
        # Ne montrer que les utilisateurs qui peuvent emprunter
        self.fields['borrower'].queryset = User.objects.filter(
            profile__user_type__in=['STUDENT', 'TEACHER', 'STAFF']
        )
        # Définir la date de retour par défaut (14 jours)
        if not self.instance.pk:
            self.fields['due_date'].initial = timezone.now() + timedelta(days=14)


class BookSearchForm(forms.Form):
    """Formulaire de recherche de livres"""
    query = forms.CharField(
        required=False,
        label="Rechercher",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Titre, auteur, ISBN, catégorie...'
        })
    )
    category = forms.CharField(
        required=False,
        label="Catégorie",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Filtrer par catégorie'
        })
    )
    status = forms.ChoiceField(
        required=False,
        label="Statut",
        choices=[('', 'Tous')] + Book.STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )


