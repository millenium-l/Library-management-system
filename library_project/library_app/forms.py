from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model= Book
        fields = ['title', 'author', 'isbn', 'category', 'description', 'total_copies', 'available_copies']