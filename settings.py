from adlibre_tms.settings import *

# HACK: Here be magic and import voodoo...
# This file exists just to make manage.py happy when passing --settings= parameter.
# Put all your config in local_settings.py

## Overrides for our project layout in a standard deployment

# Database Location project_root/db/
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

###