from unittest import TestCase

from django.core.exceptions import ValidationError

from my_bookshelf.common.validators import validate_image_max_size_in_mb, IMAGE_MAX_FILE_SIZE_IN_MB


class FakeFile:
    size = (IMAGE_MAX_FILE_SIZE_IN_MB + 0.000001) * 1024 * 1024


class FakeImage:
    file = FakeFile()


class TestValidateImageMaxSizeInMb(TestCase):
    def test__when_file_is_bigger__expect_exception(self):
        image = FakeImage()
        validator = validate_image_max_size_in_mb

        with self.assertRaises(ValidationError) as context:
            validator(image.file)

        self.assertIsNotNone(context.exception)
