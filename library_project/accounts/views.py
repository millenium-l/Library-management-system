from django.shortcuts import render, redirect
#from django.contrib.auth.forms import  AuthenticationForm
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth import login, logout
from library_app.models import Profile

# Create your views here.

def user_register(request):
    # Handle form submission and user registration logic here
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # creating a gender role
            gender = form.cleaned_data('gender')
            Profile.objects.create(user=user, gender=gender)  # create Profile here

            login(request, user)
            return redirect('dashboard')  # redirect to homepage or dashboard
    else:
        form = CustomUserCreationForm()        
    return render(request, 'accounts/register.html', {'form': form})



def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')  # redirect to dashboard or homepage
    else:
        form = CustomAuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def  user_logout(request):
    logout(request)
    return redirect('login')