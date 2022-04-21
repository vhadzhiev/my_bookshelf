from django.shortcuts import redirect
from django.utils import timezone
from django.views import generic as views

from my_bookshelf.web_app.models import Book

DAYS_FOR_RECENTLY_ADDED_BOOKS = 7


class HomeView(views.TemplateView):
    template_name = 'web_app/home.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)


class DashboardView(views.ListView):
    model = Book
    template_name = 'web_app/dashboard.html'
    queryset = Book.objects \
                   .filter(date_added__gte=timezone.now() - timezone.timedelta(days=DAYS_FOR_RECENTLY_ADDED_BOOKS)) \
                   .order_by('-date_added')[:10]
