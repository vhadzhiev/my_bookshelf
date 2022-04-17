from django.core.exceptions import ValidationError

VALIDATE_ONLY_DIGITS_EXCEPTION_MESSAGE = 'Ensure this value contains only numbers.'
VALIDATE_CORRECT_LENGTH_EXCEPTION_MESSAGE = 'Ensure this value has exactly 10 or 13 numbers.'


def validate_only_digits(value):
    for ch in value:
        if not ch.isdigit():
            raise ValidationError(VALIDATE_ONLY_DIGITS_EXCEPTION_MESSAGE)


def validate_correct_length(value):
    if len(value) != 10 and len(value) != 13:
        raise ValidationError(VALIDATE_CORRECT_LENGTH_EXCEPTION_MESSAGE)

# TODO add max file size validator
