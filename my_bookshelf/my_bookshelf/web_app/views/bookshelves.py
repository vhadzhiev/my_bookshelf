from django.contrib.auth import mixins as auth_mixins
from django.urls import reverse_lazy
from django.views import generic as views

from my_bookshelf.auth_app.models import Profile
from my_bookshelf.web_app.forms import CreateBookshelfForm, EditBookshelfForm
from my_bookshelf.web_app.models import Bookshelf


class CreateBookshelfView(auth_mixins.LoginRequiredMixin, views.CreateView):
    form_class = CreateBookshelfForm
    template_name = 'web_app/bookshelf_add.html'
    success_url = reverse_lazy('profile bookshelves')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


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
    success_url = reverse_lazy('profile bookshelves')


class BookshelfDetailsView(views.DetailView):
    model = Bookshelf
    template_name = 'web_app/bookshelf_details.html'
    context_object_name = 'bookshelf'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books_list'] = self.object.books.all().order_by('title')
        context['owner'] = Profile.objects.get(user_id=self.object.user.id)
        return context


class BookshelvesListView(views.ListView):
    model = Bookshelf
    template_name = 'web_app/bookshelves_list.html'
    queryset = Bookshelf.objects.order_by('title')
    paginate_by = 10
