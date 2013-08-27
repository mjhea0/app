# Django settings for splintera project.

import os
PROJECT_DIR = os.path.dirname(__file__)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'storages',
    'gunicorn',
    'social_auth',
    'tastypie',
    'splintera',
    #'splintera_client',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #'splintera_client.tracer.MiddleWare',
)

# check if we are using a development or production machine
DEBUG=True
APP_KEY = '4c33df528be64bf49ab315f09789a9abe4c4c7f47c9fe74ac6afe44d60b61663'
INTERNAL_IPS = ('127.0.0.1',)
'''if os.environ.get('ENVIRONMENT')=='production':
    DEBUG = False
else:
    #development/staging machine
    DEBUG = True
#    TEMPLATE_DEBUG = DEBUG
    TEMPLATE_DEBUG = True
    INTERNAL_IPS = ('127.0.0.1',)
    INSTALLED_APPS += (
        'debug_toolbar',
    )
    MIDDLEWARE_CLASSES += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )
    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
    }'''

ADMINS = (
    ('Imran Akbar', 'imran@splintera.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'splintera_app',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'skunkwerk',
        'PASSWORD': 'motherlode721!',
        'HOST': 'dbase.akbars.net',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['splintera.herokuapp.com','splintera.com','www.splintera.com','127.0.0.1']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Los_Angeles'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_DIR, "static"),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'khmpun2#6kz-c40k#j%&4utwwy74=)p)sy@*)a)im7gq=f)zup'

DEFAULT_CONTENT_TYPE = 'text/html'

TEMPLATE_CONTEXT_PROCESSORS = (
  "django.core.context_processors.request",
  "django.contrib.auth.context_processors.auth",
  "social_auth.context_processors.social_auth_by_type_backends"
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

ROOT_URLCONF = 'splintera.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'splintera.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_DIR, "templates"),
)

EMAIL_HOST = 'email-smtp.us-east-1.amazonaws.com'
EMAIL_HOST_USER = 'AKIAJHNYR2Q5EGSQZEQA'
EMAIL_HOST_PASSWORD = 'AjhVlDRXj+utjvj+rx15sY3Ooak/wRSLY5ucuti7JiYo'
EMAIL_PORT = '587'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'dev@codanza.com'

AUTHENTICATION_BACKENDS = (
    'social_auth.backends.contrib.github.GithubBackend',
    'social_auth.backends.contrib.bitbucket.BitbucketBackend',
    'django.contrib.auth.backends.ModelBackend',# Needed to login by username in Django admin, regardless of `allauth`
)

SOCIAL_AUTH_ENABLED_BACKENDS = ('github','bitbucket')

#GOOGLE_OAUTH2_CLIENT_ID      = '178550587789.apps.googleusercontent.com'
#GOOGLE_OAUTH2_CLIENT_SECRET  = 'atk2csduMENTzQd0k9meHUmb'
GITHUB_APP_ID = '55f5050b42904002d207'
GITHUB_API_SECRET = 'aa00d836e835a5dbf7aa489040beae9d9121fc2d'
GITHUB_EXTENDED_PERMISSIONS = ['repo','user:email']
BITBUCKET_CONSUMER_KEY = 'RCmse2r7CFvfdLBzjx'
BITBUCKET_CONSUMER_SECRET = 'P2qDWsWr7cxGL5fTGgrvDr3gJGYBKszD'

LOGIN_URL          = '/accounts/login'
LOGIN_REDIRECT_URL = '/'
LOGIN_ERROR_URL    = '/accounts/login-error/'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/' # callback
SOCIAL_AUTH_COMPLETE_URL_NAME  = 'socialauth_complete'
SOCIAL_AUTH_ASSOCIATE_URL_NAME = 'socialauth_associate_complete'
SOCIAL_AUTH_ASSOCIATE_BY_MAIL = True
#SOCIAL_AUTH_NEW_USER_REDIRECT_URL = '/new-users-redirect-url/'

SOCIAL_AUTH_UID_LENGTH = 222
SOCIAL_AUTH_NONCE_SERVER_URL_LENGTH = 200
SOCIAL_AUTH_ASSOCIATION_SERVER_URL_LENGTH = 135
SOCIAL_AUTH_ASSOCIATION_HANDLE_LENGTH = 125

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters': {},
    'handlers': {
        'logfile': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': "splintera.log",
            'maxBytes': 50000,
            'backupCount': 2,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers':['logfile'],
            'level':'DEBUG',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['logfile'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'splintera': {
            'handlers': ['logfile'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
}

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
ACCOUNT_ACTIVATION_DAYS = 365 #

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_ACCESS_KEY_ID = 'AKIAIIQ7BWP5E7YJCDXA'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'codanza'