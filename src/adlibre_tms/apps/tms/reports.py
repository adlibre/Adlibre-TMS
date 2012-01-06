from django.utils.translation import ugettext_lazy as _

import reporting

from tms.models import *
from tms.forms import *
import datetime

class ProjectDetailsReport(reporting.Report):
    # Related model class
    model = Timesheet
    # Form class
    form_class = ProjectDetailsForm
    # Relative path to report template
    template_name = 'tms/reports/project_details.html'
    # Verbose name, used as report title
    verbose_name = _('Project Details')
    # Short description of report
    description = _('put description here...')

    def generate(self, *args, **kwargs):
        date_start = kwargs.get('date_start', None)
        date_end = kwargs.get('date_end', None)
        customer = kwargs.get('client', None)
        # project totals counters
        total_project_minutes = 0
        total_project_chargable_minutes = 0
        totals_for_project = False

        report_list = []
        #HACK: to fix dates in reports issue
        #+datetime.timedelta(days=1)
        timesheets = self.model.objects.filter(start_time__gte=date_start, end_time__lte=date_end+datetime.timedelta(days=1))
        # check for customer was specified in form request
        if customer:
            queryset = timesheets.filter(job__customer=customer).order_by('job', 'employee', 'start_time')
            if queryset:
                report_list.append({
                    customer.customer_code: {
                        'queryset': queryset,
                        'subsets': [timesheets.filter(job=j) for j in Job.objects.filter(customer=customer)],
                        },
                    })
        else:
            # generate report for all objects
            for c in Customer.objects.all():
                queryset = timesheets.filter(job__customer=c).order_by('job', 'employee', 'start_time')
                if queryset:
                    total_project_minutes += queryset.get_total_minutes()
                    total_project_chargable_minutes += queryset.get_total_charge_minutes()
                    subsets =  [timesheets.filter(job=j) for j in Job.objects.filter(customer=c)]
                    report_list.append({
                        c.customer_code: {
                            'queryset': queryset,
                            'subsets': subsets,
                            },
                        })
            # say we are generating report for all objects into context
            totals_for_project = True
        return {
            'date_start': date_start,
            'date_end': date_end,
            'report': report_list,
            'total_project_minutes': total_project_minutes,
            'total_project_chargable_minutes': total_project_chargable_minutes,
            'totals_for_project': totals_for_project,
                }

reporting.register('project_details', ProjectDetailsReport) # Do not forget to 'register' your class in reports


class DaysConsultantReport(reporting.Report):
    # Related model class
    model = Timesheet
    # Form class
    form_class = DaysConsultantForm
    # Relative path to report template
    template_name = 'tms/reports/days_consultant.html'
    # Verbose name, used as report title
    verbose_name = _('Days by Consultant')
    # Short description of report
    description = _('put description here...')

    def generate(self, *args, **kwargs):
        # Get start / end dates
        date_start = kwargs.get('date_start', None)
        date_end = kwargs.get('date_end', None)
        # Get consultant object or None
        consultant = kwargs.get('consultant', None)
        # initializing totals
        total_project_minutes = 0
        total_project_chargable_minutes = 0
        totals_for_project = False

        report_list = []
        #HACK: to fix dates in reports issue
        #+datetime.timedelta(days=1)
        timesheets = self.model.objects.filter(start_time__gte=date_start, end_time__lte=date_end+datetime.timedelta(days=1))
        if consultant:
            # generate report for a selected object
            report_list.append({
                consultant.user.username: {
                    'queryset': timesheets.filter(employee=consultant),
                    },
                })
        else:
            # generate report for all objects
            for e in Employee.objects.all():
                queryset = timesheets.filter(employee=e)
                total_project_minutes += queryset.get_total_minutes()
                total_project_chargable_minutes += queryset.get_total_charge_minutes()
                report_list.append({
                    e.user.username: {
                        'queryset': queryset,
                        },
                    })
            # say we are generating report for all objects into context
            totals_for_project = True
        return {
            'date_start': date_start,
            'date_end': date_end,
            'report': report_list,
            'total_project_minutes': total_project_minutes,
            'total_project_chargable_minutes': total_project_chargable_minutes,
            'totals_for_project': totals_for_project,
            }

reporting.register('days_consultant', DaysConsultantReport) # Do not forget to 'register' your class in reports


