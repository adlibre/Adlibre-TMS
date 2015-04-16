from django.contrib import admin
from django import forms

from xero_client.models import XeroInvoice


class XeroInvoiceForm(forms.ModelForm):
    class Meta:
        model = XeroInvoice

    def clean(self):
        """
        Uploads data to xero on validation

        required to be so because we want to see the errors from XERO API in admin 9in case one occurs during upload process
        """
        if self.cleaned_data.get('xero_sync'):
            self.instance.upload_to_xero(self.cleaned_data)
        return self.cleaned_data


class XeroInvoiceAdmin(admin.ModelAdmin):
    #fields = ('to', 'date', 'due_date', 'reference',)
    list_display = ('to', 'invoice_date', 'summary', 'xero_sync',)
    form = XeroInvoiceForm
    pass


admin.site.register(XeroInvoice, XeroInvoiceAdmin)