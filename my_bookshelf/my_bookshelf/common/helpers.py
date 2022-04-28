from django.contrib.auth import get_user_model

from my_bookshelf.auth_app.models import Profile

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
