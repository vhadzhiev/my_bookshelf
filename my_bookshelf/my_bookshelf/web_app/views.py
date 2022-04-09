from django.shortcuts import redirect
from django.views import generic as views

from my_bookshelf.auth_app.models import Profile


class HomeView(views.TemplateView):
    template_name = 'web_app/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['hide_additional_nav_items'] = True
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)


class DashboardView(views.ListView):
    model = Profile
    template_name = 'web_app/dashboard.html'



