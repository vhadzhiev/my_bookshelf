from django.contrib.auth import mixins as auth_mixins
from django.urls import reverse_lazy
from django.views import generic as views

from my_bookshelf.auth_app.models import Profile
from my_bookshelf.web_app.forms import CreateBookForm, EditBookForm
from my_bookshelf.web_app.models import Book, BookCover


class CreateBookView(auth_mixins.LoginRequiredMixin, views.CreateView):
    form_class = CreateBookForm
    template_name = 'web_app/book_add.html'
    success_url = reverse_lazy('profile books')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class EditBookView(auth_mixins.LoginRequiredMixin, views.UpdateView):
    form_class = EditBookForm
    model = Book
    template_name = 'web_app/book_edit.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['isbn'] = self.object.isbn
        return kwargs

    def get_success_url(self):
        return reverse_lazy('book details', kwargs={'pk': self.object.id})


class DeleteBookView(auth_mixins.LoginRequiredMixin, views.DeleteView):
    model = Book
    template_name = 'web_app/book_delete.html'
    success_url = reverse_lazy('profile books')


class BookDetailsView(views.DetailView):
    model = Book
    template_name = 'web_app/book_details.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['owner'] = Profile.objects.get(user_id=self.object.user.id)
        self.request.session['book_id'] = self.object.id
        self.request.session['book_genre'] = self.object.genre

        try:
            context['book_cover'] = BookCover.objects.get(book_id=self.object.id)
        except BookCover.DoesNotExist:
            context['book_cover'] = None

        return context


class BooksListView(views.ListView):
    model = Book
    template_name = 'web_app/books_list.html'
    queryset = Book.objects.order_by('title')
    paginate_by = 10


class BooksByGenreListView(views.ListView):
    model = Book
    template_name = 'web_app/books_by_genre_list.html'
    paginate_by = 10

    def get_queryset(self):
        book_genre = self.request.session['book_genre']
        queryset = Book.objects.filter(genre=book_genre).order_by('title')
        return queryset


