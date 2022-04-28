from django.test import TestCase

from django.contrib.auth import get_user_model
from django.urls import reverse

from my_bookshelf.auth_app.models import Profile
from my_bookshelf.web_app.models import Bookshelf

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


class ValidBookshelfDataMixin:
    VALID_BOOKSHELF_DATA = {
        'title': 'My favourite books',
    }


class BookshelfCreateViewTests(ValidUserAndProfileMixin, ValidBookshelfDataMixin, TestCase):
    def test_create__when_all_valid__should_create_and_redirect_to_profile_bookshelves(self):
        user, _ = self.create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.post(reverse('bookshelf add'), data=self.VALID_BOOKSHELF_DATA, user=user)

        bookshelf = Bookshelf.objects.get(user_id=user.id)

        expected_url = reverse('profile bookshelves', kwargs={'pk': bookshelf.user_id})
        self.assertIsNotNone(bookshelf)
        self.assertRedirects(response, expected_url)


class BookshelfEditViewTests(ValidUserAndProfileMixin, ValidBookshelfDataMixin, TestCase):
    def test_edit__when_all_valid__should_edit_and_redirect_to_bookshelf_details(self):
        user, profile = self.create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        bookshelf = Bookshelf.objects.create(**self.VALID_BOOKSHELF_DATA, user=user)

        self.VALID_BOOKSHELF_DATA['title'] = 'The best books in my library'

        response = self.client.post(reverse('bookshelf edit', kwargs={'pk': bookshelf.pk}),
                                    data=self.VALID_BOOKSHELF_DATA)
        edited_bookshelf = Bookshelf.objects.get(user_id=user.id)

        expected_title = self.VALID_BOOKSHELF_DATA['title']
        expected_url = reverse('bookshelf details', kwargs={'pk': bookshelf.pk})

        self.assertEqual(expected_title, edited_bookshelf.title)
        self.assertRedirects(response, expected_url)


class BookshelfDeleteViewTest(ValidUserAndProfileMixin, ValidBookshelfDataMixin, TestCase):
    def test__when_valid__should_use_correct_template_delete_book_and_redirect_to_profile_bookshelves(self):
        user, profile = self.create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        bookshelf = Bookshelf.objects.create(**self.VALID_BOOKSHELF_DATA, user=user)

        response_get = self.client.get(reverse('bookshelf delete', kwargs={'pk': bookshelf.pk}))
        response_post = self.client.post(reverse('bookshelf delete', kwargs={'pk': bookshelf.pk}))

        expected_url = reverse('profile bookshelves', kwargs={'pk': bookshelf.user_id})
        self.assertTemplateUsed(response_get, 'web_app/bookshelf_delete.html')
        self.assertRedirects(response_post, expected_url)


class BookshelfDetailsViewTest(ValidUserAndProfileMixin, ValidBookshelfDataMixin, TestCase):
    def test_get__when_bookshelf_details_view__expect_correct_template_and_context(self):
        user, profile = self.create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        bookshelf = Bookshelf.objects.create(**self.VALID_BOOKSHELF_DATA, user=user)

        response = self.client.get(reverse('bookshelf details', kwargs={'pk': bookshelf.pk}))

        owner = response.context['owner']
        books_list = response.context['books_list']

        self.assertEqual(owner, profile)
        self.assertEqual(0, len(books_list))
        self.assertTemplateUsed(response, 'web_app/bookshelf_details.html')


class BookshelvesListViewTest(ValidUserAndProfileMixin, ValidBookshelfDataMixin, TestCase):
    def test__when_one_bookshelf__expect_context_to_contain_one_bookshelf_and_correct_template(self):
        user, profile = self.create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        bookshelf = Bookshelf.objects.create(**self.VALID_BOOKSHELF_DATA, user=user)

        response = self.client.get(reverse('bookshelves list'))

        bookshelves = response.context['object_list']

        self.assertEqual(len(bookshelves), 1)
        self.assertTemplateUsed(response, 'web_app/bookshelves_list.html')
