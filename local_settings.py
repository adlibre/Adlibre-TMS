#### Database Location ../db/

import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.abspath(os.path.join(os.path.split(__file__)[0], '..', 'db', 'tms.sqlite')),
        }
}
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


