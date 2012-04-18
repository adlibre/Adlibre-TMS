from saasu_client import settings

API_URL = 'https://secure.saasu.com/webservices/rest/r1/'

DEFAULT_GET_URL = '%s%s?wsaccesskey=%s&fileuid=%s' % (API_URL, '%s', settings.SAASU_WSACCESS_KEY, settings.SAASU_FILE_UID)
DEFAULT_POST_URL = '%s%s?wsaccesskey=%s&fileuid=%s' % (API_URL, '%s', settings.SAASU_WSACCESS_KEY, settings.SAASU_FILE_UID)

