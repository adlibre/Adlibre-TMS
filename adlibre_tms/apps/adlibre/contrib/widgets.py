import re
import datetime
from dateutil.relativedelta import *

from django.conf import settings
from django.forms.widgets import Widget, Select, HiddenInput
from django.utils.dates import MONTHS_3 as MONTHS
from django.utils.safestring import mark_safe
from django.template.defaultfilters import capfirst
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _

__all__ = ['SelectDateWidget', 'SelectTimeWidget']

now = datetime.datetime.now()

RE_DATE = re.compile(r'(\d{4})-(\d\d?)-(\d\d?)$')

class SelectDateWidget(Widget):
    """
    A Widget that splits date input into two <select> boxes.

    This also serves as an example of a Widget that has more than one HTML
    element and hence implements value_from_datadict.
    """
    none_value = (0, '---')
    day_field = '%s_day'
    yearmonth_field = '%s_yearmonth'
    datepicker_field = '%s_datepicker'
    
    class Media:
        css = {
            'all': ('js/jquery-themes/base/jquery.ui.all.css',)
            }
        js = (
            'js/jquery-ui/jquery.ui.core.js',
            'js/jquery-ui/jquery.ui.widget.js',
            'js/jquery-ui/jquery.ui.position.js',
            'js/jquery-ui/jquery.ui.datepicker.js',
            )

    def __init__(self, attrs=None, month_range=6, required=True):
        # years is an optional list/tuple of years to use in the "year" select box.
        self.attrs = attrs or {}
        self.required = required
        if month_range:
            self.month_range = month_range
        
    def render(self, name, value, attrs=None):
        try:
            year_val, month_val, day_val = value.year, value.month, value.day
        except AttributeError:
            year_val = month_val = day_val = None
            if isinstance(value, basestring):
                match = RE_DATE.match(value)
                if match:
                    year_val, month_val, day_val = [int(v) for v in match.groups()]
        output = []

        start_date = now - relativedelta(months=self.month_range)
        end_date = now + relativedelta(months=self.month_range)

        if 'id' in self.attrs:
            id_ = self.attrs['id']
        else:
            id_ = 'id_%s' % name

        day_choices = [(i, i) for i in range(1, 32)]
        if not (self.required and value):
            day_choices.insert(0, self.none_value)
        local_attrs = self.build_attrs(id=self.day_field % id_)
        s = Select(choices=day_choices)
        select_html = s.render(self.day_field % name, day_val, local_attrs)
        block_html = """<span class='%(class)s day'>%(select_html)s</span>"""
        output.append(block_html % {
            'class': local_attrs['class'],
            'select_html': select_html,
            })

        yearmonth_choices = []
        ddate = start_date
        while ddate < end_date:
            yearmonth_choices.append(('%s-%s' % (ddate.year, ddate.month), '%s %s' % (unicode(capfirst(MONTHS[ddate.month])), ddate.year)))
            ddate = ddate + relativedelta(months=1)
        if not (self.required and value):
            yearmonth_choices.append(self.none_value)

        local_attrs['id'] = self.yearmonth_field % id_
        s = Select(choices=yearmonth_choices)
        select_html = s.render(self.yearmonth_field % name, '%s-%s' % (year_val, month_val), local_attrs)
        block_html = """<span class='%(class)s yearmonth'>%(select_html)s</span>"""
        output.append(block_html % {
            'class': local_attrs['class'],
            'select_html': select_html,
            })

        local_attrs['id'] = self.datepicker_field % id_
        i = HiddenInput()
        input_html = i.render(self.datepicker_field % name, None, local_attrs)
        output.append(input_html)

        other_html = render_to_string('adlibre/contrib/widgets/selectdatewidget.html', {
            'id_datepicker_field': self.datepicker_field % id_,
            'id_day_field': self.day_field % id_,
            'id_yearmonth_field': self.yearmonth_field % id_,
            'class': local_attrs['class'],
            'month_range': self.month_range,
            })
        output.append(other_html)

        return mark_safe(u'\n'.join(output))

    def id_for_label(self, id_):
        return '%s_yearmonth' % id_
    id_for_label = classmethod(id_for_label)

    def value_from_datadict(self, data, files, name):
        y, m = data.get(self.yearmonth_field % name).split('-')
        d = data.get(self.day_field % name)
        if y == m == d == "0":
            return None
        if y and m and d:
            return '%s-%s-%s' % (y, m, d)
        return data.get(name, None)

