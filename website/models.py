from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

# Create your models here.

class UserProfile(models.Model):
    """Profil utilisateur étendu avec le type d'utilisateur"""
    USER_TYPE_CHOICES = [
        ('STUDENT', 'Étudiant'),
        ('TEACHER', 'Professeur'),
        ('STAFF', 'Personnel'),
        ('LIBRARIAN', 'Bibliothécaire'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='STUDENT')
    matricule = models.CharField(max_length=50, unique=True, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Profil Utilisateur"
        verbose_name_plural = "Profils Utilisateurs"
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.get_user_type_display()}"
    
    def can_borrow(self):
        """Vérifie si l'utilisateur peut emprunter des livres"""
        return self.user_type in ['STUDENT', 'TEACHER', 'STAFF']
    
    def is_librarian(self):
        """Vérifie si l'utilisateur est bibliothécaire"""
        return self.user_type == 'LIBRARIAN'


class Book(models.Model):
    """Modèle pour les livres"""
    STATUS_CHOICES = [
        ('AVAILABLE', 'Disponible'),
        ('BORROWED', 'Emprunté'),
        ('MAINTENANCE', 'En maintenance'),
        ('LOST', 'Perdu'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Titre")
    author = models.CharField(max_length=200, verbose_name="Auteur")
    isbn = models.CharField(max_length=13, unique=True, verbose_name="ISBN")
    publisher = models.CharField(max_length=200, blank=True, null=True, verbose_name="Éditeur")
    publication_year = models.IntegerField(blank=True, null=True, verbose_name="Année de publication")
    category = models.CharField(max_length=100, blank=True, null=True, verbose_name="Catégorie")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    cover_image = models.ImageField(upload_to='book_covers/', blank=True, null=True, verbose_name="Image de couverture")
    quantity = models.IntegerField(default=1, verbose_name="Quantité totale")
    available_quantity = models.IntegerField(default=1, verbose_name="Quantité disponible")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='AVAILABLE', verbose_name="Statut")
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='books_added')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Livre"
        verbose_name_plural = "Livres"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} par {self.author}"
    
    def is_available(self):
        """Vérifie si le livre est disponible pour emprunt"""
        return self.available_quantity > 0 and self.status == 'AVAILABLE'
    
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


class Loan(models.Model):
    """Modèle pour les emprunts de livres"""
    STATUS_CHOICES = [
        ('ACTIVE', 'En cours'),
        ('RETURNED', 'Retourné'),
        ('OVERDUE', 'En retard'),
    ]
    
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='loans', verbose_name="Livre")
    borrower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loans', verbose_name="Emprunteur")
    librarian = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='loans_managed', verbose_name="Bibliothécaire")
    borrow_date = models.DateTimeField(default=timezone.now, verbose_name="Date d'emprunt")
    due_date = models.DateTimeField(verbose_name="Date de retour prévue")
    return_date = models.DateTimeField(blank=True, null=True, verbose_name="Date de retour effective")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE', verbose_name="Statut")
    notes = models.TextField(blank=True, null=True, verbose_name="Notes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Emprunt"
        verbose_name_plural = "Emprunts"
        ordering = ['-borrow_date']
    
    def __str__(self):
        return f"{self.book.title} - {self.borrower.get_full_name() or self.borrower.username}"
    
    def save(self, *args, **kwargs):
        # Définir la date de retour prévue (14 jours après l'emprunt)
        if not self.due_date:
            self.due_date = self.borrow_date + timedelta(days=14)
        
        # Vérifier si l'emprunt est en retard
        if self.status == 'ACTIVE' and timezone.now() > self.due_date:
            self.status = 'OVERDUE'
        
        super().save(*args, **kwargs)
    
    def is_overdue(self):
        """Vérifie si l'emprunt est en retard"""
        return self.status == 'ACTIVE' and timezone.now() > self.due_date
    
    def days_overdue(self):
        """Calcule le nombre de jours de retard"""
        if self.is_overdue():
            return (timezone.now() - self.due_date).days
        return 0
    
    def return_book(self):
        """Marque le livre comme retourné"""
        self.return_date = timezone.now()
        self.status = 'RETURNED'
        self.save()
        self.book.return_book()
