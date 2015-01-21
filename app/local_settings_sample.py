DEBUG = True

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'zf*%dae-+$i^=+l05sbiibgnaxjd97rf!+d=o7i+-eo9+)i92g'

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = 'http://localhost/static/goms/'

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = '/var/www/html/static/goms/media'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = 'http://localhost/static/goms/media/'

GOOGLE_BOOKS_API_KEY = ''

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'goms',
        'USER': 'goms',
        'PASSWORD': 'goms',
        'HOST': 'localhost', # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '', # Set to empty string for default.
    }
}

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'pagination.middleware.PaginationMiddleware',
    'django_sorting.middleware.SortingMiddleware',
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# INSTALLED_APPS = (
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.sites',
#     'django.contrib.messages',
#     'django.contrib.staticfiles',

#     'south',
#     'mptt',
#     'linaro_django_pagination',
#     # 'django_sorting',
#     'webstack_django_sorting',
#     'rest_framework',
#     # If you're using Django 1.6.x or earlier
#     'debug_toolbar',
#     'froala_editor',

#     'users',
#     'inventory',
#     'account',
#     'core',
#     'ils',
#     'training',

#     'haystack',


#     'django.contrib.admin',
# )


