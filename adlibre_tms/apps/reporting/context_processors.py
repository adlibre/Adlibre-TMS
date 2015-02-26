import reporting

def reports(request):
    return {
        'reports': reporting.all_reports(),
        }
