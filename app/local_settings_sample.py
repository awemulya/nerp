from .settings import *

SECRET_KEY = 'zf*%dae-+$i^=+l05sbiibgnaxjd97rf!+d=o7i+-eo9+)i92g'

DEBUG = True
MODELTRANSLATION_DEBUG = DEBUG

STATIC_ROOT = os.path.join(BASE_DIR, '..', 'static')
STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR, '..', 'media')
MEDIA_URL = '/media/'

INSTALLED_APPS += (
    # 'debug_toolbar',
)

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'awecounting',
#         'USER': 'awecounting',
#         'PASSWORD': 'password',
#         'HOST': '',
#         'PORT': '',
#         'ATOMIC_REQUESTS': True,
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}

ALLOWED_HOSTS = ['awecode.com', 'localhost', '127.0.0.1']

SITE_ID = 1

OPENEXCHANGERATES_APP_ID = '849ea94a3d574ad7a1191857c012cff3'
