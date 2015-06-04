from django import forms
from django.contrib.formtools.wizard import FormWizard
from django.utils.encoding import force_unicode
from django.core.urlresolvers import reverse

from xero_client.models import XeroInvoice
from xero_client.models import XeroExpenseClaim
from xero_client.models import get_projects_tuple
from xero_client.models import get_customers_tuple
from tms.models import Timesheet
from tms.models import Expense


class XeroInvoiceProjectsForm(forms.Form):
    to = forms.ChoiceField(
        choices=get_projects_tuple(),
        help_text='Name of the company invoice is being issued to.'
    )

    def clean(self):
        """
        Uploads data to xero on validation

        required to be so because we want to see the errors from XERO API
        at django admin, in case one occurs during upload process
        """
        return self.cleaned_data


class XeroInvoiceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(XeroInvoiceForm, self).__init__(*args, **kwargs)
        if self.initial:
            if 'form0_cleaned' in self.initial:
                project_code = self.initial['form0_cleaned']['to']
                # access object through self.instance...
                # TODO: Is billed/submitted
                self.fields['items'].queryset = Timesheet.objects.filter(
                    job__project__project_name=project_code
                )

    class Meta:
        model = XeroInvoice
        exclude = ('to', )

    def clean(self):
        """
        Uploads data to xero on validation

        required to be so because we want to see the errors from XERO API
        at django admin, in case one occurs during upload process
        """
        if 'form0_cleaned' in self.initial:
            project_code = self.initial['form0_cleaned']['to']
            self.cleaned_data['to'] = project_code
        if self.cleaned_data.get('xero_sync'):
            self.instance.upload_to_xero(self.cleaned_data)
        return self.cleaned_data


class XeroInvoiceWizard(FormWizard):
    """
    FormWizard, representing the invoice creation process.

    To add a new invoice to the database, we'll need to:

    1. Select a corresponding project
    2. Suggest user Timesheets for that project he would like to add to that invoice.
    3. Possibly upload invoice to Xero in case the check mark is set.

    Each of these steps is handled by an appropriate form; the "done" method
    uses the data collected to create the invoice.
    """
    @property
    def __name__(self):
        # Python instances don't define __name__ (though functions and classes do).
        # We need to define this, otherwise the call to "update_wrapper" fails:
        return self.__class__.__name__

    def get_template(self, step):
        # Optional: return the template used in rendering this wizard:
        return 'xero/wizard.html'

    def parse_params(self, request, admin=None, *args, **kwargs):
        # Save the ModelAdmin instance so it's available to other methods:
        self._model_admin = admin
        # The following context variables are expected by the admin
        # "change_form.html" template; Setting them enables stuff like
        # the breadcrumbs to "just work":
        opts = admin.model._meta
        self.extra_context.update({
            'title': 'Add %s' % force_unicode(opts.verbose_name),
            # See http://docs.djangoproject.com/en/dev/ref/contrib/admin/#adding-views-to-admin-sites
            # for why we define this variable.
            'current_app': admin.admin_site.name,
            'has_change_permission': admin.has_change_permission(request),
            'add': True,
            'opts': opts,
            'root_path': reverse('admin:index'),
            'app_label': opts.app_label,
        })

    def process_step(self, request, form, step):
        """
        Hook for modifying the FormWizard's internal state, given a fully
        validated Form object. The Form is guaranteed to have clean, valid
        data.

        This method should *not* modify any of that data. Rather, it might want
        to set self.extra_context or dynamically alter self.form_list, based on
        previously submitted forms.

        Note that this method is called every time a page is rendered for *all*
        submitted steps.
        """
        # Transfering form data from step 0 to form 1 step for rendering
        if step == 0:
            self.initial[1] = {'form0_cleaned': form.cleaned_data}
        return

    def render_template(self, request, form, previous_fields, step, context=None):
        from django.contrib.admin.helpers import AdminForm
        # Wrap this form in an AdminForm so we get the fieldset stuff:
        form = AdminForm(form, [(
            'Step %d of %d' % (step + 1, self.num_steps()),
            {'fields': form.base_fields.keys()}
            )], {})
        context = context or {}
        context.update({
            'media': self._model_admin.media + form.media
        })
        return super(XeroInvoiceWizard, self).render_template(request, form, previous_fields, step, context)

    def done(self, request, form_list):
        data = {}
        for form in form_list:
            data.update(form.cleaned_data)

        invoice = XeroInvoice.objects.create(
            to=data['to'],
            summary=data['summary'],
            xero_sync=data['xero_sync'],
            #items=data['items'],
            invoice_date=data['invoice_date'],
            due_date=data['due_date'],
        )
        # Adding items to timesheets
        for item in data['items']:
            invoice.items.add(item.pk)
        # Display success message and redirect to changelist:
        return self._model_admin.response_add(request, invoice)


