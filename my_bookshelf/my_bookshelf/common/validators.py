from django.core.exceptions import ValidationError

IMAGE_MAX_FILE_SIZE_IN_MB = 10
VALIDATE_IMAGE_MAX_SIZE_EXCEPTION_MESSAGE = f'The image size exceeds the maximum allowed size of {IMAGE_MAX_FILE_SIZE_IN_MB} MB.'


def validate_image_max_size_in_mb(image):
    if image.size > IMAGE_MAX_FILE_SIZE_IN_MB * 1024 * 1024:
        raise ValidationError(VALIDATE_IMAGE_MAX_SIZE_EXCEPTION_MESSAGE)
