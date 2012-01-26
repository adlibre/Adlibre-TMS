from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.http import HttpResponse

from saasu_client.settings import SAASU_ERORS
from saasu_client.models import ContactList, FullInventoryItemList, TransactionCategoryList


@login_required
def saasu_account_lookup(request, app_label="SAASU", template_name='saasu/admin/saasu_account_lookup.html'):
    is_popup = False
    if settings.DEMO:
        return HttpResponse(SAASU_ERORS['disabled'])
    if request.method == "GET":
        if request.GET.has_key('pop') or request.GET.has_key('popup'):
            is_popup = True
    return render_to_response(template_name, {
        'object_list': TransactionCategoryList.objects.get(isActive=True),
        'app_label': app_label,
        'is_popup': is_popup,
        }, context_instance=RequestContext(request))


@login_required
def saasu_contact_lookup(request, app_label="SAASU", template_name='saasu/admin/saasu_contact_lookup.html'):
    is_popup = False
    if settings.DEMO:
        return HttpResponse(SAASU_ERORS['disabled'])
    if request.method == "GET":
        if request.GET.has_key('pop') or request.GET.has_key('popup'):
            is_popup = True
    return render_to_response(template_name, {
        'object_list': ContactList.objects.get(isActive=True),
        'app_label': app_label,
        'is_popup': is_popup,
        }, context_instance=RequestContext(request))


@login_required
def saasu_item_lookup(request, app_label="SAASU", template_name='saasu/admin/saasu_item_lookup.html'):
    is_popup = False
    if settings.DEMO:
        return HttpResponse(SAASU_ERORS['disabled'])
    if request.method == "GET":
        if request.GET.has_key('pop') or request.GET.has_key('popup'):
            is_popup = True
    return render_to_response(template_name, {
        'object_list': FullInventoryItemList.objects.get(isActive=True),
        'app_label': app_label,
        'is_popup': is_popup,
        }, context_instance=RequestContext(request))

