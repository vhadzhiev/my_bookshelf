from django.urls import path

from my_bookshelf.web_app.views import HomeView, DashboardView, CreateBookView, EditBookView, DeleteBookView, \
    BookDetailsView

urlpatterns = (
    path('', HomeView.as_view(), name='home'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    path('book/add/', CreateBookView.as_view(), name='book add'),
    path('book/edit/<int:pk>/', EditBookView.as_view(), name='book edit'),
    path('book/delete/<int:pk>/', DeleteBookView.as_view(), name='book delete'),
    path('book/<int:pk>/', BookDetailsView.as_view(), name='book details'),
)
