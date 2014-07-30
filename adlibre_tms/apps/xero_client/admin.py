from django.contrib import admin

from xero_client.forms import XeroAuthCredentialsForm
from xero_client.models import XeroAuthCredentials


class XeroAuthCredentialsModelAdmin(admin.ModelAdmin):
    form = XeroAuthCredentialsForm

admin.site.register(XeroAuthCredentials, XeroAuthCredentialsModelAdmin)