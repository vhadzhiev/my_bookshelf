from django.urls import path, include
from django.views.generic import TemplateView

from my_bookshelf.auth_app.views import UserRegistrationView, UserLoginView, UserLogoutView, ChangePasswordView, \
    ResetPasswordView, ResetPasswordConfirmView, ResetPasswordDoneView, ResetPasswordCompleteView

urlpatterns = (
    path('register/', UserRegistrationView.as_view(), name='register user'),
    path('login/', UserLoginView.as_view(), name='login user'),
    path('logout/', UserLogoutView.as_view(), name='logout user'),
    path('password_change/', ChangePasswordView.as_view(), name='password change'),
    path('password_change_done/', TemplateView.as_view(template_name='auth/password_change_done.html'),
         name='password change done'),
    path('password_reset/', ResetPasswordView.as_view(), name='password reset'),
    path('password_reset_done/', ResetPasswordDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', ResetPasswordConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_done/', ResetPasswordCompleteView.as_view(), name='password_reset_complete'),
)
