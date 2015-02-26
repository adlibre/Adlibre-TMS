from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.forms import Form
import reporting

__all__ = ['reports', 'report_detail']

@login_required
def reports(request, template_name='reporting/reports.html'):
    """Render a list of available reports"""
    # storing current user position in session
    request.session['enter_url'] = reverse('reports')
    reports_data = [
        (slug, unicode(r.verbose_name))
        for slug, r in reporting.all_reports()
    ]
    return direct_to_template(request, template_name, {'object_list': reports_data, })


@login_required
def report_detail(request, slug):
    """Render report detail or list of reports in case of wrong report slug is specified"""
    data = {}
    all_reports = {}
    template = 'reporting/reports.html'
    report = None
    form = Form()
    reports_date_init = True
    try:
        # Retrieving report name by slug specified in an URL
        report = reporting.get_report(slug)(request)
    except reporting.NoReportException:
        pass

    if report is not None:
        form = report.form_class(request.POST or None)
        if request.method == "POST" and form.is_valid():
            if request.POST.get('generate', None):
                data = report.generate(**form.cleaned_data)
                reports_date_init = False
        template = report.template_name
    else:
        # Wrong report slug is specified. rendering all the reports list
        all_reports = [(slug, unicode(r.verbose_name)) for slug, r in reporting.all_reports()]
    return direct_to_template(request, template, {
        'form': form,
        'data': data,
        'report': report,
        'reports_date_init': reports_date_init,
        'object_list': all_reports,
    })

