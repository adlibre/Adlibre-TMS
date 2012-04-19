# Django settings for Adlibre TMS project.
import os
import posixpath
import sys


PROJECT_PATH = os.path.abspath(os.path.split(__file__)[0])
sys.path.insert(0, os.path.join(PROJECT_PATH, 'apps'))
sys.path.insert(0, os.path.join(PROJECT_PATH, 'libraries'))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    #('Example Admin', 'admin@example.com'),
)

MANAGERS = ADMINS

# tells django to serve media through django.views.static.serve.
SERVE_MEDIA = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_PATH, '..', 'db', 'tms.sqlite'),
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Australia/Sydney'

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
STATIC_ROOT = os.path.join(PROJECT_PATH, '..', 'www', 'static')

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
    'compressor.finders.CompressorFinder',
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

# Make this unique, and don't share it with anybody.
#SECRET_KEY = 'changeme' # set in local settings

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
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

    # Compresses CSS/JS files from media/static
    "compressor",

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

PRODUCT_VERSION='1.0' # Adlibre TMS Product Version
DEMO = True

PAGINATION_DEFAULT_PAGINATION = 15

# Saasu settings
#SAASU_FILE_UID = 'XXXX' # Define in local_settings
#SAASU_WSACCESS_KEY = 'XXXX-XXXX-XXXX-XXXX-XXXX-XXXX-XXXX-XXXX' # Define in local_settings

# Cache settings
CACHE_BACKEND = 'locmem:///?timeout=300&max_entries=6000'

# django-compressor specific settings
# Tells to compress urls from MEDIA folder because our static lies there...
#COMPRESS = True
#COMPRESS_URL = MEDIA_URL
#COMPRESS_ROOT = MEDIA_ROOT

# This will import the local_settings in our virtual_env subdir next to manage.py.
try:
    from local_settings import *
except ImportError:
    pass

# debugging data to display if template rendered with errors (needs to be after local settings)
# NB this breaks the password change form. Issue #11
if DEBUG:
    TEMPLATE_STRING_IF_INVALID = 'error in template here'