from django.urls import path
from .views import index, dashboard, book_list, book_detail, issued_books, profile

urlpatterns = [
    path('', index, name='index'),
    path('dashboard/', dashboard, name='dashboard'),
    path('book_list/', book_list, name='book_list'),
    path('book_detail/', book_detail, name='book_detail'),
    path('issued_books/', issued_books, name='issued_books'),
    path('profile/', profile, name='profile'),
]