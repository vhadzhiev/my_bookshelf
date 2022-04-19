from django.contrib import admin
from django.contrib.auth import get_user_model

from my_bookshelf.auth_app.models import Profile, ProfilePicture

UserModel = get_user_model()


@admin.register(UserModel)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'date_joined', 'last_login', 'is_superuser', 'is_staff', 'is_active')
    readonly_fields = ('id', 'last_login', 'password')
    ordering = ('id', 'email', 'date_joined', 'last_login', 'is_superuser', 'is_staff', 'is_active')
    list_filter = ('date_joined', 'last_login', 'is_superuser', 'is_staff', 'is_active')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'first_name', 'last_name', 'user')
    readonly_fields = ('user',)
    ordering = ('user_id', 'first_name', 'last_name', 'user')
    list_display_links = ('first_name', 'last_name')


@admin.register(ProfilePicture)
class ProfilePictureAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'user', 'picture', 'date_added')
    ordering = ('user_id', 'user', 'picture', 'date_added')
    list_filter = ('date_added',)
    list_display_links = ('picture',)
