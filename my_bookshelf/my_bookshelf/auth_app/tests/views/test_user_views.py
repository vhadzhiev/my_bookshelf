from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

UserModel = get_user_model()


class UserLoginViewTest(TestCase):
    VALID_USER_CREDENTIALS = {
        'email': 'vaski@gmail.com',
        'password': '123456',
    }

    def test_login__when_valid_credentials__expect_login_and_correct_template(self):
        UserModel.objects.create_user(**self.VALID_USER_CREDENTIALS)
        login_result = self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get(reverse('login user'))
        self.assertTrue(login_result)
        self.assertTemplateUsed(response, 'auth_app/login_user.html')

    def test_login__when_invalid_email__expect_no_login(self):
        UserModel.objects.create_user(**self.VALID_USER_CREDENTIALS)
        login_result = self.client.login(email='vaski@abv.bg', password=self.VALID_USER_CREDENTIALS['password'])
        self.assertFalse(login_result)

    def test_login__when_invalid_password__expect_no_login(self):
        UserModel.objects.create_user(**self.VALID_USER_CREDENTIALS)
        login_result = self.client.login(email=self.VALID_USER_CREDENTIALS['email'], password='123457')
        self.assertFalse(login_result)

    def test_logout__expect_correct_template(self):
        UserModel.objects.create_user(**self.VALID_USER_CREDENTIALS)
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.logout()
        self.assertTemplateUsed(response, 'auth_app/logout_user.html')
