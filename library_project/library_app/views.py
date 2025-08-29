from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'library_app/index.html')

def dashboard(request):
    return render(request, 'library_app/dashboard.html')

def profile(request):
    return render(request, 'library_app/profile.html')

def book_list(request):
    return render(request, 'library_app/book_list.html')

def book_detail(request):
    return render(request, 'library_app/book_detail.html')

def issued_books(request):
    return render(request, 'library_app/issued_books.html')

