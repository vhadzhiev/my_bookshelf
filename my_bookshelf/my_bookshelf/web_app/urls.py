from django.urls import path

from my_bookshelf.web_app.views import HomeView, DashboardView

urlpatterns = (
    path('', HomeView.as_view(), name='home'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
)
