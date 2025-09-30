from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, Book, Loan


# Inline pour le profil utilisateur
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profil'
    fk_name = 'user'


# Étendre l'admin User pour inclure le profil
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_user_type', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'profile__user_type')
    
    def get_user_type(self, obj):
        return obj.profile.get_user_type_display() if hasattr(obj, 'profile') else '-'
    get_user_type.short_description = 'Type d\'utilisateur'


# Réenregistrer UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


# Admin pour le profil utilisateur
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type', 'matricule', 'phone', 'created_at')
    list_filter = ('user_type', 'created_at')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name', 'matricule')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Utilisateur', {
            'fields': ('user', 'user_type')
        }),
        ('Informations personnelles', {
            'fields': ('matricule', 'phone', 'address')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


# Admin pour les livres
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'category', 'quantity', 'available_quantity', 'status', 'created_at')
    list_filter = ('status', 'category', 'publication_year', 'created_at')
    search_fields = ('title', 'author', 'isbn', 'publisher', 'category')
    readonly_fields = ('created_at', 'updated_at', 'added_by')
    list_editable = ('status',)
    
    fieldsets = (
        ('Informations principales', {
            'fields': ('title', 'author', 'isbn', 'publisher', 'publication_year')
        }),
        ('Catégorisation', {
            'fields': ('category', 'description', 'cover_image')
        }),
        ('Disponibilité', {
            'fields': ('quantity', 'available_quantity', 'status')
        }),
        ('Métadonnées', {
            'fields': ('added_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # Si c'est une création
            obj.added_by = request.user
            if not obj.available_quantity:
                obj.available_quantity = obj.quantity
        super().save_model(request, obj, form, change)


# Admin pour les emprunts
@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('book', 'borrower', 'borrow_date', 'due_date', 'return_date', 'status', 'is_overdue_display')
    list_filter = ('status', 'borrow_date', 'due_date')
    search_fields = ('book__title', 'borrower__username', 'borrower__first_name', 'borrower__last_name')
    readonly_fields = ('created_at', 'updated_at', 'librarian', 'is_overdue_display', 'days_overdue')
    date_hierarchy = 'borrow_date'
    
    fieldsets = (
        ('Informations d\'emprunt', {
            'fields': ('book', 'borrower', 'librarian')
        }),
        ('Dates', {
            'fields': ('borrow_date', 'due_date', 'return_date')
        }),
        ('Statut', {
            'fields': ('status', 'is_overdue_display', 'days_overdue', 'notes')
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def is_overdue_display(self, obj):
        return "Oui" if obj.is_overdue() else "Non"
    is_overdue_display.short_description = 'En retard'
    is_overdue_display.boolean = True
    
    def save_model(self, request, obj, form, change):
        if not change:  # Si c'est une création
            obj.librarian = request.user
        super().save_model(request, obj, form, change)


# Configuration du site admin
admin.site.site_header = "Administration - Bibliothèque en Ligne"
admin.site.site_title = "Bibliothèque Admin"
admin.site.index_title = "Gestion de la bibliothèque"
