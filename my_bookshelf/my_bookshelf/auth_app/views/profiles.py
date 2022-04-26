from django.contrib.auth import mixins as auth_mixins, get_user_model
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic as views

from my_bookshelf.auth_app.forms import EditProfileForm
from my_bookshelf.auth_app.models import Profile, ProfilePicture
from my_bookshelf.common.mixins import SearchBarMixin
from my_bookshelf.web_app.models import Book, Bookshelf

UserModel = get_user_model()


class ProfileDetailsView(auth_mixins.LoginRequiredMixin, views.DetailView):
    model = Profile
    template_name = 'auth_app/profile_details.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books_count'] = len(Book.objects.filter(user_id=self.object.user_id))
        context['bookshelves_count'] = len(Bookshelf.objects.filter(user_id=self.object.user_id))

        try:
            context['profile_picture'] = ProfilePicture.objects.get(user_id=self.object.user_id)
        except ProfilePicture.DoesNotExist:
            context['profile_picture'] = None

        return context


class ProfileEditView(auth_mixins.LoginRequiredMixin, views.UpdateView):
    form_class = EditProfileForm
    model = Profile
    template_name = 'auth_app/profile_edit.html'

    def get_success_url(self):
        return reverse_lazy('profile details', kwargs={'pk': self.object.user_id})


class ProfileDeleteView(auth_mixins.LoginRequiredMixin, views.DeleteView):
    model = UserModel
    template_name = 'auth_app/profile_delete.html'

    def form_valid(self, form):
        user = self.object
        user.is_active = False
        user.save()
        Profile.objects.get(pk=user.id).delete()
        ProfilePicture.objects.filter(user_id=self.object.id).delete()
        Book.objects.filter(user_id=user.id).delete()
        Bookshelf.objects.filter(user_id=user.id).delete()
        return redirect('home')


class ProfileBooksListView(auth_mixins.LoginRequiredMixin, SearchBarMixin, views.ListView):
    model = Book
    template_name = 'auth_app/profile_books.html'
    queryset = Book.objects.order_by('title')
    paginate_by = 10

    def get_queryset(self):
        object_list = super().get_queryset()
        queryset = object_list.filter(user_id=self.request.user.id)
        return queryset


class ProfileBookshelvesListView(auth_mixins.LoginRequiredMixin, SearchBarMixin, views.ListView):
    model = Bookshelf
    template_name = 'auth_app/profile_bookshelves.html'
    queryset = Bookshelf.objects.order_by('title')
    paginate_by = 10

    def get_queryset(self):
        object_list = super().get_queryset()
        queryset = object_list.filter(user_id=self.request.user.id)
        return queryset


class ProfilesListView(auth_mixins.LoginRequiredMixin, views.ListView):
    model = Profile
    template_name = 'auth_app/profiles_list.html'
    queryset = Profile.objects.order_by('first_name', 'last_name')
    paginate_by = 10