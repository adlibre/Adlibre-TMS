from django.conf.urls.defaults import *

urlpatterns = patterns('tms.contrib.saasu.views',
                       url(r'^saasu_account_lookup/$', 'saasu_account_lookup', name='admin_saasu_account_lookup'),
                       url(r'^saasu_contact_lookup/$', 'saasu_contact_lookup', name='admin_saasu_contact_lookup'),
                       url(r'^saasu_item_lookup/$', 'saasu_item_lookup', name='admin_saasu_item_lookup'),
                       )
