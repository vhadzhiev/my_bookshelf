from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic as views

from my_bookshelf.auth_app.models import MyBookshelfUser
from my_bookshelf.web_app.forms import CreateBookForm
from my_bookshelf.web_app.models import Book


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
    model = Book
    template_name = 'web_app/dashboard.html'


class CreateBookView(views.CreateView):
    form_class = CreateBookForm
    template_name = 'web_app/book_add.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        user = MyBookshelfUser.objects.get(pk=self.request.user.id)
        form.instance.user = user
        return super().form_valid(form)


class BookDetailsView(views.DetailView):
    model = Book
    template_name = 'web_app/book_details.html'
    context_object_name = 'book'


class EditBookView(views.UpdateView):
    model = Book
    template_name = 'web_app/book_edit.html'
    fields = ('title', 'isbn', 'author', 'genre', 'description')

    def get_success_url(self):
        return reverse_lazy('book details', kwargs={'pk': self.object.id})


class DeleteBookView(views.DeleteView):
    model = Book
    template_name = 'web_app/book_delete.html'
    success_url = reverse_lazy('home')
