from datetime import datetime, timedelta

from django.contrib.auth import mixins as auth_mixins
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic as views

from my_bookshelf.auth_app.models import Profile
from my_bookshelf.web_app.forms import CreateBookForm, CreateBookshelfForm, EditBookshelfForm, EditBookForm
from my_bookshelf.web_app.models import Book, Bookshelf, BookCover


class HomeView(views.TemplateView):
    template_name = 'web_app/home.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)


class DashboardView(auth_mixins.LoginRequiredMixin, views.ListView):
    model = Book
    template_name = 'web_app/dashboard.html'
    queryset = Book.objects.all().filter(date_added__gte=datetime.now() - timedelta(days=7))


class CreateBookView(auth_mixins.LoginRequiredMixin, views.CreateView):
    form_class = CreateBookForm
    template_name = 'web_app/book_add.html'
    success_url = reverse_lazy('dashboard')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class BookDetailsView(auth_mixins.LoginRequiredMixin, views.DetailView):
    model = Book
    template_name = 'web_app/book_details.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['owner'] = Profile.objects.get(user_id=self.object.user.id)
        self.request.session['book_id'] = self.object.id
        context['book_cover'] = BookCover.objects.all().filter(book_id=self.object.id).last()
        return context


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
    success_url = reverse_lazy('home')


class CreateBookshelfView(auth_mixins.LoginRequiredMixin, views.CreateView):
    form_class = CreateBookshelfForm
    template_name = 'web_app/bookshelf_add.html'
    success_url = reverse_lazy('dashboard')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class BookshelfDetailsView(auth_mixins.LoginRequiredMixin, views.DetailView):
    model = Bookshelf
    template_name = 'web_app/bookshelf_details.html'
    context_object_name = 'bookshelf'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books_list'] = self.object.books.all().order_by('title')
        context['owner'] = Profile.objects.get(user_id=self.object.user.id)
        return context


class EditBookshelfView(auth_mixins.LoginRequiredMixin, views.UpdateView):
    form_class = EditBookshelfForm
    model = Bookshelf
    template_name = 'web_app/bookshelf_edit.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['title'] = self.object.title
        return kwargs

    def get_success_url(self):
        return reverse_lazy('bookshelf details', kwargs={'pk': self.object.id})


class DeleteBookshelfView(auth_mixins.LoginRequiredMixin, views.DeleteView):
    model = Bookshelf
    template_name = 'web_app/bookshelf_delete.html'
    success_url = reverse_lazy('home')


class MyBooksListView(auth_mixins.LoginRequiredMixin, views.ListView):
    model = Book
    template_name = 'web_app/my_books.html'

    def get_queryset(self):
        return Book.objects.all().filter(user_id=self.request.user.id).order_by('-date_added')


class MyBookshelvesListView(auth_mixins.LoginRequiredMixin, views.ListView):
    model = Bookshelf
    template_name = 'web_app/my_bookshelves.html'

    def get_queryset(self):
        return Bookshelf.objects.all().filter(user_id=self.request.user.id).order_by('title')


class ProfilesListView(auth_mixins.LoginRequiredMixin, views.ListView):
    model = Profile
    template_name = 'web_app/profiles_list.html'
    queryset = Profile.objects.all().order_by('first_name', 'last_name')


class BooksListView(auth_mixins.LoginRequiredMixin, views.ListView):
    model = Book
    template_name = 'web_app/books_list.html'
    queryset = Book.objects.all().order_by('title')


class BookshelvesListView(auth_mixins.LoginRequiredMixin, views.ListView):
    model = Bookshelf
    template_name = 'web_app/bookshelves_list.html'
    queryset = Bookshelf.objects.all().order_by('title')


class CreateBookCoverView(auth_mixins.LoginRequiredMixin, views.CreateView):
    model = BookCover
    template_name = 'web_app/book_cover_add.html'
    fields = ('image',)

    def get_success_url(self):
        book_id = self.request.session['book_id']
        return reverse_lazy('book details', kwargs={'pk': book_id})

    def form_valid(self, form):
        book_id = self.request.session['book_id']
        form.instance.book = Book.objects.get(id=book_id)
        return super().form_valid(form)


class ChangeBookCoverView(auth_mixins.LoginRequiredMixin, views.UpdateView):
    model = BookCover
    template_name = 'web_app/book_cover_change.html'
    fields = ('image',)

    def get_success_url(self):
        book_id = self.request.session['book_id']
        return reverse_lazy('book details', kwargs={'pk': book_id})


class DeleteBookCoverView(auth_mixins.LoginRequiredMixin, views.DeleteView):
    model = BookCover
    template_name = 'web_app/book_cover_delete.html'

    def get_success_url(self):
        book_id = self.request.session['book_id']
        return reverse_lazy('book details', kwargs={'pk': book_id})
