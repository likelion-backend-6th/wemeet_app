"""
Django settings for meet project.

Generated by 'django-admin startproject' using Django 4.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from pathlib import Path
from celery.schedules import crontab

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

VERSION = "0.1.0"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-%1q)6f3d!g4i!siz-t9!)d@z=*5q_@5k%hz9jpt%2+$re+v+vk"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

LOCAL_IP = os.getenv("LOCAL_IP", "localhost")

# 모든 IP 허용
ALLOWED_HOSTS = [
    "*",
]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
]

# Application definition
INSTALLED_APPS += [
    "plan.apps.PlanConfig",
    "accountapp.apps.AccountappConfig",
]

# Third party apps
INSTALLED_APPS += [
    "rest_framework",
    "rest_framework_simplejwt",
    "drf_yasg",
    "bootstrap4",
    "social_django",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.kakao",
    "django_prometheus",
    "django_celery_beat",
    "django_celery_results",
    "django_redis",
]

MIDDLEWARE = [
    "django_prometheus.middleware.PrometheusBeforeMiddleware",
    "common.middleware.HealthcheckMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django_prometheus.middleware.PrometheusAfterMiddleware",
]

ROOT_URLCONF = "meet.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "meet.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django_prometheus.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB", "postgres"),
        "USER": os.getenv("POSTGRES_USER", "postgres"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "postgres"),
        "HOST": os.getenv("DB_HOST", "db"),
        "OPTIONS": {"options": "-c search_path=likelion,public"},
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "ko-KR"

TIME_ZONE = "Asia/Seoul"

USE_I18N = True

# timezone
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"
# STATICFILES_DIRS = [
#     BASE_DIR / "static",
# ]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "auth.USER"


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 15,
}

SIMPLE_JWT = {
    # 'ACCESS_TOKEN_LIFETIME': timedelta(hours=8),
    "UPDATE_LAST_LOGIN": True
}

SITE_ID = 1
SOCIALACCOUNT_LOGIN_ON_GET = True
ACCOUNT_LOGOUT_REDIRECT_URL = "accountapp:dashboard"
ACCOUNT_LOGOUT_ON_GET = True
LOGIN_REDIRECT_URL = "plan"
LOGIN_URL = "accountapp:login"
LOGOUT_URL = "accountapp:logged_out"
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "social_core.backends.kakao.KakaoOAuth2",
)

# Email
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "csy5501@gmail.com"
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "xxxx xxxx xxxx xxxx")

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")

CELERY_BROKER_URL = f"redis://{REDIS_HOST}:6379/0"
CELERY_RESULT_BACKEND = "django-db"
CELERY_TIMEZONE = "Asia/Seoul"
CELERY_BEAT_SCHEDULE = {
    "send_reminder_email_at_10am": {
        "task": "meet.plan.tasks.send_reminder_email_auto",
        "schedule": crontab(hour=6, minute=0),  # 오전 06시
    },
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{REDIS_HOST}:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}
