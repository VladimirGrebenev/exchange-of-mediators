import os
from pathlib import Path

from django.urls import reverse_lazy
from dotenv import load_dotenv
from django.utils.translation import gettext_lazy as _

# Dirs
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR.parent / '.env')

SECRET_KEY = 'django-insecure-761_!a*22u-1r4c5l&xupo&@kpz)j5bs1xaq5mk#^xvg6_ta44'

# DEBUG = os.getenv('DJANGO_DEBUG', True)
DEBUG = True
ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    "daphne",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # other
    "django_bootstrap5",
    'debug_toolbar',
    "django_htmx",

    # mediators
    'user',
    'signing',
    'conflict',
    'dashboard',
    'reviews',
    'conference',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "django_htmx.middleware.HtmxMiddleware",
    "utils.middleware.AttachUserGroupsMiddleware",
    "utils.middleware.NotFoundMiddleware",
]

if DEBUG:
    ALLOWED_HOSTS = ['*']
    MIDDLEWARE += [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]

    INTERNAL_IPS = [
        '127.0.0.1',
        'localhost',
    ]

ROOT_URLCONF = 'mediators_website.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        "DIRS": [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # 'mediators_website.context_processors.random_mediators',
            ],
        },
    },
]

AUTH_USER_MODEL = "user.User"
AUTHENTICATION_BACKENDS = [
    "utils.backends.EmailBackend"
]

WSGI_APPLICATION = 'mediators_website.wsgi.application'

if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': str(BASE_DIR / 'db.sqlite3'),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": os.getenv("DJANGO_DB_ENGINE", "django.db.backends.postgresql"),
            "NAME": os.getenv("DJANGO_DB_NAME", "mediators"),
            "USER": os.getenv("DJANGO_DB_USER", "admin"),
            "PASSWORD": os.getenv("DJANGO_DB_PASSWORD", "password"),
            "HOST": os.getenv("DJANGO_DB_HOST", "localhost"),
            "PORT": int(os.getenv("DJANGO_DB_PORT", 5432)),
        }
    }

AUTH_PASSWORD_VALIDATORS = [
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
]

LANGUAGE_CODE = 'ru-ru'

LANGUAGES = [
    ('en', _('English')),
    ('ru', _('Russian')),
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),  # Путь к каталогу с файлами перевода
]

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

LOGIN_URL = reverse_lazy("signing:login")

LOGIN_REDIRECT_URL = reverse_lazy("dashboard:dashboard")

LOGOUT_REDIRECT_URL = reverse_lazy("signing:login")

EMAIL_CONFIRM_CODE_TTL_DAYS = 1
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = str(BASE_DIR / 'emails_test')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'

STATIC_DIR = BASE_DIR / 'static'
# STATIC_ROOT = os.path.join(BASE_DIR, '')

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATICFILES_DIRS = [
    STATIC_DIR,
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'django.log',  # Имя файла для записи логов
            'formatter': 'verbose',
        },
        'console': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['file', 'console'],
        'level': 'ERROR',  # Уровень логирования
    },
}

# Daphne
ASGI_APPLICATION = 'mediators_website.asgi.application'
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
        # "BACKEND": "channels_redis.core.RedisChannelLayer",
        # "CONFIG": {
        #     "hosts": [("127.0.0.1", 6380)],
        # },
    },
}
