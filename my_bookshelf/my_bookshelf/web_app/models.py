from cloudinary import models as cloudinary_models
from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models

from my_bookshelf.auth_app.models import Profile
from my_bookshelf.common.validators import validate_image_max_size_in_mb, IMAGE_MAX_FILE_SIZE_IN_MB
from my_bookshelf.web_app.validators import validate_only_digits, validate_correct_length

UserModel = get_user_model()


class Book(models.Model):
    ADVENTURE = 'Adventure'
    BIOGRAPHIES = 'Biographies'
    BUSINESS = 'Business'
    CHILDREN = 'Children\'s'
    CRIME = 'Crime'
    HEALTH = 'Health'
    HISTORY = 'History'
    HOBBIES = 'Hobbies'
    FANTASY = 'Fantasy'
    FICTION = 'Fiction'
    SCIENCE = 'Science'
    SPORTS = 'Sports'
    TECH = 'Tech'
    OTHER = 'Other'

    GENRES = [(x, x) for x in (ADVENTURE, BIOGRAPHIES, BUSINESS, CHILDREN, CRIME, HEALTH, HISTORY, HOBBIES, FANTASY,
                               FICTION, SCIENCE, SPORTS, TECH, OTHER)]

    TITLE_MAX_LEN = 100
    ISBN_MAX_LEN = 13
    AUTHOR_MAX_LEN = 50

    title = models.CharField(
        max_length=TITLE_MAX_LEN,
    )

    author = models.CharField(
        max_length=AUTHOR_MAX_LEN,
    )

    isbn = models.CharField(
        max_length=ISBN_MAX_LEN,
        validators=(
            validate_only_digits,
            validate_correct_length,
        ),
        verbose_name='ISBN',
        help_text='Book\'s unique identifier. ISBN consists only of digits and must be 10 or 13 symbols long.',
    )

    genre = models.CharField(
        max_length=max(len(x) for (x, _) in GENRES),
        choices=GENRES
    )

    date_added = models.DateTimeField(
        auto_now_add=True,
    )

    summary = models.TextField(
        null=True,
        blank=True,
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.title


class Bookshelf(models.Model):
    TITLE_MAX_LEN = 100

    title = models.CharField(
        max_length=TITLE_MAX_LEN,
    )

    date_added = models.DateTimeField(
        auto_now_add=True,
    )

    description = models.TextField(
        blank=True,
        null=True,
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    books = models.ManyToManyField(
        Book,
        blank=True,
        null=True,
        help_text='Please, choose the books, that you want to include in this bookshelf.'
    )

    def __str__(self):
        return self.title


class BookCover(models.Model):
    image = cloudinary_models.CloudinaryField(
        'image',
        validators=(
            validate_image_max_size_in_mb,
        ),
        help_text=f'The maximum allowed image size is {IMAGE_MAX_FILE_SIZE_IN_MB} MB'
    )

    date_added = models.DateTimeField(
        auto_now_add=True,
    )

    book = models.OneToOneField(
        Book,
        on_delete=models.CASCADE,
        primary_key=True,
    )
