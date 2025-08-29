from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'accounts/index.html')

def Register(request):
    return render(request, 'accounts/register.html')

def Login(request):
    return render(request, 'accounts/login.html')

def  Logout(request):
    return render(request, 'accounts/logout.html')