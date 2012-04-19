from django.conf.urls.defaults import *

from tms.views import *

urlpatterns = patterns('',
   url(r'^timesheets/$', timesheets, name='tms_timesheets'),
   url(r'^timesheet_del/$', timesheet_del, name='tms_timesheet_del'),
   url(r'^expenses/$', expenses, name='tms_expenses'),
   url(r'^expense_del/$', expense_del, name='tms_expense_del'),
)
