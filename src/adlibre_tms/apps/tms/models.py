from django.db import models
from django.db.models.query import QuerySet
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
import datetime

from tms.managers import *

from saasu_client.models import *

__all__ = ['Employee', 'Project', 'Customer', 'Service', 'Job',
           'Timesheet', 'ExpenseType', 'PaymentMethod', 'Currency', 'Expense']


SAASU_ERRORS_CONSTANT = {
    'saasu_customer': "Timesheet has no specified Customer > SAASU item UID",
    'saasu_service': "Timesheet has no specified Service > SAASU item UID",
    'saasu_exp_type': "Timesheet has no specified Expense Type > SAASU item UID",
    'saasu_contact': "Expense has no specified Customer > SAASU item UID",
    'saasu_account': "Expense has no specified Account > SAASU item UID",
}


class Employee(models.Model):

    user = models.OneToOneField(User)

    class Meta:
        pass
    
    def __unicode__(self):
        return self.user.username


class Project(models.Model):

    project_name = models.CharField(max_length=64, unique=True)
    project_code = models.CharField(max_length=32, unique=True)
    is_billable = models.BooleanField(default=True)

    class Meta:
        pass

    def __unicode__(self):
        return self.project_code   


class Customer(models.Model):
    """ Customer or client """

    customer_name = models.CharField(max_length=64, unique=True)
    customer_code = models.CharField(max_length=32, unique=True)
    is_billable = models.BooleanField(default=True)    

    # Link with SAASU contacts
    saasu_contact_uid = models.CharField(max_length=32, blank=True)

    class Meta:
        pass
    
    def __unicode__(self):
        return self.customer_code


class Service(models.Model):

    service_name = models.CharField(max_length=64, unique=True)
    service_code = models.CharField(max_length=32, unique=True)
    
    is_billable = models.BooleanField(default=True,
        help_text=_("This means that the timesheets should be charged to the client."))

    # Link with SAASU items
    saasu_item_uid = models.CharField(max_length=32, blank=True)

    class Meta:
        pass

    def __unicode__(self):
        return self.service_code


class Job(models.Model):
    """ Defines which customer/service/project combos are available. """
    
    customer = models.ForeignKey(Customer)
    service = models.ForeignKey(Service)
    project = models.ForeignKey(Project)

    is_active = models.BooleanField(default=True,
        help_text=_("This  means that current job is available for recording timesheet entries against it. (i.e. is visible in dropdown list)."))

    # For internal use

    # for calculating how far back to allow inactive jobs to be used in old timesheet entries.
    timestamp  = models.DateTimeField(auto_now=True) 

    class Meta:
        pass

    def __unicode__(self):
        return '%s %s %s' % (self.customer, self.service, self.project)
        
    def is_billable(self):
        "Return true if project is billable, service is billable and customer is billable."
        return self.project.is_billable and self.service.is_billable and self.customer.is_billable


