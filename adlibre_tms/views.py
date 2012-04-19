from django.conf import settings
from django import http
from django.template import Context, RequestContext, loader


def server_error(request, template_name='500.html'):
    """
    500 error handler.

    Don't try to render full context. Just minimal.
    """
    t = loader.get_template(template_name)
    c = Context({
        'MEDIA_URL': settings.MEDIA_URL,
        'STATIC_URL': settings.STATIC_URL,
        })
    return http.HttpResponseServerError(t.render(c))


def url_error(request, template_name='404.html'):
    t = loader.get_template(template_name)
    c = RequestContext(request)

    return http.HttpResponseNotFound(t.render(c))

