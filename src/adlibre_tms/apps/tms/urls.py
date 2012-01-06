from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required
from django.views.generic.list_detail import object_list, object_detail

from tms.models import *
from tms.views import *

urlpatterns = patterns('',
                       #new AJAX urls to edit/add/del Timesheets by Iurii Garmash
                       url(r'^timesheets/$', timesheets, name='tms_timesheets'),
                       url(r'^timesheet_del/$', timesheet_del, name='tms_timesheet_del'),
                       
                       #new AJAX urls to edit/add/del Expenses by Iurii Garmash
                       url(r'^expenses/$', expenses, name='tms_expenses'),
                       url(r'^expense_del/$', expense_del, name='tms_expense_del'),

                       #prohibited urls
                       url(r'^timesheet/(?P<object_id>[0-9]+)/$', login_required(object_detail), {
                           'queryset': Timesheet.objects.all(),
                           'template_name': 'tms/timesheet_detail.html',
                           }, name='tms_timesheet_detail'),
                       url(r'^customer/$', login_required(object_list), {
                           'queryset': Customer.objects.all(),
                           'template_name': 'tms/customer_list.html',
                           }, name='tms_customer_list'),
                       url(r'^customer/(?P<object_id>[0-9]+)/$', login_required(object_detail), {
                           'queryset': Customer.objects.all(),
                           'template_name': 'tms/customer_detail.html',
                           }, name='tms_customer_detail'),

                       url(r'^job/$', login_required(object_list), {
                           'queryset': Job.objects.all(),
                           'template_name': 'tms/job_list.html',
                           }, name='tms_job_list'),
                       url(r'^job/(?P<object_id>[0-9]+)/$', login_required(object_detail), {
                           'queryset': Job.objects.all(),
                           'template_name': 'tms/job_detail.html',
                           }, name='tms_job_detail'),

                       url(r'^service/$', login_required(object_list), {
                           'queryset': Service.objects.all(),
                           'template_name': 'tms/service_list.html',
                           }, name='tms_service_list'),
                       url(r'^service/(?P<object_id>[0-9]+)/$', login_required(object_detail), {
                           'queryset': Service.objects.all(),
                           'template_name': 'tms/service_detail.html',
                           }, name='tms_service_detail'),

                       url(r'^project/$', login_required(object_list), {
                           'queryset': Project.objects.all(),
                           'template_name': 'tms/project_list.html',
                           }, name='tms_project_list'),
                       url(r'^project/(?P<object_id>[0-9]+)/$', login_required(object_detail), {
                           'queryset': Project.objects.all(),
                           'template_name': 'tms/project_detail.html',
                           }, name='tms_project_detail'),
                       )
