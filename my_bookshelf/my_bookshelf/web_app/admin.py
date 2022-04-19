from django.contrib import admin

from my_bookshelf.web_app.models import Book, Bookshelf, BookCover


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'isbn', 'genre', 'date_added', 'user')
    ordering = ('id', 'title', 'author', 'date_added', 'isbn', 'genre', 'user')
    readonly_fields = ('user', 'isbn')
    list_filter = ('genre', 'date_added')


@admin.register(Bookshelf)
class BookshelfAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'date_added', 'user')
    ordering = ('id', 'title', 'date_added', 'user')
    readonly_fields = ('user', 'title')
    list_filter = ('date_added',)


@admin.register(BookCover)
class BookCoverAdmin(admin.ModelAdmin):
    list_display = ('book_id', 'book', 'image', 'date_added')
    ordering = ('book_id', 'book', 'date_added')
    list_filter = ('date_added',)
    list_display_links = ('image',)
