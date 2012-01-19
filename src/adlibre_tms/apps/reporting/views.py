from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
import reporting

__all__ = ['reports', 'reports_detail']

@login_required
def reports(request, template_name='reporting/reports.html'):
    """ Render a list of avaiable reports """
    object_list = reporting.all_reports()
    # storing current user position in session
    request.session['enter_url'] = reverse('reports')
    return direct_to_template(request, template_name, {
        # HACK: object list rendered incorrectly in templates somehow
        'object_list': [(slug, unicode(r.verbose_name)) for slug, r in object_list],
        })


@login_required
def reports_detail(request, slug):
    """ Render report detail """
    data = {}
    reports_date_init = True
    report = reporting.get_report(slug)(request)
    form = report.form_class(request.POST or None)
    if request.method == "POST" and form.is_valid():
        if request.POST.get('generate', None):
            data = report.generate(**form.cleaned_data)
            reports_date_init = False
    return direct_to_template(request, report.template_name, {
        'form': form,
        'data': data,
        'report': report,
        'reports_date_init': reports_date_init,
        })
