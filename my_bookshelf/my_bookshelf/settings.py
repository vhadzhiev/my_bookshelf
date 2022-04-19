import os
from pathlib import Path
import cloudinary
from django.urls import reverse_lazy

from my_bookshelf.utils import is_production, is_test

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', '')

DEBUG = os.getenv('DEBUG', 'False') == 'True'

APP_ENVIRONMENT = os.getenv('APP_ENVIRONMENT')

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(' ')

DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

THIRD_PARTY_APPS = (
    'crispy_forms',
)

PROJECT_APPS = (
    'my_bookshelf.auth_app',
    'my_bookshelf.web_app',
)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'my_bookshelf.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'my_bookshelf.wsgi.application'

DEFAULT_DATABASE_CONFIG = {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': os.getenv('DB_NAME', 'my_bookshelf_db'),
    'USER': os.getenv('DB_USER', 'postgres'),
    'PASSWORD': os.getenv('DB_PASSWORD', '123456'),
    'HOST': os.getenv('DB_HOST', '127.0.0.1'),
    'PORT': os.getenv('DB_PORT', '5432'),
}

DATABASES = {
    'default': DEFAULT_DATABASE_CONFIG,
}

DEFAULT_CACHE_CONFIG = {
    'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
}

if is_production():
    DEFAULT_CACHE_CONFIG = {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': os.getenv('REDIS_TO_GO_LOCATION'),
    }

CACHES = {
    'default': DEFAULT_CACHE_CONFIG,
}

AUTH_PASSWORD_VALIDATORS = []

if is_production():
    AUTH_PASSWORD_VALIDATORS.extend([
        {
            'NAME': 'django.contrib.auth_app.password_validation.UserAttributeSimilarityValidator',
        },
        {
            'NAME': 'django.contrib.auth_app.password_validation.MinimumLengthValidator',
        },
        {
            'NAME': 'django.contrib.auth_app.password_validation.CommonPasswordValidator',
        },
        {
            'NAME': 'django.contrib.auth_app.password_validation.NumericPasswordValidator',
        },
    ])

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    BASE_DIR / 'static',
)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGGING_LEVEL = 'DEBUG'

if is_production():
    LOGGING_LEVEL = 'INFO'
elif is_test():
    LOGGING_LEVEL = 'CRITICAL'

LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'level': LOGGING_LEVEL,
            'filters': [],
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': LOGGING_LEVEL,
            'handlers': ['console'],
        }
    }
}

cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME', None),
    api_key=os.getenv('CLOUDINARY_API_KEY', None),
    api_secret=os.getenv('CLOUDINARY_API_SECRET', None),
)

AUTH_USER_MODEL = 'auth_app.MyBookshelfUser'

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = BASE_DIR / 'sent_emails'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

LOGIN_URL = reverse_lazy('login user')

# TODO add cache to ListViews
# TODO add search bar
# TODO add sorting in ListViews
# TODO add logging
# TODO add 404 and others
