from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


"""
## When you create a form based on a model, like User, you use a Meta class to tell Django:
“This form is linked to this model, and should include these fields.”
 
## The Meta class is used only in model forms — forms that create or update model instances (like registering a new user).

## widgets==> define how the field should look and behave in the browser i.e forms.TextInput

## strip=False==> it means that leading and trailing whitespace will be preserved in the input.

## The UserCreationForm is a ModelForm — a type of Django form that is designed to:
Create or update a model instance in the database (like a User). The meta is used to specify which model 
and fields to include in the form and save to the database.

## AuthenticationForm: Just validates user credentials against existing data — 
no need to save or create, so it doesn’t need a Meta class.
"""

# Dropdown options for gender
GENDER_CHOICES = [
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Unknown', 'Unknown'),
]


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        "class": "form-control",
        "placeholder": "Enter your email"
    }))

    #it creates a dropdown for gender
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