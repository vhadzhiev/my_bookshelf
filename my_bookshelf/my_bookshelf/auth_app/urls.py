from django.urls import path
from django.views import generic as views

from my_bookshelf.auth_app.views.passwords import ChangeUserPasswordView, ResetUserPasswordView, \
    ResetUserPasswordDoneView, ResetUserPasswordConfirmView, ResetUserPasswordCompleteView
from my_bookshelf.auth_app.views.profile_pictures import CreateProfilePictureView, ChangeProfilePictureView, \
    DeleteProfilePictureView
from my_bookshelf.auth_app.views.profiles import ProfileDetailsView, ProfileEditView, ProfileDeleteView, \
    ProfilesListView, ProfileBooksListView, ProfileBookshelvesListView
from my_bookshelf.auth_app.views.users import UserRegisterView, UserLoginView, UserLogoutView

urlpatterns = (
    path('register/', UserRegisterView.as_view(), name='register user'),
    path('login/', UserLoginView.as_view(), name='login user'),
    path('logout/', UserLogoutView.as_view(), name='logout user'),

    path('profile/<int:pk>/', ProfileDetailsView.as_view(), name='profile details'),
    path('profile/edit/<int:pk>/', ProfileEditView.as_view(), name='profile edit'),
    path('profile/delete/<int:pk>/', ProfileDeleteView.as_view(), name='profile delete'),
    path('profiles/list/', ProfilesListView.as_view(), name='profiles list'),

    path('profile/<int:pk>/books/', ProfileBooksListView.as_view(), name='profile books'),
    path('profile/<int:pk>/bookshelves/', ProfileBookshelvesListView.as_view(), name='profile bookshelves'),

    path('profile/picture/add/', CreateProfilePictureView.as_view(), name='profile picture create'),
    path('profile/picture/edit/<int:pk>', ChangeProfilePictureView.as_view(), name='profile picture change'),
    path('profile/picture/delete/<int:pk>', DeleteProfilePictureView.as_view(), name='profile picture delete'),

    path('password/change/<int:pk>/', ChangeUserPasswordView.as_view(), name='password change'),
    path('password/change/done/', views.TemplateView.as_view(template_name='auth_app/password_change_done.html'),
         name='password change done'),
    path('password/reset/', ResetUserPasswordView.as_view(), name='password reset'),
    path('password/reset/done/', ResetUserPasswordDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', ResetUserPasswordConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', ResetUserPasswordCompleteView.as_view(), name='password_reset_complete'),
)
