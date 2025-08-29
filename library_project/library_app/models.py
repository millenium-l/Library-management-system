from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    USER_ROLES = (
        ('student', 'Student'),
        ('librarian', 'Librarian'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=USER_ROLES, default='student')

    def __str__(self):
        return f"{self.user.username if self.user else 'Unknown User'} - {self.role}"


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)
    category = models.CharField(max_length=100)
    total_copies = models.PositiveIntegerField()
    available_copies = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.title} - {self.author}"
    

from django.utils import timezone

class IssuedBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    issue_date = models.DateField(default=timezone.now)
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)

    def is_overdue(self):
        if self.return_date:
            return False
        return timezone.now().date() > self.due_date

    def __str__(self):
        return f"{self.book.title} issued to {self.user.username}"


