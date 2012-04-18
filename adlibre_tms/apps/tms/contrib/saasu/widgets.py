from django import forms
from django.conf import settings
from django.forms.util import flatatt
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode
from django.utils.translation import ugettext as _

__all__ = ['AdminSaasuAccountInputWidget', 'AdminSaasuContactInputWidget', 'AdminSaasuItemInputWidget']


class SaasuAccountInput(forms.Widget):
    input_type = 'text'

    class Media:
        js = (
            settings.ADMIN_MEDIA_PREFIX + "js/core.js",
            settings.ADMIN_MEDIA_PREFIX + "saasu/js/SaasuAccountLookups.js",
            )

    def render(self, name, value, attrs=None):
        output = []
        if value is None: value = ''
        saasu_account_url = '../../../saasu/saasu_account_lookup/'
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_unicode(value)
        output.append('<input%s />' % flatatt(final_attrs))
        output.append('<a href="%s" class="saasu-account-lookup" id="account_lookup_id_%s" onclick="return showSaasuAccountLookupPopup(this);">' % (saasu_account_url, name))
        output.append('<img src="%simg/admin/selector-search.gif" width="16" height="16" alt="%s" /></a>' % (settings.ADMIN_MEDIA_PREFIX, _('Lookup')))
        return mark_safe(u''.join(output))


class AdminSaasuAccountInputWidget(SaasuAccountInput):

    def __init__(self, attrs=None):
        final_attrs = {'class': 'vTextField'}
        if attrs is not None:
            final_attrs.update(attrs)
        super(AdminSaasuAccountInputWidget, self).__init__(attrs=final_attrs)


class SaasuContactInput(forms.Widget):
    input_type = 'text'

    class Media:
        js = (
            settings.ADMIN_MEDIA_PREFIX + "js/core.js",
            settings.ADMIN_MEDIA_PREFIX + "saasu/js/SaasuContactLookups.js",
            )

    def render(self, name, value, attrs=None):
        output = []
        if value is None: value = ''
        saasu_contact_url = '../../../saasu/saasu_contact_lookup/'
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_unicode(value)
        output.append('<input%s />' % flatatt(final_attrs))
        output.append('<a href="%s" class="saasu-contact-lookup" id="contact_lookup_id_%s" onclick="return showSaasuContactLookupPopup(this);">' % (saasu_contact_url, name))
        output.append('<img src="%simg/admin/selector-search.gif" width="16" height="16" alt="%s" /></a>' % (settings.ADMIN_MEDIA_PREFIX, _('Lookup')))
        return mark_safe(u''.join(output))


class AdminSaasuContactInputWidget(SaasuContactInput):

    def __init__(self, attrs=None):
        final_attrs = {'class': 'vTextField'}
        if attrs is not None:
            final_attrs.update(attrs)
        super(AdminSaasuContactInputWidget, self).__init__(attrs=final_attrs)


class SaasuItemInput(forms.Widget):
    input_type = 'text'

    class Media:
        js = (
            settings.ADMIN_MEDIA_PREFIX + "js/core.js",
            settings.ADMIN_MEDIA_PREFIX + "saasu/js/SaasuItemLookups.js",
            )

    def render(self, name, value, attrs=None):
        output = []
        if value is None: value = ''
        saasu_item_url = '../../../saasu/saasu_item_lookup/'
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_unicode(value)
        output.append('<input%s />' % flatatt(final_attrs))
        output.append('<a href="%s" class="saasu-item-lookup" id="item_lookup_id_%s" onclick="return showSaasuItemLookupPopup(this);">' % (saasu_item_url, name))
        output.append('<img src="%simg/admin/selector-search.gif" width="16" height="16" alt="%s" /></a>' % (settings.ADMIN_MEDIA_PREFIX, _('Lookup')))
        return mark_safe(u''.join(output))


class AdminSaasuItemInputWidget(SaasuItemInput):

    def __init__(self, attrs=None):
        final_attrs = {'class': 'vTextField'}
        if attrs is not None:
            final_attrs.update(attrs)
        super(AdminSaasuItemInputWidget, self).__init__(attrs=final_attrs)

