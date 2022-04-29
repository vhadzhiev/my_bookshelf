import os
from pathlib import Path
import cloudinary
from django.urls import reverse_lazy
from my_bookshelf.utils import is_production

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', 'sk')

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
    'HOST': os.getenv('DB_HOST', '127.0.0.1'),
    'PORT': os.getenv('DB_PORT', '5432'),
    'NAME': os.getenv('DB_NAME', 'my_bookshelf_db'),
    'USER': os.getenv('DB_USER', 'postgres'),
    'PASSWORD': os.getenv('DB_PASSWORD', '123456'),
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
        'LOCATION': os.getenv('REDISTOGO_URL'),
    }

CACHES = {
    'default': DEFAULT_CACHE_CONFIG,
}

AUTH_PASSWORD_VALIDATORS = []

if is_production():
    AUTH_PASSWORD_VALIDATORS.extend([
        {
            'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
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

LOGS_DIR = BASE_DIR / 'logs'

try:
    os.mkdir(LOGS_DIR)
except:
    pass

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{asctime} [{levelname}] {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'verbose',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': LOGS_DIR / 'Log.txt',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django.db.backends': {
            'level': 'INFO',
            'handlers': ['console'],
            'filters': [],
        },
    },
}

if is_production():
    LOGGING['handlers'] = {
        'coralogix': {
            'class': 'coralogix.handlers.CoralogixLogger',
            'level': 'WARNING',
            'formatter': 'verbose',
            'private_key': os.getenv('CORALOGIX_PRIVATE_KEY'),
            'app_name': os.getenv('CORALOGIX_APP_NAME'),
            'subsystem': os.getenv('CORALOGIX_SUBSYSTEM_NAME'),
        }
    }
    LOGGING['root'] = {
        'level': 'WARNING',
        'handlers': ['coralogix', ]
    }
    LOGGING['loggers'] = {
        'django.db.backends': {
            'level': 'WARNING',
            'handlers': ['coralogix', ]
        }
    }

cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET'),
)

AUTH_USER_MODEL = 'auth_app.MyBookshelfUser'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS')

CRISPY_TEMPLATE_PACK = 'bootstrap4'

LOGIN_URL = reverse_lazy('login user')

# TODO add send welcome email after successful registration
# TODO add sorting in ListViews
# TODO add selection of pagination in ListViews
# TODO add comments/review model
# TODO add book rating
# TODO translate site in BG (localization)
