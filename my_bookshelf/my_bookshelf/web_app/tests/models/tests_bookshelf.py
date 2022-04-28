from django.core.exceptions import ValidationError
from django.test import TestCase

from my_bookshelf.common.helpers import ValidUserAndProfileMixin
from my_bookshelf.web_app.models import Bookshelf


class BookshelfTests(ValidUserAndProfileMixin, TestCase):
    def test_create__when_all_valid__should_create_bookshelf(self):
        user, _ = self.create_valid_user_and_profile()
        bookshelf = Bookshelf.objects.create(title='Favourites', user=user)
        self.assertIsNotNone(bookshelf)
        self.assertEqual(bookshelf.user_id, user.id)
        self.assertEqual(bookshelf.title, bookshelf.__str__())

    def test_create__when_invalid_title__expect_exception(self):
        user, _ = self.create_valid_user_and_profile()
        title = (Bookshelf.TITLE_MAX_LEN + 1) * 'a'
        bookshelf = Bookshelf.objects.create(title=title, user=user)

        with self.assertRaises(ValidationError) as context:
            bookshelf.full_clean()

        self.assertIsNotNone(context.exception)
