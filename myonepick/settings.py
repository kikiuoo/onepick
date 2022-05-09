"""
Django settings for myonepick project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
    STATIC_DIR,
]
STATIC_ROOT = os.path.join(BASE_DIR, '.static_root')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-x0@zo^2*wmd9%%o*@*$r2l%4wh0ts+0iha7u1qlss!b*0*!5*$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['ksnpick.com', '127.0.0.1', 'localhost', '3.35.16.229', '172.31.33.129']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'picktalk.apps.PicktalkConfig',
    'user',
    'albapick',
    'apply',
    'audition',
    'banner',
    'company',
    'models',
    'profiles',

    #allauth
    #'allauth',
    #'allauth.account',
    #'allauth.socialaccount',

    #provider
    #'allauth.socialaccount.providers.kakao',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myonepick.urls'

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

WSGI_APPLICATION = 'myonepick.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': BASE_DIR / 'db.sqlite3',
#    }
#}

DATABASES = {
    'default' :{
        'ENGINE' : 'django.db.backends.mysql',
        'NAME' : 'onepick',
        'USER' : 'admin',
        'PASSWORD' : 'Q8iy-_ntkRs',
        'HOST' : 'picktalk.c5vctp8izdfi.ap-northeast-2.rds.amazonaws.com',
        'PORT' : '3306',
    }
}

# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

#TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

""" 
AWS_ACCESS_KEY_ID = 'AKIARCIZISC6QEB3E2EW'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'picktalk'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
            'CacheControl': 'max-age=86400',
            }
AWS_LOCATION = 'static'

STATICFILES_DIRS = [
                os.path.join(BASE_DIR, 'static'),
                '/usr/local/lib/python3.8/dist-packages/django/contrib/admin'
                ]
STATIC_URL = 'https://%s/%s/static/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
DEFAULT_FILE_STORAGE = 'picktalk.storage_backends.MediaStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field
"""


AWS_ACCESS_KEY_ID = 'AKIARCIZISC6QEB3E2EW'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'picktalk'

BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
    STATIC_DIR,
]
#STATIC_ROOT = os.path.join(BASE_DIR, '.static_root')
STATIC_ROOT = '/usr/local/lib/python3.8/dist-packages/django/contrib/admin'

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

"""
## 카카오 키들은 나중에 accounts.view에서 쓰일 예정
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

SITE_ID = 1
LOGIN_REDIRECT_URL = '/'
"""