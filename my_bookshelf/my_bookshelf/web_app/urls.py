from django.urls import path

from my_bookshelf.web_app.views.book_covers import CreateBookCoverView, ChangeBookCoverView, DeleteBookCoverView
from my_bookshelf.web_app.views.books import CreateBookView, EditBookView, DeleteBookView, BookDetailsView, \
    BooksListView, BooksByGenreListView
from my_bookshelf.web_app.views.bookshelves import CreateBookshelfView, EditBookshelfView, DeleteBookshelfView, \
    BookshelfDetailsView, BookshelvesListView
from my_bookshelf.web_app.views.generic import HomeView, DashboardView

urlpatterns = (
    path('', HomeView.as_view(), name='home'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    path('book/add/', CreateBookView.as_view(), name='book add'),
    path('book/edit/<int:pk>/', EditBookView.as_view(), name='book edit'),
    path('book/delete/<int:pk>/', DeleteBookView.as_view(), name='book delete'),
    path('book/<int:pk>/', BookDetailsView.as_view(), name='book details'),

    path('books/list/', BooksListView.as_view(), name='books list'),
    path('books/list/genre/', BooksByGenreListView.as_view(), name='books list by genre'),

    path('book/cover/add/', CreateBookCoverView.as_view(), name='book cover add'),
    path('book/cover/edit/<int:pk>/', ChangeBookCoverView.as_view(), name='book cover change'),
    path('book/cover/delete/<int:pk>/', DeleteBookCoverView.as_view(), name='book cover delete'),

    path('bookshelf/add/', CreateBookshelfView.as_view(), name='bookshelf add'),
    path('bookshelf/edit/<int:pk>/', EditBookshelfView.as_view(), name='bookshelf edit'),
    path('bookshelf/delete/<int:pk>/', DeleteBookshelfView.as_view(), name='bookshelf delete'),
    path('bookshelf/<int:pk>/', BookshelfDetailsView.as_view(), name='bookshelf details'),
    path('bookshelves/list/', BookshelvesListView.as_view(), name='bookshelves list'),
)
