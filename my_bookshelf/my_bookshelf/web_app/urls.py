from django.urls import path

from my_bookshelf.web_app.views import HomeView, DashboardView, CreateBookView, EditBookView, DeleteBookView, \
    BookDetailsView, CreateBookshelfView, EditBookshelfView, DeleteBookshelfView, BookshelfDetailsView, MyBooksListView, \
    MyBookshelvesListView, ProfilesListView, BooksListView, BookshelvesListView

urlpatterns = (
    path('', HomeView.as_view(), name='home'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    path('book/add/', CreateBookView.as_view(), name='book add'),
    path('book/edit/<int:pk>/', EditBookView.as_view(), name='book edit'),
    path('book/delete/<int:pk>/', DeleteBookView.as_view(), name='book delete'),
    path('book/<int:pk>/', BookDetailsView.as_view(), name='book details'),

    path('bookshelf/add/', CreateBookshelfView.as_view(), name='bookshelf add'),
    path('bookshelf/edit/<int:pk>/', EditBookshelfView.as_view(), name='bookshelf edit'),
    path('bookshelf/delete/<int:pk>/', DeleteBookshelfView.as_view(), name='bookshelf delete'),
    path('bookshelf/<int:pk>/', BookshelfDetailsView.as_view(), name='bookshelf details'),

    path('my_books/', MyBooksListView.as_view(), name='my books'),
    path('my_bookshelves/', MyBookshelvesListView.as_view(), name='my bookshelves'),

    path('profiles/list/', ProfilesListView.as_view(), name='profiles list'),
    path('books/list/', BooksListView.as_view(), name='books list'),
    path('bookshelves/list/', BookshelvesListView.as_view(), name='bookshelves list'),
)
