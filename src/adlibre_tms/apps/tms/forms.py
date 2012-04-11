import datetime
from datetime import timedelta

from django import forms
from django.utils.translation import ugettext_lazy as _

from tms.models import *
from tms.contrib.saasu.widgets import *
from adlibre.contrib.widgets import SelectTimeWidget, SelectDateWidget

now = datetime.date.today()

__all__ = ['TimesheetForm', 'ExpenseTypeAdminForm', 'CustomerAdminForm', 'ExpenseForm', 'ProjectDetailsForm', 'DaysConsultantForm',
           'ExpenseSummaryClientForm', 'ExpenseSummaryConsultantForm']


class TimesheetForm(forms.ModelForm):

    date_start = forms.DateField(label=_("Date"), required=True, initial=now.isoformat(),
                                 widget=SelectDateWidget())

    start_time = forms.TimeField(label=_('Start'), required=True, initial=datetime.datetime.time(datetime.datetime.now()),
                                 widget=SelectTimeWidget(use_seconds=False))
    end_time = forms.TimeField(label=_('Finish'), required=True, initial=datetime.datetime.time(datetime.datetime.now()),
                               widget=SelectTimeWidget(use_seconds=False))

    class Meta:
        model = Timesheet
        exclude = ('employee', 'is_submitted', 'is_billed', )

    def __init__(self, *args, **kwargs):
        super(TimesheetForm, self).__init__(*args, **kwargs)
        self.fields['job'].queryset = Job.objects.filter(is_active=True)
        # Set fields order
        self.fields.keyOrder = [
            'job',
            'date_start',
            'start_time',
            'end_time',
            'comment',
            ]

    def clean_start_time(self):
        return datetime.datetime.combine(self.cleaned_data['date_start'], self.cleaned_data['start_time'])

    def clean_end_time(self):
        return datetime.datetime.combine(self.cleaned_data['date_start'], self.cleaned_data['end_time'])

    def clean_comment(self):
        return self.cleaned_data['comment'].strip()

    def clean(self):
        start_time = self.cleaned_data.get("start_time", 0)
        end_time = self.cleaned_data.get("end_time", 0)
        if start_time > end_time:
            msg = _("Start time cannot be after end time")
            self._errors["start_time"] = self.error_class([msg])
            del self.cleaned_data["start_time"]
            del self.cleaned_data["end_time"]
        return self.cleaned_data    


class ExpenseTypeAdminForm(forms.ModelForm):

    class Meta:
        model = ExpenseType

    def __init__(self, *args, **kwargs):
        super(ExpenseTypeAdminForm, self).__init__(*args, **kwargs)
        self.fields['saasu_account_uid'].widget = AdminSaasuAccountInputWidget()


class CustomerAdminForm(forms.ModelForm):

    class Meta:
        model = Customer

    def __init__(self, *args, **kwargs):
        super(CustomerAdminForm, self).__init__(*args, **kwargs)
        self.fields['saasu_contact_uid'].widget = AdminSaasuContactInputWidget()


class ServiceAdminForm(forms.ModelForm):

    class Meta:
        model = Service

    def __init__(self, *args, **kwargs):
        super(ServiceAdminForm, self).__init__(*args, **kwargs)
        self.fields['saasu_item_uid'].widget = AdminSaasuItemInputWidget()


class ExpenseForm(forms.ModelForm):

    expense_date = forms.DateField(label=_("Receipt Date"), required=True, initial=now.isoformat(),
                                   widget=SelectDateWidget())
    claim_date = forms.DateField(label=_("Claim Date"), required=True, initial=now.isoformat(),
                                 widget=SelectDateWidget())

    class Meta:
        model = Expense
        exclude = ('employee',)

    def __init__(self, *args, **kwargs):
        super(ExpenseForm, self).__init__(*args, **kwargs)
        # Set fields order
        self.fields.keyOrder = [
            'currency',
            'expense_date',
            'claim_date',
            'customer',
            'expense_type',
            'comment',
            'is_receipted',
            'payment_method',
            'is_taxable',
            'expense_amount',
            'tax_amount',
            'local_amount',
            ]
        
    def clean_comment(self):
        return self.cleaned_data['comment'].strip()

