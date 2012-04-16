#### Database Location ../db/

import os
PROJECT_PATH = os.path.abspath(os.path.split(__file__)[0])

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.abspath(os.path.join(PROJECT_PATH, '..', 'db', 'tms.sqlite')),
        }
}

MEDIA_ROOT = os.path.abspath(os.path.join(PROJECT_PATH, '..', 'www', 'media'))
STATIC_ROOT = os.path.abspath(os.path.join(PROJECT_PATH, '..', 'www', 'static'))

STATICFILES_DIRS = ()

###

ADMINS = (
#('Admin', 'admin@example.com'),
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'change me'

# Saasu settings
SAASU_FILE_UID = 'XXXX'
SAASU_WSACCESS_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXX'

# specific timezone settings
TIME_ZONE = None

# Turn off demo
DEMO = False


