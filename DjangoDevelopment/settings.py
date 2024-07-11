from inspect import currentframe
from pathlib import Path, os

from DjangoDevelopment.config.environ import env, APP_ENV
from backend.installedapp import INSTALLED_APPS as IMPORTED_BACKEND_APPS
from frontend.installedapp import INSTALLED_APPS as IMPORTED_FRONTEND_APPS
from DjangoDevelopment.config.dependencies import (
    INSTALLED_APPS as IMPORTED_DEPENDENCIES,
)

# Distributed Files start
from DjangoDevelopment.config.environ import *
from DjangoDevelopment.config.database import *
from DjangoDevelopment.config.storage import *
from DjangoDevelopment.config.logging import *
from DjangoDevelopment.config.email import *
from DjangoDevelopment.config.rest_framework import *
from DjangoDevelopment.config.others import *
from DjangoDevelopment.config.ckeditor import *

# Distributed Files end

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-(zy(t@6ieq+)@%z!li8$8uuf^$j+u3tl48p-ali7m+r)=zew($"

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
INSTALLED_APPS += IMPORTED_BACKEND_APPS
INSTALLED_APPS += IMPORTED_FRONTEND_APPS
INSTALLED_APPS += IMPORTED_DEPENDENCIES

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # 'myapp.middleware.ExceptionLoggingMiddleware'
]

ROOT_URLCONF = "DjangoDevelopment.urls"

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
                "webp_converter.context_processors.webp_support",
            ],
        },
    },
]
TEMPLATE_CONTEXT_PROCESSORS = ("django.core.context_processors.media",)
WSGI_APPLICATION = "DjangoDevelopment.wsgi.application"

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

STATIC_URL = "static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]
