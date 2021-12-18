"""
Django settings for ioee project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!5n6(ph#g120o!xm-fq-zcc&2#83m(b$4s!qr3ti@_2$^)e^^w'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'ioestudents.herokuapp.com', 'ioee.herokuapp.com']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'hotornot.apps.HotornotConfig',
    'fuse_attend.apps.FuseAttendConfig',
    'class.apps.ClassConfig',
    'person.apps.PersonConfig',
    'api.apps.ApiConfig',
    'code_share.apps.CodeShareConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',#For Static files
]

ROOT_URLCONF = 'ioee.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'ioee.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'hotornot': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'uegbcxiy',
        'USER': 'uegbcxiy',
        'PASSWORD': 'Z8RJEf1RcSNk029GD6JG--Mpmu6Fo9O2',
        'HOST': 'john.db.elephantsql.com',
        'PORT': '5432',
    },
    
    'fuse_attend': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'vysbznab',
        'USER': 'vysbznab',
        'PASSWORD': 'x-2Zh_jpzoWLqbolbcaejot5eVByKzqI',
        'HOST': 'john.db.elephantsql.com',
        'PORT': '5432',
    },
    'brainmap': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ltifidts',
        'USER': 'ltifidts',
        'PASSWORD': '7T1hDSqMGc2_iS1cPWwHbo4sZx2UbI_n',
        'HOST': 'john.db.elephantsql.com',
        'PORT': '5432',
    },
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = DEFAULT_FROM_EMAIL = EMAIL_HOST_USER = 'amaryesh123456@gmail.com'#'076bei001.aananda@sagarmatha.edu.np'
EMAIL_HOST_PASSWORD = 'ma ai banauchu9'#'6KBfDiNyJkUg3KP'
