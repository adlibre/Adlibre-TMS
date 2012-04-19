from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.conf import settings
from accounts.views import welcome

import reporting
reporting.autodiscover()

from django.contrib import admin
admin.autodiscover()

# Admin Apps
urlpatterns = patterns('',
    (r'^admin/saasu/', include('tms.contrib.saasu.urls')),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
)


if settings.DEBUG:

    # staticfiles for debugging
    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT,
            'show_indexes': True,
        }),
    )

    urlpatterns += patterns('',
        (r'^500/$', 'adlibre_tms.views.server_error'),
        (r'^404/$', 'adlibre_tms.views.url_error'),
    )


# Site Apps
urlpatterns += patterns('',
    url(r'^$', welcome, name='home'),

    url(r'^accounts/', include('accounts.urls')),
    url(r'^reporting/', include('reporting.urls')),
    url(r'^tms/', include('tms.urls')),
)

#if settings.SERVE_MEDIA:
#    from staticfiles.urls import staticfiles_urlpatterns
#    urlpatterns += staticfiles_urlpatterns()