class ExpenseSummaryClientReport(reporting.Report):
    # Related model class
    model = Expense
    # Form class
    form_class = ExpenseSummaryClientForm
    # Relative path to report template
    template_name = 'tms/reports/expense_summary_client.html'
    # Verbose name, used as report title
    verbose_name = _('Expense Summary by Client')
    # Short description of report
    description = _('put description here...')

    def generate(self, *args, **kwargs):
        # Get start / end dates
        date_start = kwargs.get('date_start', None)
        date_end = kwargs.get('date_end', None)
        # Get client object or None
        customer = kwargs.get('client', None)
        # project totals counters
        total_project_amount = 0
        total_project_local_amount = 0
        totals_for_project = False

        report_list = []
        #HACK: to fix dates in reports issue
        #+datetime.timedelta(days=1)
        expenses = self.model.objects.filter(claim_date__gte=date_start, claim_date__lte=date_end+datetime.timedelta(days=1))
        if customer:
            queryset = expenses.filter(customer=customer).order_by('employee')
            if queryset:
                report_list.append({
                    customer.customer_code: {
                        'queryset': queryset,
                        'subsets': [queryset.filter(employee=e) for e in Employee.objects.all() if queryset.filter(employee=e)],
                        },
                    })
        else:
            # generate report for all objects
            for c in Customer.objects.all():
                queryset = expenses.filter(customer=c).order_by('employee')
                total_project_amount += queryset.get_total_amount()
                total_project_local_amount += queryset.get_total_local_amount()
                if queryset:
                    report_list.append({
                        c.customer_code: {
                            'queryset': queryset,
                            'subsets': [queryset.filter(employee=e) for e in Employee.objects.all() if queryset.filter(employee=e)],
                            },
                        })
            # say we are generating report for all objects into context
            totals_for_project = True
        return {
            'date_start': date_start,
            'date_end': date_end,
            'report': report_list,
            'total_project_amount': total_project_amount,
            'total_project_local_amount': total_project_local_amount,
            'totals_for_project': totals_for_project,
            }

reporting.register('expense_summary_client', ExpenseSummaryClientReport) # Do not forget to 'register' your class in reports


class ExpenseSummaryConsultantReport(reporting.Report):
    # Related model class
    model = Expense
    # Form class
    form_class = ExpenseSummaryConsultantForm
    # Relative path to report template
    template_name = 'tms/reports/expense_summary_consultant.html'
    # Verbose name, used as report title
    verbose_name = _('Outstanding Expenses by Consultant')
    # Short description of report
    description = _('put description here...')

    def generate(self, *args, **kwargs):
        # Get start / end dates
        date_start = kwargs.get('date_start', None)
        date_end = kwargs.get('date_end', None)
        consultant = kwargs.get('consultant', None)
        # project totals counters
        total_project_amount = 0
        total_project_local_amount = 0
        totals_for_project = False

        report_list = []
        #HACK: to fix dates in reports issue
        #+datetime.timedelta(days=1)
        expenses = self.model.objects.filter(claim_date__gte=date_start, claim_date__lte=date_end+datetime.timedelta(days=1))
        if consultant:
            queryset = expenses.filter(employee=consultant).order_by('customer')
            if queryset:
                report_list.append({
                    consultant.user.username: {
                        'queryset': queryset,
                        'subsets': [queryset.filter(customer=c) for c in Customer.objects.all() if queryset.filter(customer=c)],
                        },
                    })
        else:
            # generate report for all objects
            for e in Employee.objects.all():
                queryset = expenses.filter(employee=e).order_by('customer')
                total_project_amount += queryset.get_total_amount()
                total_project_local_amount += queryset.get_total_local_amount()
                if queryset:
                    report_list.append({
                        e.user.username: {
                            'queryset': queryset,
                            'subsets': [queryset.filter(customer=c) for c in Customer.objects.all() if queryset.filter(customer=c)],
                            },
                        })
            # say we are generating report for all objects into context
            totals_for_project = True
        return {
            'date_start': date_start,
            'date_end': date_end,
            'report': report_list,
            'total_project_amount': total_project_amount,
            'total_project_local_amount': total_project_local_amount,
            'totals_for_project': totals_for_project,
            }

reporting.register('expense_summary_consultant', ExpenseSummaryConsultantReport) # Do not forget to 'register' your class in reports
