from django.urls import path
from .views import  dashboard, book_list, book_detail, issued_books, profile, book_create, book_update, book_delete

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('book_list/', book_list, name='book_list'),
    path('book_detail/<int:id>/', book_detail, name='book_detail'),
    path('issued_books/', issued_books, name='issued_books'),
    path('profile/', profile, name='profile'),
    path('book_create/', book_create, name='book_create'),
    path('book_update/<int:id>/', book_update, name='book_update'),
    path('book_delete/<int:id>/', book_delete, name='book_delete'),
]