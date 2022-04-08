from django.urls import path

from my_bookshelf.web_app.views import HomeView

urlpatterns = (
    path('', HomeView.as_view(), name='home'),
)
