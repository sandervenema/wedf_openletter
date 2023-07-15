"""
Django settings for wedf_openletter project.

Generated by 'django-admin startproject' using Django 1.9.dev20150804144604.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

import os

from django.utils.translation import gettext_lazy as _

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Temp console backend -- comment out both lines below during production if you
# want to use the SMTP backend -- which is the default
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
#EMAIL_BACKEND = 'django_sendmail_backend.backends.EmailBackend'

# E-mail SMTP settings
# Change this!
#EMAIL_HOST = 
#EMAIL_PORT =
#EMAIL_HOST_USER =
#EMAIL_HOST_PASSWORD =
#EMAIL_USE_TLS = True
#EMAIL_USE_SSL = True
#EMAIL_TIMEOUT =
# Optional: -- note Django doesn't do certificate checking, they're passed to
# the underlying SSL connection. For more details, check the docs on Python's
# ssl.wrap_socket().
#EMAIL_SSL_KEYFILE =
#EMAIL_SSL_CERTFILE =

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'PUT SECRET KEY HERE'

CSRF_COOKIE_SECURE = False

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
IAMWL_LOG_REQUESTS = False

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'hcaptcha',
    'petitions',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True

ROOT_URLCONF = 'wedf_openletter.urls'

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

WSGI_APPLICATION = 'wedf_openletter.wsgi.application'


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
	'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

if IAMWL_LOG_REQUESTS:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'logfile': {
                'class': 'logging.handlers.WatchedFileHandler',
                'filename': 'openletter-django.log',
            },
        },
        'loggers': {
            'django.request': {
                'handers': ['logfile'],
                'level': 'DEBUG',
                'propagate': True,
            },
            'django.template': {
                'handers': ['logfile'],
                'level': 'INFO',
                'propagate': True,
            },
            'django': {
                'handlers': ['logfile'],
                'level': 'DEBUG',
            },
            'petitions': {
                'handlers': ['logfile'],
                'level': 'DEBUG',
            },
        },
    }

# Password validation
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en-us'
LANGUAGES = [
    ('de', _("German")),
    ('en', _("English")),
    ('es', _("Spanish")),
    ('fr', _("French")),
    ('sv', _("Swedish")),
]
LOCALE_PATHS = (BASE_DIR + '/petitions/locale',)

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static/")

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'