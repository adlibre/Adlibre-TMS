from django.conf.urls import url
from views import XeroItemView, XeroContactView, XeroAccountView, XeroUserView

urlpatterns = [
    url(r'item_lookup/$', XeroItemView.as_view(), name='xero_item_lookup'),
    url(r'contact_lookup/$', XeroContactView.as_view(), name='xero_contact_lookup'),
    url(r'account_lookup/$', XeroAccountView.as_view(), name='xero_account_lookup'),
    url(r'user_lookup/$', XeroUserView.as_view(), name='xero_user_lookup'),
]