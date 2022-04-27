from django.contrib.auth import get_user_model, login
from django.urls import reverse_lazy
from django.views import generic as views
from django.contrib.auth import views as auth_views
from django.contrib.auth import mixins as auth_mixins

from my_bookshelf.auth_app.forms import UserRegisterForm

UserModel = get_user_model()


class UserRegisterView(views.CreateView):
    form_class = UserRegisterForm
    template_name = 'auth_app/register_user.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        result = super().form_valid(form)
        user = self.object
        request = self.request
        login(request, user)
        return result


class UserLoginView(auth_views.LoginView):
    template_name = 'auth_app/login_user.html'

    def get_success_url(self):
        return reverse_lazy('dashboard')


class UserLogoutView(auth_mixins.LoginRequiredMixin, auth_views.LogoutView):
    template_name = 'auth_app/logout_user.html'
