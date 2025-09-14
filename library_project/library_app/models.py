from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Profile(models.Model):
    USER_ROLES = (
        ('student', 'Student'),
        ('librarian', 'Librarian'),
    )
    GENDER_CHOICES = (
        ('Male', 'Male' ),
        ('Female', 'Female'),
        ('Unknown', 'Unknown'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=USER_ROLES, default='student')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Unknown')

    def __str__(self):
        return f"{self.user.username if self.user else 'Unknown User'} - {self.role}"


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)
    category = models.CharField(max_length=100)
    description = models.TextField(blank=True)  # NEW field
    total_copies = models.PositiveIntegerField()
    available_copies = models.PositiveIntegerField()
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # NEW field
    publisher = models.ForeignKey('Publisher', on_delete=models.SET_NULL, null=True, blank=True)  # NEW field
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
    
class Publisher(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()

    def __str__(self):
        return self.name


