from django.views import generic as views


class HomeView(views.TemplateView):
    template_name = 'web_app/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hide_additional_nav_items'] = True
        return context