class Timesheet(models.Model):

    employee = models.ForeignKey(Employee)
    job = models.ForeignKey(Job)   

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    # or could have a relational 'status' and 'open/closed' field.
    comment = models.CharField(max_length=255)

    is_submitted = models.BooleanField(default=False,
        help_text=_("This means that the consultant has finished editing and has submitted the timesheet for processing."))
    is_billed = models.BooleanField(default=False,
        help_text=_("This means that the client has been billed for the recorded in this timesheet entry."))

    # For internal use

    timestamp = models.DateTimeField(auto_now=True)

    # Set custom model manager
    objects = TimesheetManager()

    class Meta:
        ordering = ('start_time',)

    def __unicode__(self):
        return unicode(self.comment)

    class QuerySet(QuerySet):
        def get_total_minutes(self):
            """ Count total minutes for a given queryset """
            minutes = 0
            for t in self:
                minutes += t.duration_minutes
            return minutes

        def get_total_charge_minutes(self):
            """ Count total charged minutes for a given queryset """
            minutes = 0
            for t in self:
                if t.is_billable:
                    minutes += t.duration_minutes
            return minutes

        def get_total_days(self):
            """ Count total days for a given queryset """
            return self.get_total_minutes() / 60.0

        def get_total_charge_days(self):
            """ Count total charged days for a given queryset """
            return self.get_total_charge_minutes() / 60.0

        def saasu_export(self):
            date_now = datetime.datetime.now()
            t_dates = {}
            sorted_timesheets = {}
            row_exported = 0
            # grouping timesheets by SAASU contacts uid and extracting their dates to list
            for timesheet in self:
                uid = timesheet.job.customer.saasu_contact_uid
                if uid == '':
                    return SAASU_ERRORS_CONSTANT['saasu_customer']
                if not uid in sorted_timesheets.keys():
                    sorted_timesheets[uid]=[]
                    t_dates[uid]=[]
                sorted_timesheets[uid].append(timesheet)
                t_dates[uid].append(timesheet.start_time)
            for key in sorted_timesheets.keys():
                # creating invoice using first invoice as an example
                t = sorted_timesheets[key][0]

                # sorting dates to get first and last for every invoice
                invoice_min_date = datetime.datetime.max
                invoice_max_date = datetime.datetime.min
                for timesheet_date in t_dates[key]:
                    if invoice_min_date > timesheet_date:
                        invoice_min_date = timesheet_date
                    if invoice_max_date < timesheet_date:
                        invoice_max_date = timesheet_date
                if t.job.customer.saasu_contact_uid:
                    # Check if contact exists
                    contact = Contact.objects.get(uid=t.job.customer.saasu_contact_uid)
                    # Create new ItemInvoice object:
                    invoice_summary = unicode(t.job) + u' (' + \
                                      unicode(invoice_min_date.strftime('%Y/%m/%d')) + \
                                      u' - ' + unicode(invoice_max_date.strftime('%Y/%m/%d')) + u')'
                    invoice = ItemInvoice.objects.create(
                            contactUid=contact.uid,
                            date=date_now.strftime('%Y-%m-%d'),
                            summary=invoice_summary
                        )
                    # append lots of timesheets to item
                    for item_entry in sorted_timesheets[key]:
                        if item_entry.job.service.saasu_item_uid:
                            # Check is inventory item exists
                            item = InventoryItem.objects.get(uid=item_entry.job.service.saasu_item_uid)
                            # Gathering data for item
                            iedd = datetime.date(item_entry.end_time.year, item_entry.end_time.month, item_entry.end_time.day)
                            ie_description = unicode(iedd.strftime('%d/%m/%Y')) + ' ' + item_entry.comment
                            t_quantity = item_entry.end_time-item_entry.start_time
                            t_hours = round((t_quantity.seconds / 60.00 / 60.00 + t_quantity.days * 24), 2)
                            # Create new item for ItemInoice object
                            invoice_item = ItemInvoiceItem.objects.create(quantity=t_hours, inventoryItemUid=item.uid, description=ie_description,
                                                                          unitPriceInclTax=item.sellingPrice, taxCode='G1')
                            # Append to a list of items
                            invoice.invoiceItems.append(invoice_item)
                            row_exported += 1
                            # marking as billed after successful export
                            item_entry.is_billed = True
                            item_entry.save()
                        else:
                            return SAASU_ERRORS_CONSTANT['saasu_service']
                    # Save invoice
                    invoice.save()
                else:
                    return SAASU_ERRORS_CONSTANT['saasu_customer']
            return row_exported

    def _get_duration_seconds(self):
        """ Return duration in seconds. Duration = end_time - start_time """
        val = self.end_time - self.start_time
        return val.seconds + (86400 * val.days)

    duration_seconds = property(_get_duration_seconds)
    
    def _get_duration_minutes(self):
        """ Return duration in minutes. Duration = end_time - start_time """
        return self.duration_seconds / 60.0

    duration_minutes = property(_get_duration_minutes)

    def _get_duration_days(self):
        """ Return duration in dats. Duration = end_time - start_time """
        return self.duration_seconds / 3600.0

    duration_days = property(_get_duration_days)

    def _get_is_billable(self):
        return self.job.is_billable()

    is_billable = property(_get_is_billable)

    def _get_customer_code(self):
        return self.job.customer

    customer_code = property(_get_customer_code)

    def _get_service_code(self):
        return self.job.service

    service_code = property(_get_service_code)


