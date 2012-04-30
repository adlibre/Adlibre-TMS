"""
Settings file for when we install using pip in non development scenario
Contains overrides for our project layout in a standard deployment.
"""

from adlibre_tms.settings import * # Import global settings

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

# This will import the local_settings in our virtual_env subdir next to manage.py.
try:
    from local_settings import *
except ImportError:
    pass