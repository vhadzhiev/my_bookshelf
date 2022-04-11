from django.contrib.auth import get_user_model, login
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect

from django.urls import reverse_lazy
from django.views import generic as views

from my_bookshelf.auth_app.forms import UserRegisterForm
from my_bookshelf.auth_app.models import Profile, MyBookshelfUser
from my_bookshelf.web_app.models import Book, Bookshelf

UserModel = get_user_model()


class UserRegisterView(views.CreateView):
    form_class = UserRegisterForm
    template_name = 'auth_app/register.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        result = super().form_valid(form)
        user = self.object
        request = self.request
        login(request, user)
        return result


class UserLoginView(auth_views.LoginView):
    template_name = 'auth_app/login.html'
    success_url = reverse_lazy('dashboard')

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        return super().get_success_url()


class UserLogoutView(auth_views.LogoutView):
    template_name = 'auth_app/logout.html'


class ChangeUserPasswordView(auth_views.PasswordChangeView):
    template_name = 'auth_app/password_change.html'
    success_url = reverse_lazy('password change done')


class ResetUserPasswordView(auth_views.PasswordResetView):
    template_name = 'auth_app/password_reset.html'


class ResetUserPasswordDoneView(auth_views.PasswordResetDoneView):
    template_name = 'auth_app/password_reset_done.html'


class ResetUserPasswordConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'auth_app/password_reset_confirm.html'


class ResetUserPasswordCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'auth_app/password_reset_complete.html'


class ProfileDetailsView(views.DetailView):
    model = Profile
    template_name = 'auth_app/profile_details.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books_count'] = len(Book.objects.all().filter(user_id=self.object.user_id))
        context['bookshelves_count'] = len(Bookshelf.objects.all().filter(user_id=self.object.user_id))
        return context


class ProfileEditView(views.UpdateView):
    model = Profile
    template_name = 'auth_app/profile_edit.html'
    fields = ('first_name', 'last_name', 'date_of_birth', 'bio')

    def get_success_url(self):
        return reverse_lazy('profile details', kwargs={'pk': self.object.user_id})


class ProfileDeleteView(views.DeleteView):
    model = MyBookshelfUser
    template_name = 'auth_app/profile_delete.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = self.object
        user.is_active = False
        user.save()
        Profile.objects.get(pk=user.id).delete()
        Book.objects.filter(user_id=user.id).delete()
        Bookshelf.objects.filter(user_id=user.id).delete()
        return redirect('home')


