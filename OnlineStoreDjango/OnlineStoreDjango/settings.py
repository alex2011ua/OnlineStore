"""
Django settings for OnlineStoreDjango project.

Generated by 'django-admin startproject' using Django 4.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from datetime import timedelta
from pathlib import Path
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = (
    os.getenv("DJANGO_SECRET_KEY")
)

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = int(os.getenv("DEBUG", 1))

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost").split()
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://main--lighthearted-cocada-0d2e37.netlify.app",
    "https://alex-online-store.fly.dev"
]
# CORS_ALLOW_ALL_ORIGINS = True

CSRF_TRUSTED_ORIGINS = (
    [os.getenv("CSRF_TRUSTED_ORIGINS")] if os.getenv("CSRF_TRUSTED_ORIGINS") else []
)
# Application definition

INSTALLED_APPS = [
    "modeltranslation",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    'whitenoise.runserver_nostatic',  # <-- Updated! whitenoise
    "django.contrib.staticfiles",
    #
    "rest_framework",
    "rest_framework_simplejwt",
    "django_extensions",
    "phonenumber_field",
    "drf_spectacular",
    "corsheaders",
    #  my app
    "my_apps.accounts",
    "my_apps.shop",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.security.SecurityMiddleware",
    'whitenoise.middleware.WhiteNoiseMiddleware',  # <-- Updated! whitenoise
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # "querycount.middleware.QueryCountMiddleware",
]

ROOT_URLCONF = "OnlineStoreDjango.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "OnlineStoreDjango.wsgi.application"
import dj_database_url

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql_psycopg2",
#         "NAME": os.getenv("POSTGRES_DB", "online_store_db"),
#         "USER": os.getenv("POSTGRES_USER", "AlexUA"),
#         "PASSWORD": os.getenv("POSTGRES_PASSWORD", "online_store"),
#         "HOST": os.getenv(
#             "DB_HOST",
#             "172.19.0.2",
#         ),
#         "PORT": str(os.getenv("PORT_DB", 5432)),
#     }
# }
DATABASES = {"default": dj_database_url.config(default=os.environ.get("DATABASE_URL"))}
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "my_apps.accounts.api_v1.authenticate.CustomAuthentication",
    ),
    "DEFAULT_PAGINATION_CLASS": "my_apps.shop.api_v1.paginators.StandardResultsSetPagination",
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.AllowAny",),
}


SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.getenv("GOOGLE_CLIENT_ID")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
]

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS: list = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "ua"

TIME_ZONE = "Europe/Madrid"

USE_I18N = True

USE_TZ = True

gettext = lambda s: s
LANGUAGES = (
    ("ua", gettext("Ukrainian")),
    ("en", gettext("English")),
)
MODELTRANSLATION_DEFAULT_LANGUAGE = "ua"
MODELTRANSLATION_PREPOPULATE_LANGUAGE = "en"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = "shop/media/"
STATIC = "shop/media/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "accounts.User"

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=5),
    # custom
    "AUTH_COOKIE": "access_token",  # cookie name
    "AUTH_COOKIE_DOMAIN": None,  # specifies domain for which the cookie will be sent
    "AUTH_COOKIE_SECURE": False,  # restricts the transmission of the cookie to only occur over secure (HTTPS) connections.
    "AUTH_COOKIE_HTTP_ONLY": True,  # prevents client-side js from accessing the cookie
    "AUTH_COOKIE_PATH": "/",  # URL path where cookie will be sent
    "AUTH_COOKIE_SAMESITE": "Lax",  # specifies whether the cookie should be sent in cross site requests
}
SPECTACULAR_SETTINGS = {
    "TITLE": "GiftHub API",  # название проекта
    "VERSION": "0.0.1",  # версия проекта
    "SERVE_INCLUDE_SCHEMA": False,  # исключить эндпоинт /schema
    "SWAGGER_UI_SETTINGS": {
        "filter": True,  # включить поиск по тегам
    },
    "COMPONENT_SPLIT_REQUEST": True,
}
QUERYCOUNT = {
    "THRESHOLDS": {"MEDIUM": 10, "HIGH": 20, "MIN_TIME_TO_LOG": 0, "MIN_QUERY_COUNT_TO_LOG": 1},
    "IGNORE_REQUEST_PATTERNS": [r"^/admin/"],
    "IGNORE_SQL_PATTERNS": [],
    "DISPLAY_DUPLICATES": True,
    "RESPONSE_HEADER": "X-DjangoQueryCount-Count",
}

# for sending emails
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        }
    },
    "handlers": {
        "console": {
            "formatter": "main_format",
            # "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
            "level": "WARNING",
        },
        "file": {
            "formatter": "main_format",
            # "filters": ["require_debug_true"],
            "class": "logging.FileHandler",
            "filename": "information.log",
            "level": "INFO",
        },
    },
    "formatters": {
        "main_format": {
            "format": "[{levelname}] {asctime}:{module}: {message}",
            "style": "{",
        }
    },
    "loggers": {
        # show SQL query
        # "django.db.backends": {
        #     "level": "DEBUG",
        #     "handlers": ["console"],
        # },
        "main": {
            "handlers": ["console", "file"],
            "level": "INFO",
        }
    },
}
