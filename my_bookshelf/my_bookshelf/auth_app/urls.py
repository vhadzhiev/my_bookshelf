from django.urls import path
from django.views import generic as views

from my_bookshelf.auth_app.views import UserRegisterView, UserLoginView, UserLogoutView, ChangeUserPasswordView, \
    ResetUserPasswordView, ResetUserPasswordConfirmView, ResetUserPasswordDoneView, ResetUserPasswordCompleteView

urlpatterns = (
    path('register/', UserRegisterView.as_view(), name='register user'),
    path('login/', UserLoginView.as_view(), name='login user'),
    path('logout/', UserLogoutView.as_view(), name='logout user'),

    path('password_change/', ChangeUserPasswordView.as_view(), name='password change'),
    path('password_change_done/', views.TemplateView.as_view(template_name='auth_app/password_change_done.html'),
         name='password change done'),

    path('password_reset/', ResetUserPasswordView.as_view(), name='password reset'),
    path('password_reset_done/', ResetUserPasswordDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', ResetUserPasswordConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_done/', ResetUserPasswordCompleteView.as_view(), name='password_reset_complete'),
)
