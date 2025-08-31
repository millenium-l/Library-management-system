from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, IssuedBook
from .forms import BookForm

# Create your views here.

def dashboard(request):
    return render(request, 'library_app/dashboard.html')

def profile(request):
    return render(request, 'library_app/profile.html')

def book_list(request):
    books = Book.objects.all()
    return render(request, 'library_app/book_list.html', {'books': books})

def book_detail(request, id):
    book = get_object_or_404(Book, id=id)
    return render(request, 'library_app/book_detail.html', {'book': book})

def issued_books(request):
    return render(request, 'library_app/issued_books.html')

def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()

    return render(request, 'library_app/book_create.html', {'form': form})

