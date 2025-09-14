from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
    ('U', 'Unknown'),
]


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        "class": "form-control",
        "placeholder": "Enter your email"
    }))

    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        widget=forms.Select(attrs={"class": "form-select"}),
        required=True
    )

    password1 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Enter your password"
    }),)
    password2 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Confirm your password"
            }),)
    

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        widgets = {
            "username": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter your username"
            }),
            
        }

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Enter your username"
    }))
    password = forms.CharField(strip=False, widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Enter your password"
    }))