from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, IssuedBook
from .forms import BookForm

# Create your views here.


def dashboard(request):
    title = "Dashboard"
    context = {
        'title': title,
        'total_books': Book.objects.count(),
    }
    return render(request, 'library_app/dashboard.html', context)

def profile(request):
    title = "Profile"
    return render(request, 'library_app/profile.html', {'title': title})

def book_list(request):
    books = Book.objects.all()
    title = "Book List"
    return render(request, 'library_app/book_list.html', {'books': books, 'title': title})

def book_detail(request, id):
    book = get_object_or_404(Book, id=id)
    title = "Book Detail"
    return render(request, 'library_app/book_detail.html', {'book': book, 'title': title})

def issued_books(request):
    title = "Issued Books"
    return render(request, 'library_app/issued_books.html', {'title': title})

def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
        
    title = "Add New Book"

    return render(request, 'library_app/book_create.html', {'form': form, 'title': title})

def book_update(request, id):
    book = get_object_or_404(Book, id=id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)

    title = "Update Book"
    return render(request, 'library_app/book_update.html', {'form': form, 'title': title})

def book_delete(request, id):
    book = get_object_or_404(Book, id=id)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    
    title = "Delete Book"
    
    return render(request, 'library_app/book_delete.html', {'book': book, 'title': title})