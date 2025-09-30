from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, logout
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from .models import Book, Loan, UserProfile
from .forms import BookForm, LoanForm, BookSearchForm, UserRegistrationForm


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
@user_passes_test(is_librarian)
def dashboard(request):
    """Tableau de bord pour les bibliothécaires"""
    total_books = Book.objects.count()
    available_books = Book.objects.filter(status='AVAILABLE').count()
    borrowed_books = Book.objects.filter(status='BORROWED').count()
    
    active_loans = Loan.objects.filter(status='ACTIVE').count()
    overdue_loans = Loan.objects.filter(status='OVERDUE').count()
    
    recent_loans = Loan.objects.filter(status__in=['ACTIVE', 'OVERDUE'])[:10]
    overdue_list = Loan.objects.filter(status='OVERDUE')
    
    context = {
        'total_books': total_books,
        'available_books': available_books,
        'borrowed_books': borrowed_books,
        'active_loans': active_loans,
        'overdue_loans': overdue_loans,
        'recent_loans': recent_loans,
        'overdue_list': overdue_list,
    }
    return render(request, 'website/dashboard.html', context)