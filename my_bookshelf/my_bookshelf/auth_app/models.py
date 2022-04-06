from django.contrib.auth import models as auth_models
from django.db import models

from my_bookshelf.auth_app.managers import MyBookshelfUsersManager


class MyBookshelfUser(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    email = models.EmailField(
        unique=True,
        null=False,
        blank=False,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    date_joined = models.DateTimeField(
        auto_now_add=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    USERNAME_FIELD = 'email'

    objects = MyBookshelfUsersManager()


class Profile(models.Model):
    FIRST_NAME_MAX_LEN = 25
    LAST_NAME_MAX_LEN = 25

    first_name = models.CharField(
        max_length=FIRST_NAME_MAX_LEN,
    )

    last_name = models.CharField(
        max_length=LAST_NAME_MAX_LEN,
    )

    user = models.OneToOneField(
        MyBookshelfUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
