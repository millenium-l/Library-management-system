from django.urls import path
from .views import index, Register, Login, Logout

urlpatterns = [
    path('', index, name='index'),
    path('register/', Register, name='register'),
    path('login/', Login, name='login'),
    path('logout/', Logout, name='logout'),
] 