class ExpenseType(models.Model):

    expense_type_name = models.CharField(max_length=64, unique=True)
    expense_type_code = models.CharField(max_length=32, unique=True)

    # Link with SAASU account
    saasu_account_uid = models.CharField(max_length=32, blank=True)

    class Meta:
        pass

    def __unicode__(self):
        return self.expense_type_code


class PaymentMethod(models.Model):

    payment_method_name = models.CharField(max_length=64, unique=True)
    payment_method_code = models.CharField(max_length=32, unique=True)

    class Meta:
        pass

    def __unicode__(self):
        return self.payment_method_code


class Currency(models.Model):

    currency_name = models.CharField(max_length=64, unique=True)

    currency_code = models.CharField(max_length=32, unique=True)
    currency_symbol = models.CharField(max_length=1)

    class Meta:
        verbose_name_plural = 'currencies'

    def __unicode__(self):
        return self.currency_code


class Expense(models.Model):

    employee = models.ForeignKey(Employee)
    customer = models.ForeignKey(Customer)
    expense_type = models.ForeignKey(ExpenseType) # (these should be linked to saasu accounts)
    payment_method = models.ForeignKey(PaymentMethod)
    currency = models.ForeignKey(Currency)

    is_receipted = models.BooleanField(default=True) # invoice / documentation exists
    is_submitted = models.BooleanField(default=False) # eg completed
    is_billed = models.BooleanField(default=False) # eg is processed
    is_taxable = models.BooleanField(default=True) # eg is taxed / gst applies

    expense_amount = models.DecimalField(max_digits=10, decimal_places=2) # amount in currency expense receipted in.
    local_amount = models.DecimalField(_("Local Currency Amount"), max_digits=10, decimal_places=2) # amount  converted to local currency / claimed currency, inc tax.
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2) # amount of tax.

    # tax_rate # this should be a method
    # exchange_rate # this should be a method,

    comment = models.CharField(max_length=255)

    expense_date = models.DateField()
    claim_date = models.DateField()
    
    # For internal use

    timestamp = models.DateTimeField(auto_now=True)

    # Set custome model manager

    objects = ExpenseManager()

    class Meta:
        pass

    def __unicode__(self):
        return '%s %s %s %s' % (self.employee, self.customer, self.expense_type, self.expense_amount)

    class QuerySet(QuerySet):
        def get_total_amount(self):
            """ Count total expenses for a given queryset """
            amount = 0
            for ex in self:
                amount += ex.total_amount
            return amount

        def get_total_local_amount(self):
            """ Count total local expenses for a given queryset """
            amount = 0
            for ex in self:
                amount += ex.local_amount
            return amount

        def saasu_export(self):
            row_exported = 0
            for e in self:
                if e.customer.saasu_contact_uid:
                    # Check if contact exists
                    contact = Contact.objects.get(uid=e.customer.saasu_contact_uid)
                    # Create new ServicePurchase object
                    # converting date first
                    purchase_date = datetime.date(e.expense_date.year, e.expense_date.month, e.expense_date.day,)
                    purchase_date_str = unicode(purchase_date)
                    purchase = ServicePurchase.objects.create(contactUid=contact.uid, date=purchase_date_str, summary=e.comment)
                    if e.expense_type.saasu_account_uid:
                        # Check is account item exists
                        account = TransactionCategory.objects.get(uid=e.expense_type.saasu_account_uid)
                        # create new item for ServiceInoice object
                        service_item = ServiceInvoiceItem.objects.create(description=e.expense_type.expense_type_name, accountUid=account.uid,
                                                                         totalAmountInclTax=e.total_amount)
                        # Append to a list of items
                        purchase.invoiceItems.append(service_item)
                        # Save purchase
                        purchase.save()
                        row_exported += 1
                    else:
                        return SAASU_ERRORS_CONSTANT['saasu_exp_type']
                else:
                    return SAASU_ERRORS_CONSTANT['saasu_contact']
            return row_exported

    def _get_total_amount(self):
        return self.expense_amount + self.tax_amount

    total_amount = property(_get_total_amount)

