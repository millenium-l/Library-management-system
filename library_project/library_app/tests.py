from django.test import TestCase
from .models import Book, IssuedBook, BookRequest


# Create your tests here.

class BookModelTest(TestCase):

    def test_book_creation(self):
        book = Book.objects.create(
            title="Test Book",
            author="Author Name",
            isbn="1234567890123",
            category="Fiction",
            description="A test book description.",
            total_copies=5,
            available_copies=5,
        )
        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(book.title, "Test Book")