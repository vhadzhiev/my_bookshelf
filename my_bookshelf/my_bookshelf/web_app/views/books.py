from django.contrib.auth import mixins as auth_mixins
from django.db.models.functions import Lower
from django.urls import reverse_lazy
from django.views import generic as views

from my_bookshelf.auth_app.models import Profile
from my_bookshelf.web_app.forms import BookCreateForm, BookEditForm
from my_bookshelf.common.views_mixins import SearchBarMixin
from my_bookshelf.web_app.models import Book, BookCover


class BookCreateView(auth_mixins.LoginRequiredMixin, views.CreateView):
    form_class = BookCreateForm
    template_name = 'web_app/book_add.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('profile books', kwargs={'pk': self.object.user.id})


class BookEditView(auth_mixins.LoginRequiredMixin, views.UpdateView):
    form_class = BookEditForm
    model = Book
    template_name = 'web_app/book_edit.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['isbn'] = self.object.isbn
        return kwargs

    def get_success_url(self):
        return reverse_lazy('book details', kwargs={'pk': self.object.id})


class BookDeleteView(auth_mixins.LoginRequiredMixin, views.DeleteView):
    model = Book
    template_name = 'web_app/book_delete.html'
    success_url = reverse_lazy('profile books')

    def get_success_url(self):
        return reverse_lazy('profile books', kwargs={'pk': self.object.user.id})


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


class BooksListView(SearchBarMixin, views.ListView):
    model = Book
    template_name = 'web_app/books_list.html'
    queryset = Book.objects.order_by(Lower('title')).filter(user__is_active=True)
    paginate_by = 10


class BooksByGenreListView(SearchBarMixin, views.ListView):
    model = Book
    template_name = 'web_app/books_by_genre_list.html'
    queryset = Book.objects.order_by(Lower('title')).filter(user__is_active=True)
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        book_genre = self.request.session['book_genre']
        queryset = queryset.filter(genre=book_genre)
        return queryset
