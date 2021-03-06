from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from my_bookshelf.auth_app.models import Profile
from my_bookshelf.common.helpers import ValidUserAndProfileMixin
from my_bookshelf.web_app.models import Book, Bookshelf

UserModel = get_user_model()

class ProfileDetailsViewTest(ValidUserAndProfileMixin, TestCase):
    def test_get__when_profile_details_view__expect_correct_template_and_context(self):
        user, profile = self.create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)

        response = self.client.get(reverse('profile details', kwargs={'pk': profile.user_id}))

        books_count = response.context['books_count']
        bookshelves_count = response.context['bookshelves_count']
        profile_picture = response.context['profile_picture']

        self.assertEqual(0, books_count)
        self.assertEqual(0, bookshelves_count)
        self.assertIsNone(profile_picture)
        self.assertTemplateUsed(response, 'auth_app/profile_details.html')


class ProfileEditViewTest(ValidUserAndProfileMixin, TestCase):
    def test__when_valid_edits__should_change_profile_and_redirect_to_details(self):
        user, profile = self.create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)

        data = {
            'first_name': 'Test',
            'last_name': 'Testov',
        }

        response_get = self.client.get(reverse('profile edit', kwargs={'pk': profile.user_id}))
        response_post = self.client.post(reverse('profile edit', kwargs={'pk': profile.user_id}), data=data)
        edited_profile = Profile.objects.get(user_id=user.id)

        expected_full_name = f'{data["first_name"]} {data["last_name"]}'
        expected_url = reverse('profile details', kwargs={'pk': profile.user_id})

        self.assertEqual(expected_full_name, edited_profile.full_name)
        self.assertTemplateUsed(response_get, 'auth_app/profile_edit.html')
        self.assertRedirects(response_post, expected_url)

    def test__when_invalid_date_of_birth__expect_exception(self):
        user, profile = self.create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)

        data = {
            'date_of_birth': date.today() + timedelta(days=1),
        }

        profile.date_of_birth = data['date_of_birth']

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()

        self.assertIsNotNone(context.exception)


class ProfileDeleteViewTest(ValidUserAndProfileMixin, TestCase):
    def test__when_valid__should_use_correct_template_and_redirect_to_home(self):
        user, profile = self.create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)

        response_get = self.client.get(reverse('profile delete', kwargs={'pk': profile.user_id}))
        response_post = self.client.post(reverse('profile delete', kwargs={'pk': profile.user_id}))

        expected_url = reverse('home')
        self.assertTemplateUsed(response_get, 'auth_app/profile_delete.html')
        self.assertRedirects(response_post, expected_url)


class ProfilesListViewTest(ValidUserAndProfileMixin, TestCase):
    def test__when_one_profile__expect_context_to_contain_one_profile_and_correct_template(self):
        _, _ = self.create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)

        response = self.client.get(reverse('profiles list'))

        profiles = response.context['object_list']

        self.assertEqual(len(profiles), 1)
        self.assertTemplateUsed(response, 'auth_app/profiles_list.html')


class ProfileBooksListViewTest(ValidUserAndProfileMixin, TestCase):
    def test__when_two_books_of_user__expect_context_to_contain_two_books_and_correct_template(self):
        user, profile = self.create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)

        user2 = UserModel.objects.create_user(email='vaski@abv.bg', password='654321')

        books_to_create = (
            Book(title='Lord of the rings', author='J.R.R. Tolkien', genre='Fantasy', isbn='1111111111111', user=user),
            Book(title='Hobbit', author='J.R.R. Tolkien', genre='Fantasy', isbn='2222222222222', user=user),
            Book(title='The Silmarillion', author='J.R.R. Tolkien', genre='Fantasy', isbn='3333333333333', user=user2)
        )

        Book.objects.bulk_create(books_to_create)

        response = self.client.get(reverse('profile books', kwargs={'pk': profile.user_id}))
        books = response.context['object_list']

        self.assertTemplateUsed(response, 'auth_app/profile_books.html')
        self.assertEqual(len(books), 2)


class ProfileBookshelvesListViewTest(ValidUserAndProfileMixin, TestCase):
    def test__when_two_bookshelves_of_user__expect_context_to_contain_two_bookshelves_and_correct_template(self):
        user, profile = self.create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)

        user2 = UserModel.objects.create_user(email='vaski@abv.bg', password='654321')

        bookshelves_to_create = (
            Bookshelf(title='Fantasy', user=user),
            Bookshelf(title='Favourites', user=user),
            Bookshelf(title='Hobbies', user=user2)
        )

        Bookshelf.objects.bulk_create(bookshelves_to_create)

        response = self.client.get(reverse('profile bookshelves', kwargs={'pk': profile.user_id}))
        bookshelves = response.context['object_list']

        self.assertTemplateUsed(response, 'auth_app/profile_bookshelves.html')
        self.assertEqual(len(bookshelves), 2)
