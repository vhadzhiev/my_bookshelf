from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic as views

from my_bookshelf.web_app.forms import CreateBookForm, CreateBookshelfForm
from my_bookshelf.web_app.models import Book, Bookshelf


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

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class BookDetailsView(views.DetailView):
    model = Book
    template_name = 'web_app/book_details.html'
    context_object_name = 'book'


class EditBookView(views.UpdateView):
    model = Book
    template_name = 'web_app/book_edit.html'
    fields = ('title', 'isbn', 'author', 'genre', 'summary')

    def get_success_url(self):
        return reverse_lazy('book details', kwargs={'pk': self.object.id})


class DeleteBookView(views.DeleteView):
    model = Book
    template_name = 'web_app/book_delete.html'
    success_url = reverse_lazy('home')


class CreateBookshelfView(views.CreateView):
    form_class = CreateBookshelfForm
    template_name = 'web_app/bookshelf_add.html'
    success_url = reverse_lazy('dashboard')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class BookshelfDetailsView(views.DetailView):
    model = Bookshelf
    template_name = 'web_app/bookshelf_details.html'
    context_object_name = 'bookshelf'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books_list'] = self.object.books.all()
        return context


class EditBookshelfView(views.UpdateView):
    model = Bookshelf
    template_name = 'web_app/bookshelf_edit.html'
    fields = ('title', 'description')

    def get_success_url(self):
        return reverse_lazy('bookshelf details', kwargs={'pk': self.object.id})


class DeleteBookshelfView(views.DeleteView):
    model = Bookshelf
    template_name = 'web_app/bookshelf_delete.html'
    success_url = reverse_lazy('home')
