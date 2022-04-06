from django.urls import path

from my_bookshelf.auth_app.views import UserRegistrationView, UserLoginView, UserLogoutView, ChangePasswordView

urlpatterns = (
    path('register/', UserRegistrationView.as_view(), name='register user'),
    path('login/', UserLoginView.as_view(), name='login user'),
    path('logout/', UserLogoutView.as_view(), name='logout user'),
    path('change_password/', ChangePasswordView.as_view(), name='change password'),
    # path('accounts/', include('django.contrib.auth.urls')),
)
