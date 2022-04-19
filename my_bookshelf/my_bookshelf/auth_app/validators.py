from datetime import datetime

from django.core.exceptions import ValidationError

VALIDATE_DATE_OF_BIRTH_EXCEPTION_MESSAGE = 'Date of birth can not be later than today.'


def validate_date_of_birth(value):
    if value > datetime.today().date():
        raise ValidationError(VALIDATE_DATE_OF_BIRTH_EXCEPTION_MESSAGE)
