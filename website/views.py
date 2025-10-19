from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from .models import Book, Loan, UserProfile
from .forms import BookForm, LoanForm, BookSearchForm, UserRegistrationForm
from django.contrib.auth.forms import AuthenticationForm


# Fonctions de vérification des permissions
def is_librarian(user):
    """Vérifie si l'utilisateur est un bibliothécaire"""
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.is_librarian()


def can_borrow(user):
    """Vérifie si l'utilisateur peut emprunter des livres"""
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.can_borrow()


# Vues publiques
def home(request):
    """Page d'accueil"""
    recent_books = Book.objects.filter(status='AVAILABLE')[:6]
    total_books = Book.objects.count()
    available_books = Book.objects.filter(status='AVAILABLE').count()
    
    context = {
        'recent_books': recent_books,
        'total_books': total_books,
        'available_books': available_books,
    }
    return render(request, 'website/home.html', context)


def book_list(request):
    """Liste de tous les livres avec recherche"""
    books = Book.objects.all()
    form = BookSearchForm(request.GET)
    
    if form.is_valid():
        query = form.cleaned_data.get('query')
        category = form.cleaned_data.get('category')
        status = form.cleaned_data.get('status')
        
        if query:
            books = books.filter(
                Q(title__icontains=query) |
                Q(author__icontains=query) |
                Q(isbn__icontains=query) |
                Q(category__icontains=query)
            )
        
        if category:
            books = books.filter(category__icontains=category)
        
        if status:
            books = books.filter(status=status)
    
    context = {
        'books': books,
        'form': form,
    }
    return render(request, 'website/book_list.html', context)


def book_detail(request, pk):
    """Détails d'un livre"""
    book = get_object_or_404(Book, pk=pk)
    context = {
        'book': book,
    }
    return render(request, 'website/book_detail.html', context)


# Vues d'authentification
def custom_login(request):
    """Connexion avec redirection intelligente selon le type d'utilisateur"""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Bienvenue {user.get_full_name() or user.username} !')
                
                # Vérifier s'il y a une page "next" demandée
                next_page = request.GET.get('next') or request.POST.get('next')
                
                if next_page:
                    # Si une page est demandée, vérifier les permissions
                    if 'dashboard' in next_page or 'add_book' in next_page or 'create_loan' in next_page:
                        # Pages réservées aux bibliothécaires
                        if hasattr(user, 'profile') and (user.profile.is_librarian() or user.is_staff or user.is_superuser):
                            return redirect(next_page)
                        else:
                            messages.warning(request, 'Vous n\'avez pas accès à cette page.')
                            return redirect('home')
                    else:
                        # Autres pages accessibles
                        return redirect(next_page)
                
                # Redirection intelligente par défaut selon le type d'utilisateur
                if hasattr(user, 'profile'):
                    if user.profile.is_librarian() or user.is_staff or user.is_superuser:
                        # Bibliothécaires et admins → Dashboard
                        return redirect('dashboard')
                    else:
                        # Autres utilisateurs → Page d'accueil
                        return redirect('home')
                else:
                    # Utilisateur sans profil → Page d'accueil
                    return redirect('home')
    else:
        form = AuthenticationForm()
    
    return render(request, 'website/login.html', {'form': form})


