from django.core.exceptions import ValidationError
from django.test import TestCase

from my_bookshelf.common.helpers import ValidUserAndProfileMixin
from my_bookshelf.web_app.models import Book


class BookTests(ValidUserAndProfileMixin, TestCase):
    VALID_BOOK_DATA = {
        'title': 'Lord of the rings',
        'author': 'J.R.R. Tolkien',
        'genre': 'Fantasy',
        'isbn': '1111111111111',
    }

    def test_create__when_all_valid__should_create_book(self):
        user, _ = self.create_valid_user_and_profile()
        book = Book.objects.create(**self.VALID_BOOK_DATA, user=user)
        self.assertIsNotNone(book)
        self.assertEqual(book.user_id, user.id)
        self.assertEqual(self.VALID_BOOK_DATA['title'], book.__str__())
        self.assertEqual(self.VALID_BOOK_DATA['title'], book.title)
        self.assertEqual(self.VALID_BOOK_DATA['author'], book.author)
        self.assertEqual(self.VALID_BOOK_DATA['genre'], book.genre)
        self.assertEqual(self.VALID_BOOK_DATA['isbn'], book.isbn)

    def test_create__when_invalid_title__expect_exception(self):
        user, _ = self.create_valid_user_and_profile()
        self.VALID_BOOK_DATA['title'] = (Book.TITLE_MAX_LEN + 1) * 'a'
        book = Book(**self.VALID_BOOK_DATA, user=user)

        with self.assertRaises(ValidationError) as context:
            book.full_clean()

        self.assertIsNotNone(context.exception)

    def test_create__when_invalid_author__expect_exception(self):
        user, _ = self.create_valid_user_and_profile()
        self.VALID_BOOK_DATA['author'] = (Book.AUTHOR_MAX_LEN + 1) * 'a'
        book = Book(**self.VALID_BOOK_DATA, user=user)

        with self.assertRaises(ValidationError) as context:
            book.full_clean()

        self.assertIsNotNone(context.exception)

    def test_create__when_longer_isbn__expect_exception(self):
        user, _ = self.create_valid_user_and_profile()
        self.VALID_BOOK_DATA['isbn'] = (Book.ISBN_MAX_LEN + 1) * '1'
        book = Book(**self.VALID_BOOK_DATA, user=user)

        with self.assertRaises(ValidationError) as context:
            book.full_clean()

        self.assertIsNotNone(context.exception)

    def test_create__when_isbn_contains_different_symbol_than_digit__expect_exception(self):
        user, _ = self.create_valid_user_and_profile()
        self.VALID_BOOK_DATA['isbn'] = '111111111111a'
        book = Book(**self.VALID_BOOK_DATA, user=user)

        with self.assertRaises(ValidationError) as context:
            book.full_clean()

        self.assertIsNotNone(context.exception)
