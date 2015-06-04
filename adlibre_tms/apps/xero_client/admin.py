from django.contrib import admin
from django.utils.functional import update_wrapper
from django.conf.urls import url, patterns

from xero_client.models import XeroInvoice, XeroExpenseClaim
from xero_client.forms import XeroInvoiceForm
from xero_client.forms import XeroExpenseForm
from xero_client.forms import create_invoice
from xero_client.forms import create_expense


class XeroInvoiceAdmin(admin.ModelAdmin):
    list_display = ('to', 'invoice_date', 'summary', 'xero_sync',)
    form = XeroInvoiceForm

    def get_urls(self):
        """Override the default "add" view with the invoice creation wizard."""

        def wrap(view):
            def wrapper(*args, **kwargs):
                kwargs['admin'] = self
                return self.admin_site.admin_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)

        urlpatterns = patterns('',
            url(r'^add/$',
                wrap(create_invoice),
                name='xero_invoice_add')
        )
        urlpatterns += super(XeroInvoiceAdmin, self).get_urls()
        return urlpatterns


class XeroExpenseAdmin(admin.ModelAdmin):
    list_display = ('to', 'xero_sync',)
    form = XeroExpenseForm

    def get_urls(self):
        """Override the default "add" view with the invoice creation wizard."""

        def wrap(view):
            def wrapper(*args, **kwargs):
                kwargs['admin'] = self
                return self.admin_site.admin_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)

        urlpatterns = patterns('',
            url(r'^add/$',
                wrap(create_expense),
                name='xero_expense_add')
        )
        urlpatterns += super(XeroExpenseAdmin, self).get_urls()
        return urlpatterns


admin.site.register(XeroInvoice, XeroInvoiceAdmin)
admin.site.register(XeroExpenseClaim, XeroExpenseAdmin)