import datetime

from django.db import models
from xero import Xero
from xero.auth import PrivateCredentials

from xero_client.settings import XERO_CONSUMER_KEY
from xero_client.settings import XERO_PATH_CERTIFICATE


class XeroInvoice(models.Model):
    to = models.CharField(max_length=200, help_text='Name of the company invoice is being issued to.')
    date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    invoice_no = models.CharField(max_length=10)
    reference = models.CharField(max_length=200, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Uploading before actual model instance saving to DB
        manager = XeroAuthManager()
        xero = manager.xero
        xero.invoices.put({
            u'Status': u'DRAFT',
            u'Total': u'264.00',
            u'CurrencyRate': u'1.000000',
            u'Reference': u'sdfghsfgh',
            u'Type': u'ACCREC',
            u'CurrencyCode': u'AUD',
            u'AmountPaid': u'0.00',
            u'TotalTax': u'24.00',
            u'Contact': {
                u'Name': u'Test One'
            },
            u'AmountDue': u'264.00',
            u'Date': datetime.date(2014, 7, 24),
            u'LineAmountTypes': u'Exclusive',
            u'LineItems': {
                u'LineItem': {
                    u'AccountCode': u'200',
                    u'TaxAmount': u'24.00',
                    u'Description': u'fgshfsdh',
                    u'UnitAmount': u'24.00',
                    u'TaxType': u'OUTPUT',
                    u'ItemCode': u'sfghfshg',
                    u'LineAmount': u'240.00',
                    u'Quantity': u'10.0000'
                }
            },
            u'SubTotal': u'240.00',
            u'DueDate': datetime.date(2014, 7, 24)
        })


        super(XeroInvoice, self).save(*args, **kwargs)



class XeroAuthManager(object):
    """Manager to work with basic xero API pyXero and TMS wide credentials"""

    def __init__(self):
        print XERO_PATH_CERTIFICATE
        with open(XERO_PATH_CERTIFICATE) as keyfile:
            rsa_key = keyfile.read()
        credentials = PrivateCredentials(XERO_CONSUMER_KEY, rsa_key)
        self.credentials = credentials
        self.xero = Xero(credentials)