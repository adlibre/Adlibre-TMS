from xero import Xero
from xero.auth import PrivateCredentials

from xero_client.settings import XERO_CONSUMER_KEY
from xero_client.settings import XERO_PATH_CERTIFICATE


class XeroAuthManager(object):
    """Manager to work with basic xero API pyXero and TMS wide credentials"""

    def __init__(self):
        with open(XERO_PATH_CERTIFICATE) as keyfile:
            rsa_key = keyfile.read()
        credentials = PrivateCredentials(XERO_CONSUMER_KEY, rsa_key)
        self.credentials = credentials
        self.xero = Xero(credentials)