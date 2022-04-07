from django import forms
from django.contrib.auth import forms as auth_forms, get_user_model, login
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.views import generic as views

from my_bookshelf.auth_app.models import Profile

UserModel = get_user_model()


class UserRegistrationForm(auth_forms.UserCreationForm):
    first_name = forms.CharField(
        max_length=Profile.FIRST_NAME_MAX_LEN,
    )

    last_name = forms.CharField(
        max_length=Profile.LAST_NAME_MAX_LEN,
    )

    class Meta:
        model = UserModel
        fields = ('email',)

    def save(self, commit=True):
        user = super().save(commit=commit)
        profile = Profile(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            user=user,
        )
        if commit:
            profile.save()
        return user


class UserRegistrationView(views.CreateView):
    form_class = UserRegistrationForm
    template_name = 'auth/register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        result = super().form_valid(form)
        user = self.object
        request = self.request
        login(request, user)
        return result


class UserLoginView(auth_views.LoginView):
    template_name = 'auth/login.html'

    def get_success_url(self):
        next = self.request.GET.get('next', None)
        if next:
            return next
        return reverse_lazy('home')


class UserLogoutView(auth_views.LogoutView):
    template_name = 'auth/logout.html'


class ChangePasswordView(auth_views.PasswordChangeView):
    template_name = 'auth/password_change.html'

    def get_success_url(self):
        return reverse_lazy('password change done')


class ResetPasswordView(auth_views.PasswordResetView):
    template_name = 'auth/password_reset.html'


class ResetPasswordDoneView(auth_views.PasswordResetDoneView):
    template_name = 'auth/password_reset_done.html'


class ResetPasswordConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'auth/password_reset_confirm.html'


class ResetPasswordCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'auth/password_reset_complete.html'
