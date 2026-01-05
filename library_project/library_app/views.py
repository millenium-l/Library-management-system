from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, IssuedBook, BookRequest
from .forms import BookForm, IssuedBookForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime
from django.utils import timezone
from django.db.models import Q, Count
# Create your views here.



def dashboard(request):
    total_books = Book.objects.count()
    borrowed_books = IssuedBook.objects.filter(return_date__isnull=True).count()
    recent_books = Book.objects.order_by('-created_at')[:5]

    # Optional: Most popular books (by borrow count)
    #annotate to count related issuedbook entries
    popular_books = (
        Book.objects.annotate(borrow_count=Count('issuedbook'))
        .order_by('-borrow_count')[:5]
    )

    context = {
        'title': "Dashboard",
        'total_books': total_books,
        'borrowed_books': borrowed_books,
        'recent_books': recent_books,
        'popular_books': popular_books,
        'current_year': timezone.now().year,
    }
    return render(request, 'library_app/dashboard.html', context)

@login_required
def profile(request):
    profile = request.user.profile # access the profile linked to the user
    context = {
        'title': profile,
        'profile': profile,
        'current_year': timezone.now().year,
    }
    return render(request, 'library_app/profile.html', context, )

"""
use of q object allowing complex queries with OR conditions

"""

@login_required
def book_list(request):
    query = request.GET.get('q', '')# reads the search query from the URL parameters
    books = Book.objects.all().order_by('title')
    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(isbn__icontains=query)
        )
    
    paginator = Paginator(books, 4)  # Show 4 books per page
    page_number = request.GET.get('page') # get the page number from the URL parameters
    books_page = paginator.get_page(page_number) # get the books for the current page

    context = {
        'title': "Book List",
        'books': books_page,
        'query': query,
        'current_year': timezone.now().year,
    }

    
    
    return render(request, 'library_app/book_list.html', context)

"""

class based boook_list
from django.views.generic import ListView
class BookListView(ListView):
    model = Book  # The model you want to list
    template_name = 'library_app/book_list.html'  # Optional, default will be book_list.html
    context_object_name = 'books'  # This is the variable name that will be used in the template
    paginate_by = 4  # This will paginate the list, showing 4 books per page

"""
@login_required
def book_detail(request, id):
    book = get_object_or_404(Book, id=id)
    
    # Check if the logged-in user currently has this book issued and not returned
    issued_book = IssuedBook.objects.filter(
        user=request.user,
        book=book,
        return_date__isnull=True
    ).first()

    context = {
        'book': book,
        'issued_book': issued_book,
        'title': "Book Detail",
        'current_year': timezone.now().year,
    }
    return render(request, 'library_app/book_detail.html', context)

@login_required
def book_create(request): 
    if not request.user.is_staff: 
        messages.error(request, "You are not authorized to add books.")
        return redirect('book_list')
    if request.method == 'POST':
        form = BookForm(request.POST)# holds the submitted data
        if form.is_valid():
            book = form.save(commit=False)# commit false to modify(added_by) before saving
            book.added_by = request.user
            book.save()
            messages.success(request, 'Book added successfully!')
            return redirect('book_list')
    else:
        form = BookForm()
        
    title = "Add New Book"
    context = {
        'form': form,
        'title': title,
        'current_year': datetime.now().year,
    }

    return render(request, 'library_app/book_create.html', context)

@login_required
def book_update(request, id): 
    if not request.user.is_staff: 
        messages.error(request, "You are not authorized to edit books.")
        return redirect('book_list')
    book = get_object_or_404(Book, id=id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)# instance to update existing book 
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)

    title = "Update Book"
    context = {
        'form': form,
        'title': title,
        'current_year': datetime.now().year,
    }
    return render(request, 'library_app/book_update.html', context)

@login_required
def book_delete(request, id):  
    if not request.user.is_staff: 
        messages.error(request, "You are not authorized to delete books.")
        return redirect('book_list')
    book = get_object_or_404(Book, id=id)#fetch the book to be deleted, and prevent errors when the book doesn’t exist, not wrong deletions.
    # confirm deletion on POST request to avoid accidental deletions
    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Book deleted successfully!')
        return redirect('book_list')
    
    title = "Delete Book"

    context = {
        'book': book,
        'title': title,
        'current_year': datetime.now().year,
    }
    
    return render(request, 'library_app/book_delete.html', context)






