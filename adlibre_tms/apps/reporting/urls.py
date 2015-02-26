# Django imports
from django.conf.urls.defaults import patterns, url

# Local imports
from reporting.views import *

urlpatterns = patterns('',
                       url(r'^$', reports, name='reports'),
                       url(r'^(?P<slug>\w+)/$', reports_detail, name='report_detail'),
                       )
