from django.contrib.auth import mixins as auth_mixins
from django.urls import reverse_lazy
from django.views import generic as views

from my_bookshelf.web_app.models import BookCover, Book


class BookCoverCreateView(auth_mixins.LoginRequiredMixin, views.CreateView):
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


class BookCoverChangeView(auth_mixins.LoginRequiredMixin, views.UpdateView):
    model = BookCover
    template_name = 'web_app/book_cover_change.html'
    fields = ('image',)

    def get_success_url(self):
        book_id = self.request.session['book_id']
        return reverse_lazy('book details', kwargs={'pk': book_id})


class BookCoverDeleteView(auth_mixins.LoginRequiredMixin, views.DeleteView):
    model = BookCover
    template_name = 'web_app/book_cover_delete.html'

    def get_success_url(self):
        book_id = self.request.session['book_id']
        return reverse_lazy('book details', kwargs={'pk': book_id})
