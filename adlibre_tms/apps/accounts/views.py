from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.sites.models import Site

def welcome(request):
    """
    Handles site Welcome redirects behavior.
    It handles last opened page in session.
    And it's basically suits main home view.
    - if you go here somewhere from within current site it shows home page
        (HTTP_REFERER is current site)
    - if you are opening this page but last time you've closed it somewhere,
        say on 'timesheets', it will redirect you there
    - if you are not logged in it shows home page
    """
    if request.user.is_authenticated():
        # check if HOME request is from current site
        try:
            if request.environ['HTTP_REFERER']:
                referer = request.environ['HTTP_REFERER']
                current_site=Site.objects.get_current()
                if str(current_site) in referer:
                    #request is from current site
                    request.session['enter_url'] = reverse('home')
                    return render_to_response('homepage.html', {}, RequestContext(request))
        except: pass
        #check if session has redirect and do so
        try:
            redirect_url = request.session['enter_url']
            # anti loop protection
            if not request.session['enter_url'] == reverse('home'):
                return redirect(redirect_url)
            else:
                pass
        except:
            pass
    # simply set current session to home page and return it
    request.session['enter_url'] = reverse('home')
    return render_to_response('homepage.html', {}, RequestContext(request))
