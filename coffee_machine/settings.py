"""
Django settings for the Coffee Making Machine project.

Database: MySQL (configured via environment variables, with sensible
local-dev defaults so the project also runs out of the box once a
matching MySQL database has been created in MySQL Workbench).
"""

import os
import dj_database_url
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# --------------------------------------------------------------------------
# Core / security
# --------------------------------------------------------------------------
# In production, set a real secret key via the DJANGO_SECRET_KEY env var
# and never commit it to source control.
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "dev-only-secret-key-change-this-before-deploying",
)

DEBUG = os.environ.get("DJANGO_DEBUG", "False") == "True"
ALLOWED_HOSTS = ["*"]


# --------------------------------------------------------------------------
# Applications
# --------------------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Local app
    "cafe",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "coffee_machine.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "cafe" / "templates"],
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

WSGI_APPLICATION = "coffee_machine.wsgi.application"

# --------------------------------------------------------------------------
# Database (MySQL / MySQL Workbench)
# --------------------------------------------------------------------------
# 1. Open MySQL Workbench and run the statements in schema.sql to create
#    the database (default name below: coffee_machine_db).
# 2. Either edit the defaults directly, or set these environment variables
#    before running manage.py: DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.environ.get("DB_NAME", "coffee_machine_db"),
        "USER": os.environ.get("DB_USER", "root"),
        "PASSWORD": os.environ.get("DB_PASSWORD", ""),
        "HOST": os.environ.get("DB_HOST", "127.0.0.1"),
        "PORT": os.environ.get("DB_PORT", "3306"),
        "OPTIONS": {
            "charset": "utf8mb4",
        },
    }
}

# --------------------------------------------------------------------------
# Password validation
# --------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --------------------------------------------------------------------------
# Auth redirects
# --------------------------------------------------------------------------
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "menu"
LOGOUT_REDIRECT_URL = "login"

# --------------------------------------------------------------------------
# Internationalization
# --------------------------------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

# --------------------------------------------------------------------------
# Static & media files
# --------------------------------------------------------------------------

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    BASE_DIR / "cafe" / "static",
]

STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