# Attempt to match many time formats:
# Example: "12:34:56 P.M."  matches:
# ('12', '34', ':56', '56', 'P.M.', 'P', '.', 'M', '.')
# ('12', '34', ':56', '56', 'P.M.')
# Note that the colon ":" before seconds is optional, but only if seconds are omitted
time_pattern = r'(\d\d?):(\d\d)(:(\d\d))? *([aApP]\.?[mM]\.?)?$'

RE_TIME = re.compile(time_pattern)
# The following are just more readable ways to access re.matched groups:
HOURS = 0
MINUTES = 1
SECONDS = 3
MERIDIEM = 4

class SelectTimeWidget(Widget):
    """
    A Widget that splits time input into <select> elements.
    Allows form to show as 24hr: <hour>:<minute>:<second>, (default)
    or as 12hr: <hour>:<minute>:<second> <am|pm> 
    
    Also allows user-defined increments for minutes/seconds
    """
    hour_field = '%s_hour'
    minute_field = '%s_minute'
    second_field = '%s_second' 
    meridiem_field = '%s_meridiem'
    now_field = '%s_now'
    twelve_hr = False # Default to 24hr.
    use_seconds = True
    
    def __init__(self, attrs=None, hour_step=None, minute_step=None, second_step=None, twelve_hr=False, use_seconds=True):
        """
        hour_step, minute_step, second_step are optional step values for
        for the range of values for the associated select element
        twelve_hr: If True, forces the output to be in 12-hr format (rather than 24-hr)
        use_seconds: If False, doesn't show seconds select element and stores seconds = 0.
        """
        self.attrs = attrs or {}
        
        if twelve_hr:
            self.twelve_hr = True # Do 12hr (rather than 24hr)
            self.meridiem_val = 'a.m.' # Default to Morning (A.M.)
        
        if hour_step and twelve_hr:
            self.hours = range(1,13,hour_step) 
        elif hour_step: # 24hr, with stepping.
            self.hours = range(0,24,hour_step)
        elif twelve_hr: # 12hr, no stepping
            self.hours = range(1,13)
        else: # 24hr, no stepping
            self.hours = range(0,24) 

        if minute_step:
            self.minutes = range(0,60,minute_step)
        else:
            self.minutes = range(0,60)

        if second_step:
            self.seconds = range(0,60,second_step)
        else:
            self.seconds = range(0,60)
        
        self.use_seconds = use_seconds

    def render(self, name, value, attrs=None):
        try: # try to get time values from a datetime.time object (value)
            hour_val, minute_val, second_val = value.hour, value.minute, value.second
            if self.twelve_hr:
                if hour_val >= 12:
                    self.meridiem_val = 'p.m.'
                else:
                    self.meridiem_val = 'a.m.'
        except AttributeError:
            hour_val = minute_val = second_val = 0
            if isinstance(value, basestring):
                match = RE_TIME.match(value)
                if match:
                    time_groups = match.groups();
                    hour_val = int(time_groups[HOURS]) % 24 # force to range(0-24)
                    minute_val = int(time_groups[MINUTES]) 
                    if time_groups[SECONDS] is None:
                        second_val = 0
                    else:
                        second_val = int(time_groups[SECONDS])
                    
                    # check to see if meridiem was passed in
                    if time_groups[MERIDIEM] is not None:
                        self.meridiem_val = time_groups[MERIDIEM]
                    else: # otherwise, set the meridiem based on the time
                        if self.twelve_hr:
                            if hour_val >= 12:
                                self.meridiem_val = 'p.m.'
                            else:
                                self.meridiem_val = 'a.m.'
                        else:
                            self.meridiem_val = None
                    

        # If we're doing a 12-hr clock, there will be a meridiem value, so make sure the
        # hours get printed correctly
        if self.twelve_hr and self.meridiem_val:
            if self.meridiem_val.lower().startswith('p') and hour_val > 12 and hour_val < 24:
                hour_val = hour_val % 12
        elif hour_val == 0:
            hour_val = 12
            
        output = []
        if 'id' in self.attrs:
            id_ = self.attrs['id']
        else:
            id_ = 'id_%s' % name

        # For times to get displayed correctly, the values MUST be converted to unicode
        # When Select builds a list of options, it checks against Unicode values
        hour_val = u"%.2d" % hour_val
        minute_val = u"%.2d" % minute_val
        second_val = u"%.2d" % second_val

        hour_choices = [("%d"%i, "%.2d"%i) for i in self.hours]
        local_attrs = self.build_attrs(id=self.hour_field % id_)
        select_html = Select(choices=hour_choices).render(self.hour_field % name, hour_val, local_attrs)
        block_html = """<span class='%(class)s hour'>%(select_html)s</span>"""
        output.append(block_html % {
            'class': local_attrs['class'],
            'select_html': select_html,
            })

        minute_choices = [("%d"%i, "%.2d"%i) for i in self.minutes]
        local_attrs['id'] = self.minute_field % id_
        select_html = Select(choices=minute_choices).render(self.minute_field % name, minute_val, local_attrs)
        block_html = """<span class='%(class)s minute'>%(select_html)s</span>"""
        output.append(block_html % {
            'class': local_attrs['class'],
            'select_html': select_html,
            })


        if self.use_seconds:
            second_choices = [("%d"%i, "%.2d"%i) for i in self.seconds]
            local_attrs['id'] = self.second_field % id_
            select_html = Select(choices=second_choices).render(self.second_field % name, second_val, local_attrs)
            block_html = """<span class='%(class)s second'>%(select_html)s</span>"""
            output.append(block_html % {
                'class': local_attrs['class'],
                'select_html': select_html,
                })

    
        if self.twelve_hr:
            #  If we were given an initial value, make sure the correct meridiem gets selected.
            if self.meridiem_val is not None and  self.meridiem_val.startswith('p'):
                    meridiem_choices = [('p.m.','p.m.'), ('a.m.','a.m.')]
            else:
                meridiem_choices = [('a.m.','a.m.'), ('p.m.','p.m.')]

            local_attrs['id'] = local_attrs['id'] = self.meridiem_field % id_
            select_html = Select(choices=meridiem_choices).render(self.meridiem_field % name, self.meridiem_val, local_attrs)
            block_html = """<span class='%(class)s meridiem'>%(select_html)s</span>"""
            output.append(block_html % {
                'class': local_attrs['class'],
                'select_html': select_html,
                })

        other_html = render_to_string('adlibre/contrib/widgets/selecttimewidget.html', {
            'id_now_field': self.now_field % id_,
            'id_hour_field': self.hour_field % id_,
            'id_minute_field': self.minute_field % id_,
            'class': local_attrs['class'],
            })
        output.append(other_html)

        return mark_safe(u'\n'.join(output))

    def id_for_label(self, id_):
        return '%s_hour' % id_
    id_for_label = classmethod(id_for_label)

    def value_from_datadict(self, data, files, name):
        # if there's not h:m:s data, assume zero:
        h = data.get(self.hour_field % name, 0) # hour
        m = data.get(self.minute_field % name, '00') # minute
        s = data.get(self.second_field % name, '00') # second

        meridiem = data.get(self.meridiem_field % name, None)

        #NOTE: if meridiem is None, assume 24-hr
        if meridiem is not None:
            if meridiem.lower().startswith('p') and int(h) != 12:
                h = (int(h)+12)%24 
            elif meridiem.lower().startswith('a') and int(h) == 12:
                h = 0

        if (int(h) == 0 or h) and m and s:
            return '%s:%s:%s' % (h, m, s)

        return data.get(name, None)
