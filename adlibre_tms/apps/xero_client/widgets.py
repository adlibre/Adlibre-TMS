from django import forms
from django.core.urlresolvers import reverse
from django.conf import settings
from django.forms.util import flatatt
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode
from django.utils.translation import ugettext as _


class XeroItemInput(forms.Widget):
    input_type = 'text'

    class Media:
        js = (
            settings.ADMIN_MEDIA_PREFIX + "js/core.js",
            settings.ADMIN_MEDIA_PREFIX + "xero/js/XeroItemLookups.js",
            )

    def render(self, name, value, attrs=None):
        output = []
        if value is None:
            value = ''
        xero_item_url = reverse('xero_item_lookup')
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_unicode(value)
        output.append('<input%s />' % flatatt(final_attrs))
        output.append('<a href="%s" class="saasu-contact-lookup" id="id_%s" onclick="return showXeroItemLookupPopup(this);">' % (xero_item_url, name))
        output.append('<img src="%simg/selector-search.gif" width="16" height="16" alt="%s" /></a>' % (settings.ADMIN_MEDIA_PREFIX, _('Lookup')))
        return mark_safe(u''.join(output))


class AdminXeroItemInputWidget(XeroItemInput):

    def __init__(self, attrs=None):
        final_attrs = {'class': 'vTextField'}
        if attrs is not None:
            final_attrs.update(attrs)
        super(AdminXeroItemInputWidget, self).__init__(attrs=final_attrs)
