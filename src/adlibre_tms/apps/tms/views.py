from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseBadRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.core.urlresolvers import reverse
#from django.utils.translation import ugettext_lazy as _

import datetime
from time import mktime

from tms.models import Timesheet, Employee, Expense
from tms.forms import TimesheetForm, ExpenseForm

__all__ = ['timesheets', 'expenses', 'timesheet_del', 'expense_del']

# TODO: Combine this two pairs of views
#       They are similar. 
#       We can add Timesheets/Expenses in templates POST's somehow

@login_required
def timesheets(request, data_id = None, template_name='tms/timesheets.html',
               form_template_name='tms/timesheets_form.html',
               entry_template_name='tms/timesheets_single_entry.html',
               post_save_redirect='tms_timesheets'):
    """
    Displaying/Adding/Editing existing Timesheet entry in database.
    Used with AJAX calls now. Main gear view for Timesheets.
    
    - GET to this view retrieves Whole timesheets page (form and entries paginated table)
    - POST to this view: 
        - Adds a new entry 
            (When request.POST['data_id'] is not given (equal to u('') or u(' ') ))
        - Edits an entry 
            (Upon request.POST['data_id'] is equal to some Timesheet PK)
            (Creates a form instance with model of provided PK and validates it)
    - returns single Timesheet entry when form is valid
    - returns single Timesheet entry when form is valid and item was edited
        (Response contains <div class="edited_item_returned"></div> in this case... 
        To check for editing/adding entry in AJAX side)
    - Returns form with errors in case some errors occurred in form validation
    
    """
    # storing sessin user position
    request.session['enter_url'] = reverse('tms_timesheets')
    #checking for the edit data_id exists in the call and selecting behavior
    if request.method == 'POST' and data_id != ('' or ' '):
        try:
            data_id = request.POST['data_id']
            timesheet = get_object_or_404(Timesheet, pk=data_id)
            form = TimesheetForm(request.POST or None, instance=timesheet)
            edit_ajax = True
        except:
            data_id = ' '
            edit_ajax = False
            form = TimesheetForm(request.POST or None)
    else:
        form = TimesheetForm(request.POST or None)
    # form validation
    if request.method == 'POST' and form.is_valid():
        if request.POST.get('save', None):
            # saving data with form
            obj = form.save(commit=False)
            employee, created = Employee.objects.get_or_create(user=request.user)
            obj.employee = employee
            obj.save()
            # Add message to admin
            request.user.message_set.create(message='Timesheet entry was added successfully')
            context = {
                       'object': obj,
                       'edit_ajax': edit_ajax,
                       'add_init': True
                       }
            return render_to_response(entry_template_name, context, context_instance=RequestContext(request))
    elif request.method == 'POST' and not form.is_valid():
        #returning form with errors
        context = {
                   'form': form,
                   'edit_pk': data_id,
                   }
        return render_to_response(form_template_name, context, context_instance=RequestContext(request))

    timesheets_list = Timesheet.objects.filter(employee__user=request.user,
                                        is_submitted=False,
                                        is_billed=False).order_by('-start_time')
    # adding context vars for proper form init (described in project Wiki/TimesheetEntry)
    latest_date = ''
    latest_job = ''
    timesheets_today = timesheets_list.filter(start_time__startswith=str(datetime.date.today())).order_by('-end_time')
    if timesheets_today:
        latest_date = timesheets_today[0].end_time
        latest_job = timesheets_today[0].job.pk
    #returning empty form
    context = {
        'form': form,
        'object_list': timesheets_list,
        'init_latest_date':  latest_date,
        'init_latest_job' : latest_job,
        }
    return render_to_response(template_name, context, context_instance=RequestContext(request))

@login_required
def timesheet_del(request):
    """
    Deleting existing Timesheet entry in database.
    Used with AJAX calls now.
    
    - retrieves 'data_id' (Timesheet model PK) from request context
    - deletes model instance with this PK
    """
    if request.method == 'POST':
        #deleting object from base
        try:
            data_id = request.POST['data_id']
            timesheet = Timesheet.objects.get(pk=data_id)
            timesheet.delete()
        except:
            return HttpResponseBadRequest('Insufficient variables or faulty POST')
        return HttpResponse(data_id)
    else:
        return HttpResponseBadRequest('Only POST accepted')

@login_required
def expenses(request, data_id = None, template_name='tms/expenses.html',
               form_template_name='tms/expenses_form.html',
               entry_template_name='tms/expenses_single_entry.html',
               post_save_redirect='tms_expenses'):
    # storing current user position in session
    request.session['enter_url'] = reverse('tms_expenses')
    #checking for the edit data_id exists in the call and selecting behavior
    if request.method == 'POST' and data_id != ('' or ' '):
        try:
            data_id = request.POST['data_id']
            timesheet = get_object_or_404(Expense, pk=data_id)
            form = ExpenseForm(request.POST or None, instance=timesheet)
            edit_ajax = True
        except:
            data_id = ' '
            edit_ajax = False
            form = ExpenseForm(request.POST or None)
    else:
        form = ExpenseForm(request.POST or None)
    # form validation
    if request.method == 'POST' and form.is_valid():
        if request.POST.get('save', None):
            obj = form.save(commit=False)
            employee, created = Employee.objects.get_or_create(user=request.user)
            obj.employee = employee
            obj.save()
            # Add message
            request.user.message_set.create(message='Expenses entry was added successfully')
            context = {
                       'object': obj,
                       'edit_ajax': edit_ajax
                       }
            return render_to_response(entry_template_name, context, context_instance=RequestContext(request))
    elif request.method == 'POST' and not form.is_valid():
        #returning form with errors
        context = {
                   'form': form,
                   'edit_pk': data_id,
                   }
        return render_to_response(form_template_name, context, context_instance=RequestContext(request))
    
    #returning empty form
    context = {
        'form': form,
        'object_list': Expense.objects.filter(employee__user=request.user,
                                              #is_submitted=True
                                              ).order_by('-expense_date'),
        }
    return render_to_response(template_name, context, context_instance=RequestContext(request))

@login_required
def expense_del(request):
    """
    Deleting existing Expense entry in database.
    Used with AJAX calls now.
    
    - retrieves 'data_id' (Expense model PK) from request context
    - deletes model instance with this PK
    """
    if request.method == 'POST':
        #deleting object from base
        try:
            data_id = request.POST['data_id']
            expense = Expense.objects.get(pk=data_id)
            expense.delete()
        except:
            return HttpResponseBadRequest('Insufficient variables or faulty POST')
        return HttpResponse(data_id)
    else:
        return HttpResponseBadRequest('Only POST accepted')
