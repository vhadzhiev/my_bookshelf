from django.contrib.auth import mixins as auth_mixins
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy


class ChangeUserPasswordView(auth_mixins.LoginRequiredMixin, auth_views.PasswordChangeView):
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
