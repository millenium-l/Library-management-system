from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model= Book
        fields = ['title', 'author', 'isbn', 'category', 'description', 'total_copies', 'available_copies']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter book title'}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter author name'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter ISBN number'}),
            'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter book category'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'total_copies': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter total copies'}),
            'available_copies': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter available copies'}),
        }