from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from my_bookshelf.auth_app.models import Profile

UserModel = get_user_model()


class ProfileTests(TestCase):
    VALID_USER_CREDENTIALS = {
        'email': 'vaski@gmail.com',
        'password': '123456',
    }

    VALID_PROFILE_DATA = {
        'first_name': 'Vaski',
        'last_name': 'Vaski',
    }

    def test_register__when_all_valid__should_create_profile(self):
        user = UserModel.objects.create_user(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(user=user, **self.VALID_PROFILE_DATA)
        self.assertIsNotNone(profile)
        self.assertEqual(profile.user_id, user.id)
        self.assertEqual(self.VALID_PROFILE_DATA['first_name'], profile.first_name)
        self.assertEqual(self.VALID_PROFILE_DATA['last_name'], profile.last_name)

    def test_profile_full_name__when_valid__expect_correct_full_name(self):
        profile = Profile(**self.VALID_PROFILE_DATA)
        expected_fullname = f'{self.VALID_PROFILE_DATA["first_name"]} {self.VALID_PROFILE_DATA["last_name"]}'
        self.assertEqual(expected_fullname, profile.full_name)

    def test_profile_age__when_valid_date_of_birth__expect_correct_age(self):
        profile = Profile(**self.VALID_PROFILE_DATA)
        profile.date_of_birth = date(2010, 10, 10)
        today = date.today()
        expected_age = today.year - profile.date_of_birth.year - (
                (today.month, today.day) < (profile.date_of_birth.month, profile.date_of_birth.day))
        self.assertEqual(expected_age, profile.age)

    def test_profile_age__when_invalid_date_of_birth__expect_exception(self):
        profile = Profile(**self.VALID_PROFILE_DATA)
        today = date.today()
        profile.date_of_birth = today + timedelta(days=1)

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()

        self.assertIsNotNone(context.exception)
