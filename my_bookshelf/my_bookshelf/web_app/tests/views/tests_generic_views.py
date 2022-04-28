from django.test import TestCase
from django.urls import reverse

from my_bookshelf.common.helpers import ValidUserAndProfileMixin


class HomeViewTests(ValidUserAndProfileMixin, TestCase):
    def test__when_user_is_authenticated__should_redirect_to_dashboard(self):
        user, _ = self.create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)

        response = self.client.get(reverse('home'))

        expected_url = reverse('dashboard')
        self.assertRedirects(response, expected_url)
