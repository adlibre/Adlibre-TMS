from adlibre_tms import settings

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

##########

import os

PROJECT_PATH = os.path.abspath(os.path.split(__file__)[0])

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_PATH, '..', 'db', 'tms.sqlite'),
        }
}

print PROJECT_PATH