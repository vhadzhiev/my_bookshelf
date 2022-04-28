from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from my_bookshelf.auth_app.models import Profile
from my_bookshelf.web_app.models import Book

UserModel = get_user_model()


class ValidUserAndProfileMixin:
    VALID_USER_CREDENTIALS = {
        'email': 'vaski@gmail.com',
        'password': '123456',
    }

    VALID_PROFILE_DATA = {
        'first_name': 'Vaski',
        'last_name': 'Vaski',
    }

    def create_valid_user_and_profile(self):
        user = UserModel.objects.create_user(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(**self.VALID_PROFILE_DATA, user=user)
        return user, profile


class ValidBookDataMixin:
    VALID_BOOK_DATA = {
        'title': 'Lord of the rings',
        'author': 'J.R.R. Tolkien',
        'genre': 'Fantasy',
        'isbn': '1111111111111',
    }


class BookCreateViewTests(ValidUserAndProfileMixin, ValidBookDataMixin, TestCase):
    def test_create__when_all_valid__should_create_and_redirect_to_profile_books(self):
        user, _ = self.create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.post(reverse('book add'), data=self.VALID_BOOK_DATA, user=user)

        book = Book.objects.get(user_id=user.id)

        expected_url = reverse('profile books', kwargs={'pk': book.user_id})
        self.assertIsNotNone(book)
        self.assertRedirects(response, expected_url)


class BookEditViewTests(ValidUserAndProfileMixin, ValidBookDataMixin, TestCase):
    def test_edit__when_all_valid__should_edit_and_redirect_to_book_details(self):
        user, profile = self.create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        book = Book.objects.create(**self.VALID_BOOK_DATA, user=user)

        self.VALID_BOOK_DATA['title'] = 'Hobbit'

        response = self.client.post(reverse('book edit', kwargs={'pk': book.pk}), data=self.VALID_BOOK_DATA)
        edited_book = Book.objects.get(user_id=user.id)

        expected_title = self.VALID_BOOK_DATA['title']
        expected_url = reverse('book details', kwargs={'pk': book.pk})

        self.assertEqual(expected_title, edited_book.title)
        self.assertRedirects(response, expected_url)


class BookDeleteViewTest(ValidUserAndProfileMixin, ValidBookDataMixin, TestCase):
    def test__when_valid__should_use_correct_template_delete_book_and_redirect_to_profile_books(self):
        user, profile = self.create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        book = Book.objects.create(**self.VALID_BOOK_DATA, user=user)

        response_get = self.client.get(reverse('book delete', kwargs={'pk': book.pk}))
        response_post = self.client.post(reverse('book delete', kwargs={'pk': book.pk}))

        expected_url = reverse('profile books', kwargs={'pk': book.user_id})
        self.assertTemplateUsed(response_get, 'web_app/book_delete.html')
        self.assertRedirects(response_post, expected_url)


class BookDetailsViewTest(ValidUserAndProfileMixin, ValidBookDataMixin, TestCase):
    def test_get__when_profile_view__expect_correct_template_and_context(self):
        user, profile = self.create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        book = Book.objects.create(**self.VALID_BOOK_DATA, user=user)

        response = self.client.get(reverse('book details', kwargs={'pk': book.pk}))

        owner = response.context['owner']
        book_cover = response.context['book_cover']

        self.assertEqual(owner, profile)
        self.assertIsNone(book_cover)
        self.assertTemplateUsed(response, 'web_app/book_details.html')


class BooksListViewTest(ValidUserAndProfileMixin, ValidBookDataMixin, TestCase):
    def test__when_one_book__expect_context_to_contain_one_book_and_correct_template(self):
        user, profile = self.create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        book = Book.objects.create(**self.VALID_BOOK_DATA, user=user)

        response = self.client.get(reverse('books list'))

        books = response.context['object_list']

        self.assertEqual(len(books), 1)
        self.assertTemplateUsed(response, 'web_app/books_list.html')
