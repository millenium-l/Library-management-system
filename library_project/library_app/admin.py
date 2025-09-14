from django.contrib import admin
from .models import Profile, Book, IssuedBook, Publisher
# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'gender')
    search_fields = ('user__username', 'role')
    list_filter = ('role',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'category', 'description', 'total_copies', 'available_copies', 'publisher', 'added_by')
    search_fields = ('title', 'author', 'isbn' )
    list_filter = ('title', 'category',)

@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    search_fields = ('name', 'email')

@admin.register(IssuedBook)
class IssuedBookAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'issue_date', 'due_date', 'return_date', 'is_overdue_display')
    search_fields = ('book__title', 'user__username')
    list_filter = ('issue_date', 'due_date', 'return_date')

    def is_overdue_display(self, obj):
        return obj.is_overdue()
    is_overdue_display.boolean = True
    is_overdue_display.short_description = 'Overdue?'


#custom admin site header and title
admin.site.site_header = "Library Management Admin"
admin.site.site_title = "Library Management Admin Portal"
