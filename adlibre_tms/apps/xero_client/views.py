from django.views.generic import View
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse

from models import XeroItemList


class XeroItemView(View):
    template_name = 'xero/xero_item_lookup.html'
    app_label = 'xero_client'

    def get(self, request):
        is_popup = False

        # if settings.DEMO:
        #     return HttpResponse('Disabled in DEMO mode')

        if request.GET.has_key('pop') or request.GET.has_key('popup'):
            is_popup = True
        xero = XeroItemList()
        print xero.items

        return render(request, self.template_name, {
            'object_list': xero.items,
            'app_label': self.app_label,
            'is_popup': is_popup,
        })
