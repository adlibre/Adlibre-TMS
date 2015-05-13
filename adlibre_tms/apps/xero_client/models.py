from datetime import date, timedelta

from django.db import models
from django.core.exceptions import ValidationError

from xero.exceptions import *

from tms.models import Project
from tms.models import Timesheet
from xero_client import XeroAuthManager

DEFAULT_CURRENCY = 'AUD'


def get_projects_tuple():
    projects = Project.objects.filter(is_billable=True)
    results = ()
    c = 0
    for p in projects:
        results += ((p.project_name, p.project_name), )
        c += 1
    print results
    return results


class XeroInvoice(models.Model):
    xero_sync = models.BooleanField(default=True, help_text='Upload this invoice to Xero')
    to = models.CharField(
        max_length=200,
        choices=get_projects_tuple(),
        help_text='Name of the company invoice is being issued to.'
    )
    invoice_date = models.DateField(default=date.today())
    default_due_date = date.today() + timedelta(days=5)
    due_date = models.DateField(default=default_due_date)
    summary = models.CharField(max_length=200, help_text='Leave blank for auto name', null=True, blank=True)
    items = models.ManyToManyField(Timesheet)

    def upload_to_xero(self, cleaned_data):
        summary = cleaned_data.get('summary')
        to = cleaned_data.get('to')
        invoice_date = cleaned_data.get('invoice_date')
        due_date = cleaned_data.get('due_date')
        project = Project.objects.filter(is_billable=True, project_name=to)[0]
        # TODO: related to tms.models failures
        #curency_code = project.currency.currency_code
        curency_code = None

        if not summary:
            summary = 'TMS generated: %s' % to

        manager = XeroAuthManager()
        xero = manager.xero
        invoice_data = {
            u'Type': u'ACCREC',
            u'Status': u'AUTHORISED',
            u'Contact': {
                u'Name': to
            },
            u'Date': invoice_date,
            u'DueDate': due_date,
            u'LineAmountTypes': u'Exclusive',
            u'Reference': summary,
            u'CurrencyCode': curency_code or DEFAULT_CURRENCY,
            u'LineItems': [],
        }

        items = cleaned_data.get('items')
        if items:  # can be none in case of sending invoice with no timesheets seleceted
            for item in items:
                invoice_data[u'LineItems'].append(
                    {
                        u'ItemCode': item.service_code.xero_item_id,
                        u'Description': u'%s %s' % (item.start_time, item),
                        u'Quantity': item.duration_minutes / 60,
                    }
                )

        try:
            xero.invoices.put(invoice_data)
        except (
            XeroBadRequest,
            XeroUnauthorized,
            XeroForbidden,
            XeroNotImplemented,
            XeroNotAvailable
        ), e:
            # Intercepting Xero API errors and output during validation with full API error message
            raise ValidationError('Xero invoice submit error: %s, %s' % (e, '\\'.join(e.errors)))


class XeroItemList(models.Model):
    items = None

    def __init__(self, *args, **kwargs):
        super(XeroItemList, self).__init__(*args, **kwargs)
        manager = XeroAuthManager()
        items = manager.xero.items.all()
        self.items = items


class XeroContactList(models.Model):
    items = None

    def __init__(self, *args, **kwargs):
        super(XeroContactList, self).__init__(*args, **kwargs)
        manager = XeroAuthManager()
        contacts = manager.xero.contacts.all()
        self.contacts = contacts

