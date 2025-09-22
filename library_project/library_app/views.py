from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, IssuedBook
from .forms import BookForm, IssuedBookForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime
from django.utils import timezone
from django.db.models import Q
# Create your views here.


def dashboard(request):
    title = "Dashboard"
    context = {
        'title': title,
        'total_books': Book.objects.count(),
        'current_year': datetime.now().year,
    }
    return render(request, 'library_app/dashboard.html', context)

@login_required
def profile(request):
    title = "Profile"
    profile = request.user.profile # access the profile linked to the user
    context = {
        'title': title,
        'profile': profile,
        'current_year': datetime.now().year,
    }
    return render(request, 'library_app/profile.html', context, )

@login_required
def book_list(request):
    query = request.GET.get('q', '')
    books = Book.objects.all().order_by('title')
    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(isbn__icontains=query)
        )
    
    paginator = Paginator(books, 4)  # Show 4 books per page
    page = request.GET.get('page')

    try:
        paginated_books = paginator.page(page)
    except PageNotAnInteger:
        paginated_books = paginator.page(1)
    except EmptyPage:
        paginated_books = paginator.page(paginator.num_pages)
    title = "Book List"
    return render(request, 'library_app/book_list.html', {'books': paginated_books, 'title': title, 'current_year': datetime.now().year, 'query': query})

"""
class based boook_list
from django.views.generic import ListView
class BookListView(ListView):
    model = Book  # The model you want to list
    template_name = 'library_app/book_list.html'  # Optional, default will be book_list.html
    context_object_name = 'books'  # This is the variable name that will be used in the template
    paginate_by = 4  # This will paginate the list, showing 4 books per page

"""

@login_required
def book_detail(request, id):
    book = get_object_or_404(Book, id=id)
    title = "Book Detail"
    context = {
        'book': book,
        'title': title,
        'current_year': datetime.now().year,
    }
    return render(request, 'library_app/book_detail.html', context)


@login_required
def book_issue(request):
    if not request.user.is_staff:  # Only librarian can issue books
        messages.error(request, "You are not authorized to issue books.")
        return redirect('book_list')

    if request.method == 'POST':
        form = IssuedBookForm(request.POST)
        if form.is_valid():
            issued_book = form.save(commit=False)

            # Check if book is available
            if issued_book.book.available_copies < 1:
                messages.error(request, "No available copies for this book.")
            else:
                issued_book.save()
                # Reduce available copies count
                issued_book.book.available_copies -= 1
                issued_book.book.save()
                messages.success(request, "Book issued successfully.")
                return redirect('dashboard')
    else:
        form = IssuedBookForm()

    return render(request, 'library_app/issued_book.html', {'form': form})


@login_required
def return_book(request, issued_book_id):
    issued_book = get_object_or_404(IssuedBook, id=issued_book_id)
    if request.method == 'POST':
        issued_book.return_date = timezone.now().date()
        issued_book.save()
        # Increase available copies
        issued_book.book.available_copies += 1
        issued_book.book.save()
        messages.success(request, "Book returned successfully.")
        return redirect('dashboard')

    return render(request, 'library_app/return_book.html', {'issued_book': issued_book})



@login_required
def book_create(request): 
    if not request.user.is_staff: 
        messages.error(request, "You are not authorized to add books.")
        return redirect('book_list')
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.added_by = request.user
            book.save()
            messages.success(request, 'Book added successfully!')
            return redirect('book_list')
    else:
        form = BookForm()
        
    title = "Add New Book"
    context = {
        'form': form,
        'title': title,
        'current_year': datetime.now().year,
    }

    return render(request, 'library_app/book_create.html', context)

@login_required
def book_update(request, id): 
    if not request.user.is_staff: 
        messages.error(request, "You are not authorized to edit books.")
        return redirect('book_list')
    book = get_object_or_404(Book, id=id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)

    title = "Update Book"
    context = {
        'form': form,
        'title': title,
        'current_year': datetime.now().year,
    }
    return render(request, 'library_app/book_update.html', context)

@login_required
def book_delete(request, id):  
    if not request.user.is_staff: 
        messages.error(request, "You are not authorized to delete books.")
        return redirect('book_list')
    book = get_object_or_404(Book, id=id)
    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Book deleted successfully!')
        return redirect('book_list')
    
    title = "Delete Book"

    context = {
        'book': book,
        'title': title,
        'current_year': datetime.now().year,
    }
    
    return render(request, 'library_app/book_delete.html', context)