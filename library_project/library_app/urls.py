from django.urls import path
from .views import  dashboard, book_list, book_detail, book_issue, profile, book_create, book_update, book_delete, return_book

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('book_list/', book_list, name='book_list'),
    path('book_detail/<int:id>/', book_detail, name='book_detail'),
    path('issued_book/', book_issue, name='issued_book'),
    path('return-book/<int:issued_book_id>/', return_book, name='return_book'),
    path('profile/', profile, name='profile'),
    path('book_create/', book_create, name='book_create'),
    path('book_update/<int:id>/', book_update, name='book_update'),
    path('book_delete/<int:id>/', book_delete, name='book_delete'),
]