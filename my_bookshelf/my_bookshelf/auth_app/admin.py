from django.contrib import admin

from my_bookshelf.auth_app.models import Profile, MyBookshelfUser


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'first_name', 'last_name', 'user')
    ordering = ('user_id', 'first_name', 'last_name', 'user')
    list_filter = ('user_id', 'first_name', 'last_name', 'user')


@admin.register(MyBookshelfUser)
class MyBookshelfUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'date_joined', 'last_login', 'is_superuser', 'is_staff', 'is_active')
    ordering = ('id', 'email', 'date_joined', 'last_login', 'is_superuser', 'is_staff', 'is_active')
    list_filter = ('id', 'email', 'date_joined', 'last_login', 'is_superuser', 'is_staff', 'is_active')
