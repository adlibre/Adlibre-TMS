from xero.auth import PublicCredentials
from xero.auth import XeroUnauthorized

from django.http import HttpResponse, HttpResponseBadRequest
from django.views.generic.base import View

from xero_client.models import XeroCredentials


class XeroAuthHelper(View):

    def post(self, request, *args, **kwargs):
        key = request.POST.get('key', None)
        secret = request.POST.get('secret', None)
        try:
            credentials = PublicCredentials(key, secret)
        except XeroUnauthorized:
            return HttpResponseBadRequest('Wrong KEY or SECRET')
        cred_obj = XeroCredentials(secret=secret, credentials=credentials)
        cred_obj.save()
        return HttpResponse(credentials.url)