from datetime import date

from cloudinary import models as cloudinary_models
from django.contrib.auth import models as auth_models
from django.core import validators
from django.db import models

from my_bookshelf.auth_app.managers import MyBookshelfUsersManager
from my_bookshelf.auth_app.validators import validate_date_of_birth
from my_bookshelf.common.validators import validate_image_max_size_in_mb


class MyBookshelfUser(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    email = models.EmailField(
        unique=True,
        null=False,
        blank=False,
    )

    date_joined = models.DateTimeField(
        auto_now_add=True,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    is_superuser = models.BooleanField(
        default=False,
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

    date_of_birth = models.DateField(
        blank=True,
        null=True,
        validators=(
            validate_date_of_birth,
        ),
    )

    bio = models.TextField(
        null=True,
        blank=True,
    )

    user = models.OneToOneField(
        MyBookshelfUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    @property
    def age(self):
        today = date.today()
        return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class ProfilePicture(models.Model):
    picture = cloudinary_models.CloudinaryField(
        'image',
        validators=(
            validate_image_max_size_in_mb,
        ),
    )

    date_added = models.DateTimeField(
        auto_now_add=True,
    )

    user = models.OneToOneField(
        MyBookshelfUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )
