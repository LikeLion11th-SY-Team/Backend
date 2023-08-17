"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 4.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os,json
from pathlib import Path
from datetime import timedelta
from django.core.exceptions import ImproperlyConfigured
import pymysql
import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env(
    env_file=os.path.join(BASE_DIR, '.env')
)

pymysql.install_as_MySQLdb()


SECRET_KEY = env('SECRET_KEY')
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/


DEBUG = True


# Application definition

INSTALLED_APPS = [

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'login',
    'users',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'posts',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.kakao',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ORIGIN_WHITELIST = ['http://127.0.0.1:3000' ,'http://localhost:3000','http://localhost:8000']
CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = { 
    'default': {
        'ENGINE' : 'django.db.backends.mysql',
        'HOST': env('HOST'),
        'PORT': env('PORT'),
        'NAME' : env('DB_NAME'),
        'USER': env('MYSQL_USER'),
        'PASSWORD': env('MYSQL_PASSWORD')
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#allauth 
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)
SITE_ID = 1

SOCIALACCOUNT_PROVIDERS = {
    'kakao': {
        'APP': {
            'client_id': 'dc6d77371b58fce528a75d2f7504577c',
            'secret': '',
            'key': '', 
        }
    }
}

SOCIALACCOUNT_LOGIN_ON_GET = True
LOGIN_REDIRECT_URL = 'main'  # 수정 필요
ACCOUNT_LOGOUT_REDIRECT_URL = 'index'  # 수정 필요
ACCOUNT_LOGOUT_ON_GET = True

ALLOWED_HOSTS = [
    'port-0-triptopper-f69b2mlhaa9b38.sel4.cloudtype.app',
    '127.0.0.1',
    'localhost',
    '13.125.121.158',
    'ec2-13-125-121-158.ap-northeast-2.compute.amazonaws.com',
    '.한걸음씩.o-r.kr',
    '.xn--369a718b4pbn1y.o-r.kr',
]


# 새로 추가
AUTH_USER_MODEL = 'users.User'
ACCOUNT_EMAIL_REQUIRED = False
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME' : timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME' : timedelta(days=7),
    'ROTATE_REFRESH_TOKENS' : False,
    'BLACKLIST_AFTER_ROTATION' : False,
    'UPDATE_LAST_LOGIN' : False,
}

# 메일을 호스트하는 서버
EMAIL_HOST = 'smtp.gmail.com'

# gmail과의 통신하는 포트
EMAIL_PORT = '587'

# 발신할 이메일
EMAIL_HOST_USER = env('SENDER_MAIL')

# 발신할 메일의 비밀번호
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
# TLS 보안 방법
EMAIL_USE_TLS = True

# 사이트와 관련한 자동응답을 받을 이메일 주소
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER