from .settings import *

SECRET_KEY = 'zf*%dae-+$i^=+l05sbiibgnaxjd97rf!+d=o7i+-eo9+)i92g'

DEBUG = True

STATIC_ROOT = '/var/www/html/static/goms'
STATIC_URL = 'http://localhost/static/goms/'
STATIC_URL = '/static/'
MEDIA_ROOT = '/var/www/html/static/goms/media'
MEDIA_URL = 'http://localhost/static/goms/media/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'goms',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',  # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',  # Set to empty string for default.
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'TIMEOUT': 5,
    }
}

SITE_ID = 1

INSTALLED_APPS += (
    'debug_toolbar',
)
