from django.urls import path
from .views import  dashboard, book_list, book_detail, book_issue, profile, book_create, book_update, book_delete, return_book, request_book, my_requests, approve_request, reject_request, manage_requests

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('book_list/', book_list, name='book_list'),
    path('book_detail/<int:id>/', book_detail, name='book_detail'),
    path('request-book/<int:book_id>/', request_book, name='request_book'),
    path('issued_book/', book_issue, name='issued_book'),
    path('manage_requests/', manage_requests, name='manage_requests'),
    path('return-book/<int:issued_book_id>/', return_book, name='return_book'),
    path('profile/', profile, name='profile'),
    path('book_create/', book_create, name='book_create'),
    path('book_update/<int:id>/', book_update, name='book_update'),
    path('book_delete/<int:id>/', book_delete, name='book_delete'),
    path('approve-request/<int:request_id>/', approve_request, name='approve_request'),
    path('reject-request/<int:request_id>/', reject_request, name='reject_request'),
    path('my-requests/', my_requests, name='my_requests'),


]