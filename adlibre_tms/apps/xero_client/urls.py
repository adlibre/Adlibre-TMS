from django.conf.urls import patterns, url
from xero_client.views import XeroAuthHelper

urlpatterns = patterns('',
    url(r'^xero-pin/', XeroAuthHelper.as_view(), name='xero-auth-pin'),
)