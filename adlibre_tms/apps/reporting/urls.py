from django.conf.urls import patterns, url
from reporting.views import *

urlpatterns = patterns('',
    url(r'^$', reports, name='reports'),
    url(r'^(?P<slug>\w+)/$', report_detail, name='report_detail'),
)
