from datetime import date, datetime, timedelta

from django.db import models
from django.core.exceptions import ValidationError

from xero.exceptions import *

from tms.models import Project
from tms.models import Timesheet
from xero_client import XeroAuthManager


class XeroInvoice(models.Model):
    projects = Project.objects.filter(is_billable=True)
    PROJECTS = ()
    c = 0
    for p in projects:
        PROJECTS += ((p.project_name, p.project_name), )
        c += 1
    # TODO: make sure it works and simplify
    print PROJECTS

    xero_sync = models.BooleanField(default=True, help_text='Upload this invoice to Xero')
    to = models.CharField(
        max_length=200,
        choices=PROJECTS,
        help_text='Name of the company invoice is being issued to.'
    )
    invoice_date = models.DateField(default=date.today())
    default_due_date = date.today() + timedelta(days=5)
    due_date = models.DateField(default=default_due_date)
    summary = models.CharField(max_length=200, help_text='Leave blank for auto name', null=True, blank=True)
    items = models.ManyToManyField(Timesheet)

    def clean(self, *args, **kwargs):
        super(XeroInvoice, self).clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        super(XeroInvoice, self).save(*args, **kwargs)

    def upload_to_xero(self, cleaned_data):
        summary = cleaned_data.get('summary')
        to = cleaned_data.get('to')
        invoice_date = cleaned_data.get('invoice_date')
        due_date = cleaned_data.get('due_date')
        project = Project.objects.filter(is_billable=True, project_name=to)[0]

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
            u'CurrencyCode': 'AUD',  # TODO:
            u'LineItems': [],
        }

        items = cleaned_data.get('items')
        for item in items:
            invoice_data[u'LineItems'].append(
                {
                    u'Description': '%s %s' % (item.date_start, item),
                    u'Quantity': item.duration_minutes / 60,
                    u'UnitAmount': item.job.price,
                    u'AccountCode': u'200',
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



