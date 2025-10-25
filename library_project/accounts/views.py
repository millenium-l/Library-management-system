from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth import login, logout
from library_app.models import Profile

# Create your views here.

"""
A session is a temporary way to remember “who you are” as you move through the website.

"""

def user_register(request):
    # Handle form submission and user registration logic here
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)# Builds a form with submitted data.
        if form.is_valid():
            user = form.save() 
            # creating a gender role
            gender = form.cleaned_data['gender'] 
            user.profile.gender = gender 
            user.profile.save()

            login(request, user)# create a session for the user to log them in
            return redirect('dashboard')  
    else:
        form = CustomUserCreationForm()  
    return render(request, 'accounts/register.html', {'form': form}) 



def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)# data=request.POST, the actual form data the user submitted
        if form.is_valid():
            user = form.get_user()# get the authenticated user object
            login(request, user)
            return redirect('dashboard')  
    else:
        form = CustomAuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def  user_logout(request):
    logout(request)
    return redirect('login')