class ProjectDetailsForm(forms.Form):
    """ Project Details (101) form """

    # undefined client means get data for all client
    client = forms.ModelChoiceField(queryset=Customer.objects.all(), 
                                    empty_label=_("Everyone"), required=False)
    date_start = forms.DateField(label=_("Start Date"), required=True, initial=(now - timedelta(weeks=4)).isoformat(),
                                 widget=SelectDateWidget())
    date_end = forms.DateField(label=_("End Date"), required=True, initial=now.isoformat(),
                               widget=SelectDateWidget())

    def clean(self):
        date_start = self.cleaned_data.get("date_start", 0)
        date_end = self.cleaned_data.get("date_end", 0)
        if date_start > date_end:
            msg = _("Start date cannot be after end date")
            self._errors["date_start"] = self.error_class([msg])
            del self.cleaned_data["date_start"]
            del self.cleaned_data["date_end"]
        return self.cleaned_data


class DaysConsultantForm(forms.Form):
    """ Days by Consultant (103) form """

    # undefined consultant means get data for all consulants
    consultant = forms.ModelChoiceField(label=_("Select a consultant"), queryset=Employee.objects.all(), 
                                        empty_label=_("Everyone"), required=False)
    date_start = forms.DateField(label=_("Start Date"), required=True, initial=(now - timedelta(weeks=4)).isoformat(),
                                 widget=SelectDateWidget())
    date_end = forms.DateField(label=_("End Date"), required=True, initial=now.isoformat(),
                                 widget=SelectDateWidget())

    def clean(self):
        date_start = self.cleaned_data.get("date_start", 0)
        date_end = self.cleaned_data.get("date_end", 0)
        if date_start > date_end:
            msg = _("Start date cannot be after end date")
            self._errors["date_start"] = self.error_class([msg])
            del self.cleaned_data["date_start"]
            del self.cleaned_data["date_end"]
        return self.cleaned_data    


class ExpenseSummaryClientForm(forms.Form):
    """ Expense Summary by Client (220) form """

    # undefined client means get data for all client
    client = forms.ModelChoiceField(queryset=Customer.objects.all(), 
                                    empty_label=_("Everyone"), required=False)
    date_start = forms.DateField(label=_("Start Date"), required=True, initial=(now - timedelta(weeks=4)).isoformat(),
                                 widget=SelectDateWidget())
    date_end = forms.DateField(label=_("End Date"), required=True, initial=now.isoformat(),
                               widget=SelectDateWidget())

    def clean(self):
        date_start = self.cleaned_data.get("date_start", 0)
        date_end = self.cleaned_data.get("date_end", 0)
        if date_start > date_end:
            msg = _("Start date cannot be after end date")
            self._errors["date_start"] = self.error_class([msg])
            del self.cleaned_data["date_start"]
            del self.cleaned_data["date_end"]
        return self.cleaned_data


class ExpenseSummaryConsultantForm(forms.Form):
    """ Outstanding Expenses by Client (230) form """

    # undefined consultant means get data for all client
    consultant = forms.ModelChoiceField(queryset=Employee.objects.all(), 
                                        empty_label=_("Everyone"), required=False)
    date_start = forms.DateField(label=_("Start Date"), required=True, initial=(now - timedelta(weeks=4)).isoformat(),
                                 widget=SelectDateWidget())
    date_end = forms.DateField(label=_("End Date"), required=True, initial=now.isoformat(),
                               widget=SelectDateWidget())

    def clean(self):
        date_start = self.cleaned_data.get("date_start", 0)
        date_end = self.cleaned_data.get("date_end", 0)
        if date_start > date_end:
            msg = _("Start date cannot be after end date")
            self._errors["date_start"] = self.error_class([msg])
            del self.cleaned_data["date_start"]
            del self.cleaned_data["date_end"]
        return self.cleaned_data

