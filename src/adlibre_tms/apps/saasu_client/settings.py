from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

SAASU_WSACCESS_KEY = getattr(settings, 'SAASU_WSACCESS_KEY', None)
if SAASU_WSACCESS_KEY is None:
    raise ImproperlyConfigured('Please set your SAASU_WSACCESS_KEY setting.')

SAASU_FILE_UID = getattr(settings, 'SAASU_FILE_UID', None)
if SAASU_FILE_UID is None:
    raise ImproperlyConfigured('Please set your SAASU_FILE_UID setting.')
