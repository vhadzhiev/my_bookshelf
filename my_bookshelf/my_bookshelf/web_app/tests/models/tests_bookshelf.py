from django.core.exceptions import ValidationError
from django.test import TestCase

from django.contrib.auth import get_user_model

from my_bookshelf.web_app.models import Bookshelf

UserModel = get_user_model()


class ValidUserMixin:
    VALID_USER_CREDENTIALS = {
        'email': 'vaski@gmail.com',
        'password': '123456',
    }

    def create_valid_user(self):
        user = UserModel.objects.create_user(**self.VALID_USER_CREDENTIALS)
        return user


class BookshelfTests(ValidUserMixin, TestCase):
    def test_create__when_all_valid__should_create_bookshelf(self):
        user = self.create_valid_user()
        bookshelf = Bookshelf.objects.create(title='Favourites', user=user)
        self.assertIsNotNone(bookshelf)
        self.assertEqual(bookshelf.user_id, user.id)
        self.assertEqual(bookshelf.title, bookshelf.__str__())

    def test_create__when_invalid_title__expect_exception(self):
        user = self.create_valid_user()
        title = (Bookshelf.TITLE_MAX_LEN + 1) * 'a'
        bookshelf = Bookshelf.objects.create(title=title, user=user)

        with self.assertRaises(ValidationError) as context:
            bookshelf.full_clean()

        self.assertIsNotNone(context.exception)