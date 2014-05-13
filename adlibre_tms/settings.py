# Django settings for Adlibre TMS project.
import os
import posixpath
import sys

from . import __version__ as VERSION


PROJECT_PATH = os.path.abspath(os.path.split(__file__)[0])
sys.path.insert(0, os.path.join(PROJECT_PATH, 'apps'))
sys.path.insert(0, os.path.join(PROJECT_PATH, 'libraries'))

DEBUG = bool(os.environ.get('DEBUG', False))
TEMPLATE_DEBUG = DEBUG

ADMINS = ()
for admin in os.environ.get('ADMINS', '').split():
    ADMINS = ADMINS + (tuple(admin.split('/')),)

MANAGERS = ADMINS

from dj_database_url import config as db_config

DATABASES = {'default': db_config(default='sqlite://localhost//%s'
                                          % os.path.join(PROJECT_PATH, '..', 'db', 'tms.sqlite3'))}

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_PATH, '..', 'www', 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory that holds static files like app media.
# Example: "/home/media/media.lawrence.com/apps/"
STATIC_ROOT = os.path.join(PROJECT_PATH, '..',  'www', 'static')

# URL that handles the static files like app media.
# Example: "http://media.lawrence.com"
STATIC_URL = '/static/'

# Additional directories which hold static files
STATICFILES_DIRS = (
    ('', os.path.join(PROJECT_PATH, 'static')),
    ('', os.path.join(PROJECT_PATH, 'apps/tms/contrib/saasu/media')),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other finders..
)

STATICFILES_EXCLUDED_APPS = (
    'uni_form',
    )

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = posixpath.join(STATIC_URL, "admin/")

FIXTURE_DIRS = (
    os.path.join(PROJECT_PATH, 'fixtures'),
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',

    'adlibre_tms.context_processors.demo',

    'adlibre.core.context_processors.adlibre_settings',
    'django.core.context_processors.static',

    'reporting.context_processors.reports',
    )

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

    'pagination.middleware.PaginationMiddleware',
)

ROOT_URLCONF = 'adlibre_tms.urls'

TEMPLATE_DIRS = (
    'templates',
    os.path.join(PROJECT_PATH, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    #'django.contrib.sites',
    'django.contrib.admindocs',
    'django.contrib.admin',
    'django.contrib.sitemaps',
    #'django.contrib.flatpages',
    'django.contrib.staticfiles',

    # external
    'uni_form',
    'pagination',

    # local
    'accounts',
    'adlibre',
    'tms',
    'tms.contrib.saasu',
    'saasu_client',
    'reporting',
)

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'

SITE_NAME = 'Adlibre TMS'

PRODUCT_VERSION = VERSION  # Adlibre TMS Product Version
DEMO = True

PAGINATION_DEFAULT_PAGINATION = 15

# Cache settings
CACHE_BACKEND = 'locmem:///?timeout=300&max_entries=6000'

# Settings from .env (optional load)
TIME_ZONE = os.environ.setdefault("TIME_ZONE", "Australia/Sydney")
EMAIL_HOST = os.environ.setdefault("EMAIL_HOST", "localhost")
SAASU_FILE_UID = getattr(os.environ, 'SAASU_FILE_UID', 'XXXX')
SAASU_WSACCESS_KEY = getattr(os.environ, 'SAASU_WSACCESS_KEY', 'XXXXXXXXXXXXXXXXXXXXXXXXX')

# This will import the local_settings in our virtual_env subdir next to manage.py.
# But the preferred method is to use .env file and bureaucrat
try:
    from local_settings import *
except ImportError:
    pass

# debugging data to display if template rendered with errors (needs to be after local settings)
# NB this breaks the password change form. Issue #11
if DEBUG:
    TEMPLATE_STRING_IF_INVALID = 'error in template here'

# Loading SECRET_KEY from .env variable in case it is not already set somewhere else
try:
    if not SECRET_KEY:
        SECRET_KEY = os.environ['SECRET_KEY']
except NameError:
    print "Warning: settings.SECRET_KEY is nto set!"
    pass