class XeroExpenseProjectsForm(forms.Form):
    to = forms.ChoiceField(
        choices=get_customers_tuple(),
        help_text='Name of the company expense claim is being issued to.'
    )

    def clean(self):
        """
        Uploads data to xero on validation
        """
        return self.cleaned_data


class XeroExpenseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(XeroExpenseForm, self).__init__(*args, **kwargs)
        if self.initial:
            if 'form0_cleaned' in self.initial:
                customer_name = self.initial['form0_cleaned']['to']
                # access object through self.instance...
                # TODO: is billed/submitted filtering
                self.fields['items'].queryset = Expense.objects.filter(
                    customer__customer_name=customer_name
                )

    class Meta:
        model = XeroExpenseClaim
        exclude = ('to', )

    def clean(self):
        """Uploads data to xero on validation"""
        if 'form0_cleaned' in self.initial:
            project_code = self.initial['form0_cleaned']['to']
            self.cleaned_data['to'] = project_code
        if self.cleaned_data.get('xero_sync'):
            self.instance.upload_to_xero(self.cleaned_data)
        return self.cleaned_data


class XeroExpenseWizard(FormWizard):
    """
    FormWizard, representing the invoice creation process.

    To add a new invoice to the database, we'll need to:

    1. Select a corresponding project
    2. Suggest user Expenses for that project he would like to add to that invoice.
    3. Possibly upload invoice to Xero in case the check mark is set.

    Each of these steps is handled by an appropriate form the "done" method
    uses the data collected to create the invoice.
    """
    @property
    def __name__(self):
        # Python instances don't define __name__ (though functions and classes do).
        # We need to define this, otherwise the call to "update_wrapper" fails:
        return self.__class__.__name__

    def get_template(self, step):
        # Optional: return the template used in rendering this wizard:
        return 'xero/wizard.html'

    def parse_params(self, request, admin=None, *args, **kwargs):
        # Save the ModelAdmin instance so it's available to other methods:
        self._model_admin = admin
        # The following context variables are expected by the admin
        # "change_form.html" template; Setting them enables stuff like
        # the breadcrumbs to "just work":
        opts = admin.model._meta
        self.extra_context.update({
            'title': 'Add %s' % force_unicode(opts.verbose_name),
            # See http://docs.djangoproject.com/en/dev/ref/contrib/admin/#adding-views-to-admin-sites
            # for why we define this variable.
            'current_app': admin.admin_site.name,
            'has_change_permission': admin.has_change_permission(request),
            'add': True,
            'opts': opts,
            'root_path': reverse('admin:index'),
            'app_label': opts.app_label,
        })

    def process_step(self, request, form, step):
        """
        Hook for modifying the FormWizard's internal state, given a fully
        validated Form object. The Form is guaranteed to have clean, valid
        data.

        This method should *not* modify any of that data. Rather, it might want
        to set self.extra_context or dynamically alter self.form_list, based on
        previously submitted forms.

        Note that this method is called every time a page is rendered for *all*
        submitted steps.
        """
        # Transfering form data from step 0 to form 1 step for rendering
        if step == 0:
            self.initial[1] = {'form0_cleaned': form.cleaned_data}
        return

    def render_template(self, request, form, previous_fields, step, context=None):
        from django.contrib.admin.helpers import AdminForm
        # Wrap this form in an AdminForm so we get the fieldset stuff:
        form = AdminForm(form, [(
            'Step %d of %d' % (step + 1, self.num_steps()),
            {'fields': form.base_fields.keys()}
            )], {})
        context = context or {}
        context.update({
            'media': self._model_admin.media + form.media
        })
        return super(XeroExpenseWizard, self).render_template(request, form, previous_fields, step, context)

    def done(self, request, form_list):
        data = {}

        for form in form_list:
            data.update(form.cleaned_data)
        expense = XeroExpenseClaim.objects.create(
            to=data['to'],
            xero_sync=data['xero_sync'],
        )
        # Adding items to timesheets
        for item in data['items']:
            expense.items.add(item.pk)
        # # Display success message and redirect to changelist:
        return self._model_admin.response_add(request, expense)

create_invoice = XeroInvoiceWizard([XeroInvoiceProjectsForm, XeroInvoiceForm])
create_expense = XeroExpenseWizard([XeroExpenseProjectsForm, XeroExpenseForm])


