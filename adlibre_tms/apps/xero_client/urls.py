from django.conf.urls import url
from views import XeroItemView

urlpatterns = [
    url(r'item_lookup/$', XeroItemView.as_view(), name='xero_item_lookup'),
]