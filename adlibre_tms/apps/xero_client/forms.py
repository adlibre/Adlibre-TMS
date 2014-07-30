from django import forms
from django.core.urlresolvers import reverse
from xero_client.models import XeroAuthCredentials

from django.utils.safestring import mark_safe
from django.template.loader import render_to_string


class GetPinWidget(forms.Widget):
    template_name = 'auth_button_widget.html'

    class Media:
        js = (
            'admin/js/jquery.js',
            'js/xero-auth.js',
        )

    def render(self, name, value, attrs=None):
        context = {
            'url': reverse('xero-auth-pin'),
        }
        return mark_safe(render_to_string(self.template_name, context))


class XeroAuthCredentialsForm(forms.ModelForm):
    get_pin = forms.CharField(widget=GetPinWidget, required=False)

    class Meta:
        model = XeroAuthCredentials
