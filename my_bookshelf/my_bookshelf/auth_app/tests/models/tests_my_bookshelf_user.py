from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

UserModel = get_user_model()


class UserModelTests(TestCase):
    VALID_USER_CREDENTIALS = {
        'email': 'vaski@gmail.com',
        'password': '123456',
    }

    def test_get__expect_correct_template(self):
        response = self.client.get(reverse('register user'))
        self.assertTemplateUsed(response, 'auth_app/register.html')

    def test_user_register__when_valid_email_and_password__should_register_user(self):
        user = UserModel(**self.VALID_USER_CREDENTIALS)
        user.save()
        self.assertIsNotNone(user.pk)