@login_required
def book_issue(request):
    if not request.user.is_staff:  # Only staff can issue books
        messages.error(request, "You are not authorized to issue books.")
        return redirect('book_list')

    if request.method == 'POST':
        form = IssuedBookForm(request.POST)
        if form.is_valid():
            issued_book = form.save(commit=False)

            # Check if book is available
            if issued_book.book.available_copies < 1:
                messages.error(request, "No available copies for this book.")
            else:
                issued_book.save()
                # Reduce available copies count
                issued_book.book.available_copies -= 1
                issued_book.book.save()
                messages.success(request, "Book issued successfully.")
                return redirect('dashboard')
    else:
        form = IssuedBookForm()

    return render(request, 'library_app/issued_book.html', {'form': form})


@login_required
def request_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    # Check if user already requested this book and it's pending or approved
    existing_request = BookRequest.objects.filter(
        user=request.user,
        book=book,
        status__in=['pending', 'approved']
    ).exists()

    if existing_request:
        messages.info(request, "You already have a pending or approved request for this book.")
        return redirect('book_list')

    if request.method == 'POST':
        # Create a new BookRequest
        BookRequest.objects.create(user=request.user, book=book)
        messages.success(request, f"Your request for '{book.title}' has been sent.")
        return redirect('book_list')

    # Show confirmation page (optional)
    return render(request, 'library_app/request_book.html', {'book': book})


@login_required
def return_book(request, issued_book_id):
    issued_book = get_object_or_404(IssuedBook, id=issued_book_id)

    if request.method == 'POST':
        issued_book.return_date = timezone.now().date()
        issued_book.save()

        # Increase available copies
        issued_book.book.available_copies += 1
        issued_book.book.save()

        # Update the related book request status
        try:
            book_request = BookRequest.objects.get(
                user=issued_book.user,
                book=issued_book.book,
                status='approved'
            )
            book_request.status = 'returned'
            book_request.save()
        except BookRequest.DoesNotExist:
            pass  # No active request found (edge case)

        messages.success(request, f"Book '{issued_book.book.title}' returned successfully.")
        return redirect('my_requests')

    return render(request, 'library_app/return_book.html', {'issued_book': issued_book})


from django.contrib.admin.views.decorators import staff_member_required
@login_required
@staff_member_required
def manage_requests(request):

    query = request.GET.get('q', '').strip()

    user_filter = Q()
    if query:
        user_filter = (
            Q(user__username__icontains=query) |
            Q(user__email__icontains=query) |
            Q(user__id__icontains=query)
        )

    pending_requests = BookRequest.objects.filter(
        user_filter, status='pending'
    ).order_by('-request_date')

    approved_requests = BookRequest.objects.filter(
        user_filter, status='approved'
    ).order_by('-request_date')

    rejected_requests = BookRequest.objects.filter(
        user_filter, status='rejected'
    ).order_by('-request_date')

    returned_requests = BookRequest.objects.filter(
        user_filter, status='returned'
    ).order_by('-request_date')

    context = {
        'title': 'Manage Book Requests',
        'query': query,
        'pending_requests': pending_requests,
        'approved_requests': approved_requests,
        'rejected_requests': rejected_requests,
        'returned_requests': returned_requests,
    }

    return render(request, 'library_app/manage_requests.html', context)


@staff_member_required
def approve_request(request, request_id):
    book_request = get_object_or_404(BookRequest, id=request_id)# fetch the specific book request

    if book_request.book.available_copies < 1:
        messages.error(request, "No available copies to approve the request.")
        return redirect('manage_requests')

    # Mark request approved
    book_request.status = 'approved'
    book_request.approved_by = request.user
    book_request.save()

    # Create IssuedBook entry record within 14 days
    IssuedBook.objects.create(
        user=book_request.user,
        book=book_request.book,
        due_date=timezone.now().date() + timezone.timedelta(days=14),
        request=book_request
    )   

    # Reduce available copies
    book_request.book.available_copies -= 1
    book_request.book.save()

    messages.success(request, f"Book '{book_request.book.title}' issued to {book_request.user.username}.")
    return redirect('manage_requests')


@staff_member_required
def reject_request(request, request_id):
    book_request = get_object_or_404(BookRequest, id=request_id)
    book_request.status = 'rejected'
    book_request.approved_by = request.user
    book_request.save()

    messages.info(request, f"Request for '{book_request.book.title}' rejected.")
    return redirect('manage_requests')


from django.utils import timezone

@login_required
def my_requests(request):
    requests = BookRequest.objects.filter(user=request.user).order_by('-request_date')

    for req in requests:
        req.issued_book = IssuedBook.objects.filter(
            user=request.user,
            book=req.book,
            return_date__isnull=True
        ).first()

    context = {
        'requests': requests,
        'today': timezone.now().date(),  # ✅ ADD THIS LINE
    }
    return render(request, 'library_app/my_requests.html', context)
