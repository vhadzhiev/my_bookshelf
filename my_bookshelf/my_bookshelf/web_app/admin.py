from django.contrib import admin

from my_bookshelf.web_app.models import Book, Bookshelf


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'genre', 'date_added', 'user')
    ordering = ('title', 'author', 'date_added', 'user')
    list_filter = ('genre', 'user')


@admin.register(Bookshelf)
class BookshelfAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_added', 'user')
    ordering = ('title', 'date_added', 'user')
    list_filter = ('user',)
