from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

XERO_ERROR_MESSAGES = {
    'no_key': 'Please set your XERO_CONSUMER_KEY setting.',
    'no_secret': 'Please set your XERO_PATH_CERTIFICATE setting. Must be a path to your privatekey.pem',
}

XERO_CONSUMER_KEY = getattr(settings, 'XERO_CONSUMER_KEY', None)
if XERO_CONSUMER_KEY is None:
    raise ImproperlyConfigured(XERO_ERROR_MESSAGES['no_key'])

XERO_PATH_CERTIFICATE = getattr(settings, 'XERO_PATH_CERTIFICATE', None)
if XERO_PATH_CERTIFICATE is None:
    raise ImproperlyConfigured(XERO_ERROR_MESSAGES['no_secret'])

DEFAULT_INVOICE_PAYMENT_DAYS = 3