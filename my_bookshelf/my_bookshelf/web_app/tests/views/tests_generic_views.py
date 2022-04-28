from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

UserModel = get_user_model()


class ValidUserMixin:
    VALID_USER_CREDENTIALS = {
        'email': 'vaski@gmail.com',
        'password': '123456',
    }

    def create_valid_user(self):
        user = UserModel.objects.create_user(**self.VALID_USER_CREDENTIALS)
        return user


class HomeViewTests(ValidUserMixin, TestCase):
    def test__when_user_is_authenticated__should_redirect_to_dashboard(self):
        user = self.create_valid_user()
        self.client.login(**self.VALID_USER_CREDENTIALS)

        response = self.client.get(reverse('home'))

        expected_url = reverse('dashboard')
        self.assertRedirects(response, expected_url)