def register(request):
    """Inscription d'un nouvel utilisateur"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Inscription réussie ! Bienvenue sur la plateforme.')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'website/register.html', {'form': form})


# Vues pour les bibliothécaires
@login_required
@user_passes_test(is_librarian)
def add_book(request):
    """Ajouter un nouveau livre (bibliothécaires uniquement)"""
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.added_by = request.user
            book.available_quantity = book.quantity
            book.save()
            messages.success(request, f'Le livre "{book.title}" a été ajouté avec succès.')
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookForm()
    
    return render(request, 'website/book_form.html', {'form': form, 'action': 'Ajouter'})


@login_required
@user_passes_test(is_librarian)
def edit_book(request, pk):
    """Modifier un livre (bibliothécaires uniquement)"""
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, f'Le livre "{book.title}" a été modifié avec succès.')
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookForm(instance=book)
    
    return render(request, 'website/book_form.html', {'form': form, 'action': 'Modifier', 'book': book})


@login_required
@user_passes_test(is_librarian)
def delete_book(request, pk):
    """Supprimer un livre (bibliothécaires uniquement)"""
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        title = book.title
        book.delete()
        messages.success(request, f'Le livre "{title}" a été supprimé.')
        return redirect('book_list')
    
    return render(request, 'website/book_confirm_delete.html', {'book': book})


# Vues pour les emprunts
@login_required
@user_passes_test(is_librarian)
def create_loan(request):
    """Créer un nouvel emprunt (bibliothécaires uniquement)"""
    if request.method == 'POST':
        form = LoanForm(request.POST)
        if form.is_valid():
            loan = form.save(commit=False)
            loan.librarian = request.user
            
            # Vérifier que le livre est disponible
            if loan.book.is_available():
                loan.save()
                loan.book.borrow_book()
                messages.success(
                    request,
                    f'Emprunt créé : "{loan.book.title}" pour {loan.borrower.get_full_name()}'
                )
                return redirect('loan_list')
            else:
                messages.error(request, 'Ce livre n\'est pas disponible pour emprunt.')
    else:
        form = LoanForm()
    
    return render(request, 'website/loan_form.html', {'form': form})


@login_required
def loan_list(request):
    """Liste des emprunts"""
    if hasattr(request.user, 'profile') and request.user.profile.is_librarian():
        # Les bibliothécaires voient tous les emprunts
        loans = Loan.objects.all()
    else:
        # Les autres ne voient que leurs emprunts
        loans = Loan.objects.filter(borrower=request.user)
    
    # Filtrer par statut si demandé
    status = request.GET.get('status')
    if status:
        loans = loans.filter(status=status)
    
    context = {
        'loans': loans,
    }
    return render(request, 'website/loan_list.html', context)


@login_required
@user_passes_test(is_librarian)
def return_book(request, loan_id):
    """Marquer un livre comme retourné (bibliothécaires uniquement)"""
    loan = get_object_or_404(Loan, pk=loan_id)
    
    if request.method == 'POST':
        if loan.status != 'RETURNED':
            loan.return_book()
            messages.success(
                request,
                f'Le livre "{loan.book.title}" a été retourné par {loan.borrower.get_full_name()}'
            )
        else:
            messages.warning(request, 'Ce livre a déjà été retourné.')
        
        return redirect('loan_list')
    
    return render(request, 'website/loan_return_confirm.html', {'loan': loan})


@login_required
def my_loans(request):
    """Mes emprunts en cours et historique"""
    active_loans = Loan.objects.filter(
        borrower=request.user,
        status__in=['ACTIVE', 'OVERDUE']
    )
    
    past_loans = Loan.objects.filter(
        borrower=request.user,
        status='RETURNED'
    )
    
    context = {
        'active_loans': active_loans,
        'past_loans': past_loans,
    }
    return render(request, 'website/my_loans.html', context)


@login_required
@user_passes_test(can_borrow)
def borrow_book(request, pk):
    """Emprunter un livre (pour étudiants, professeurs, personnel)"""
    book = get_object_or_404(Book, pk=pk)
    
    # Vérifier que le livre est disponible
    if not book.is_available():
        messages.error(request, 'Ce livre n\'est pas disponible actuellement.')
        return redirect('book_detail', pk=pk)
    
    # Vérifier que l'utilisateur n'a pas déjà emprunté ce livre
    existing_loan = Loan.objects.filter(
        book=book,
        borrower=request.user,
        status__in=['ACTIVE', 'OVERDUE']
    ).exists()
    
    if existing_loan:
        messages.warning(request, 'Vous avez déjà emprunté ce livre.')
        return redirect('my_loans')
    
    if request.method == 'POST':
        from datetime import timedelta
        
        # Créer l'emprunt
        loan = Loan.objects.create(
            book=book,
            borrower=request.user,
            borrow_date=timezone.now(),
            due_date=timezone.now() + timedelta(days=14),
            status='ACTIVE'
        )
        
        # Mettre à jour la disponibilité du livre
        book.borrow_book()
        
        messages.success(
            request,
            f'Vous avez emprunté "{book.title}". Date de retour prévue : {loan.due_date.strftime("%d/%m/%Y")}'
        )
        return redirect('my_loans')
    
    return render(request, 'website/borrow_confirm.html', {'book': book})


@login_required
@user_passes_test(is_librarian)
def dashboard(request):
    """Tableau de bord pour les bibliothécaires"""
    from django.contrib.auth.models import User
    
    # Statistiques des livres
    total_books = Book.objects.count()
    available_books = Book.objects.filter(status='AVAILABLE').count()
    borrowed_books = Book.objects.filter(status='BORROWED').count()
    maintenance_books = Book.objects.filter(status='MAINTENANCE').count()
    
    # Calcul du nombre total d'exemplaires disponibles
    total_copies_available = sum(book.available_quantity for book in Book.objects.all())
    total_copies = sum(book.quantity for book in Book.objects.all())
    
    # Statistiques des emprunts
    active_loans = Loan.objects.filter(status='ACTIVE').count()
    overdue_loans = Loan.objects.filter(status='OVERDUE').count()
    returned_loans = Loan.objects.filter(status='RETURNED').count()
    total_loans = Loan.objects.count()
    
    # Statistiques des utilisateurs
    total_users = User.objects.count()
    total_borrowers = UserProfile.objects.filter(user_type__in=['STUDENT', 'TEACHER', 'STAFF']).count()
    total_librarians = UserProfile.objects.filter(user_type='LIBRARIAN').count()
    
    # Emprunts récents et en retard
    recent_loans = Loan.objects.filter(status__in=['ACTIVE', 'OVERDUE']).select_related('book', 'borrower', 'borrower__profile')[:10]
    overdue_list = Loan.objects.filter(status='OVERDUE').select_related('book', 'borrower', 'borrower__profile')
    
    # Livres les plus empruntés (top 5)
    from django.db.models import Count
    popular_books = Book.objects.annotate(
        loan_count=Count('loans')
    ).filter(loan_count__gt=0).order_by('-loan_count')[:5]
    
    context = {
        # Livres
        'total_books': total_books,
        'available_books': available_books,
        'borrowed_books': borrowed_books,
        'maintenance_books': maintenance_books,
        'total_copies': total_copies,
        'total_copies_available': total_copies_available,
        
        # Emprunts
        'active_loans': active_loans,
        'overdue_loans': overdue_loans,
        'returned_loans': returned_loans,
        'total_loans': total_loans,
        
        # Utilisateurs
        'total_users': total_users,
        'total_borrowers': total_borrowers,
        'total_librarians': total_librarians,
        
        # Listes
        'recent_loans': recent_loans,
        'overdue_list': overdue_list,
        'popular_books': popular_books,
    }
    return render(request, 'website/dashboard.html', context)