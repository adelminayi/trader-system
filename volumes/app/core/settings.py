"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 4.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import os
from pathlib import Path
from datetime import timedelta
from ast import literal_eval
from dotenv import load_dotenv


load_dotenv()

POSTGRES_DB         = os.getenv('POSTGRES_DB')
POSTGRES_USER       = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD   = os.getenv('POSTGRES_PASSWORD')
POSTGRES_HOST       = os.getenv('POSTGRES_HOST')
POSTGRES_PORT       = os.getenv('POSTGRES_PORT')

DJANGO_SECRET_KEY   = os.getenv('DJANGO_SECRET_KEY')
DJANGO_DEBUG        = os.getenv('DJANGO_DEBUG')
DJANGO_ALLOWED_HOSTS= os.getenv('DJANGO_ALLOWED_HOSTS')
CSRFORIGIN1         = os.getenv('CSRFORIGIN1')

EMAILHOSTUSER       = os.getenv('EMAILHOSTUSER')
EMAILHOSTPASSWORD    = os.getenv('EMAILHOSTPASSWORD')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = DJANGO_SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = [DJANGO_ALLOWED_HOSTS]
ALLOWED_HOSTS = ["apiv1.jirnal.ir",
                 "my.jirnal.ir",
                 "dev.panel.jirnal.ir",
                 "localhost",
                 "192.168.11.33"]
# CSRF_TRUSTED_ORIGINS = [CSRFORIGIN1]
CSRF_TRUSTED_ORIGINS = [
                 "http://localhost:3000",
                 "http://192.168.11.33:5100",
                 "https://apiv1.jirnal.ir"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # third-party apps
    'corsheaders',
    'django_crontab',
    'phonenumber_field',

    'rest_framework',
    'rest_framework.authtoken',
    
    'dj_rest_auth',
    'dj_rest_auth.registration',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.twitter',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',

    # project apps
    'profiles.apps.ProfilesConfig',
    'keysecrets.apps.KeysecretsConfig',
    'orders.apps.OrdersConfig',
    'trades.apps.TradesConfig',
    'userstrategies.apps.UserstrategiesConfig',
    'binanceWallet.apps.BinancewalletConfig',
    'balance.apps.BalanceConfig',
    'events.apps.EventsConfig',
    'emails.apps.EmailsConfig',
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
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

# WSGI_APPLICATION = 'core.wsgi.application'
ASGI_APPLICATION = 'core.asgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': POSTGRES_DB,
        'USER': POSTGRES_USER,
        'PASSWORD': POSTGRES_PASSWORD,
        'HOST': POSTGRES_HOST,
        'PORT': POSTGRES_PORT,
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }


# Password validation
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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR.parent / 'static'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR.parent / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# https://django-allauth.readthedocs.io/en/latest/configuration.html
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST    = 'smtp.gmail.com'
EMAIL_PORT    = 587
EMAIL_HOST_USER     = EMAILHOSTUSER
EMAIL_HOST_PASSWORD = EMAILHOSTPASSWORD

SITE_ID = 1

ACCOUNT_ADAPTER ='allauth.account.adapter.DefaultAccountAdapter'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_MAX_EMAIL_ADDRESSES = 3
ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = False
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'     ######## 'mandatory'/'optional'
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1
ACCOUNT_USERNAME_BLACKLIST =[]
ACCOUNT_ADAPTER = "emails.adapter.MyAdapter"

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# SOCIALACCOUNT_PROVIDERS = {
#     'google': {
#         'APP': {
#             'client_id': '',            ####
#             'secret': '',               ####
#             'key': ''                   ####
#         }
#     }
# }

# https://dj-rest-auth.readthedocs.io/en/latest/installation.html#
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'dj_rest_auth.jwt_auth.JWTCookieAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 5
}

REST_USE_JWT = True
JWT_AUTH_COOKIE = 'jirnal-auth'
JWT_AUTH_REFRESH_COOKIE = 'jirnal-refresh-token'
JWT_AUTH_SECURE = True    # send cookie over https
# JWT_AUTH_COOKIE_USE_CSRF = True
JWT_AUTH_COOKIE_USE_CSRF = False
# JWT_AUTH_COOKIE_ENFORCE_CSRF_ON_UNAUTHENTICATED = True
JWT_AUTH_COOKIE_ENFORCE_CSRF_ON_UNAUTHENTICATED = False
SIMPLE_JWT = {
'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
'REFRESH_TOKEN_LIFETIME': timedelta(days=15),
'ROTATE_REFRESH_TOKENS': False,
'BLACKLIST_AFTER_ROTATION': False
}

# https://pypi.org/project/django-phonenumber-field/
PHONENUMBER_DB_FORMAT = "NATIONAL"
PHONENUMBER_DEFAULT_FORMAT = "NATIONAL"
PHONENUMBER_DEFAULT_REGION = "IR"

# https://pypi.org/project/django-cors-headers/
# For demo purposes only. Use a white list in the real world.
CORS_ORIGIN_ALLOW_ALL = True


# https://pypi.org/project/django-crontab/
CRONJOBS = [
    ('*/5 * * * *', 'jobs.cronjobs.balances'),
    ('0 0 * * *', 'jobs.cronjobs.walletbalances', '>> /tmp/scheduled_job.log'),
    # ('0 0 * * *', 'jobs.cronjobs.onlyTestCron', '>> /tmp/onlytest.log'),
    ('*/5 * * * *', 'jobs.cronjobs.trades'),
    # ('*/5 * * * *', 'jobs.cronjobs.totaltrades'),
]