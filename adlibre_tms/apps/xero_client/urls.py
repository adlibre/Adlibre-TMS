from django.conf.urls import url
from views import XeroItemView, XeroContactView

urlpatterns = [
    url(r'item_lookup/$', XeroItemView.as_view(), name='xero_item_lookup'),
    url(r'contact_lookup/$', XeroContactView.as_view(), name='xero_contact_lookup'),
]