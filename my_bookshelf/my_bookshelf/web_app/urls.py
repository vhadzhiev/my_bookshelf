from django.urls import path

from my_bookshelf.web_app.views.book_covers import BookCoverCreateView, BookCoverChangeView, BookCoverDeleteView
from my_bookshelf.web_app.views.books import BookCreateView, BookEditView, BookDeleteView, BookDetailsView, \
    BooksListView, BooksByGenreListView
from my_bookshelf.web_app.views.bookshelves import BookshelfCreateView, BookshelfEditView, BookshelfDeleteView, \
    BookshelfDetailsView, BookshelvesListView
from my_bookshelf.web_app.views.generic import HomeView, DashboardView

urlpatterns = (
    path('', HomeView.as_view(), name='home'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    path('book/add/', BookCreateView.as_view(), name='book add'),
    path('book/edit/<int:pk>/', BookEditView.as_view(), name='book edit'),
    path('book/delete/<int:pk>/', BookDeleteView.as_view(), name='book delete'),
    path('book/<int:pk>/', BookDetailsView.as_view(), name='book details'),

    path('books/list/', BooksListView.as_view(), name='books list'),
    path('books/list/genre/', BooksByGenreListView.as_view(), name='books list by genre'),

    path('book/cover/add/', BookCoverCreateView.as_view(), name='book cover add'),
    path('book/cover/edit/<int:pk>/', BookCoverChangeView.as_view(), name='book cover change'),
    path('book/cover/delete/<int:pk>/', BookCoverDeleteView.as_view(), name='book cover delete'),

    path('bookshelf/add/', BookshelfCreateView.as_view(), name='bookshelf add'),
    path('bookshelf/edit/<int:pk>/', BookshelfEditView.as_view(), name='bookshelf edit'),
    path('bookshelf/delete/<int:pk>/', BookshelfDeleteView.as_view(), name='bookshelf delete'),
    path('bookshelf/<int:pk>/', BookshelfDetailsView.as_view(), name='bookshelf details'),
    path('bookshelves/list/', BookshelvesListView.as_view(), name='bookshelves list'),
)
