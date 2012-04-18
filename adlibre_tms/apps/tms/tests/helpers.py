from django.contrib.auth.models import User
from test_settings import *
from django.core.urlresolvers import reverse

def new_test_user(TEST_USERNAME = TEST_USER_USERNAME, TEST_PASSWORD = TEST_USER_PASSWORD):
    """
    Helper function.
    Creating a test user and writing to database.
    using settings from test_settings.py by default.
    
    Creates a test user Iurii Garmash and puts him into base with provided
    or given username and password combination.
    Also makes user active
    """
    user, created = User.objects.get_or_create(username=TEST_USERNAME, 
                                      first_name='Iurii',
                                      last_name='Garmash',
                                      email='yuri@adlibre.com.au',
                                      is_active = True,)
    if created:
        user.set_password(TEST_PASSWORD)
        user.save()
    #print ('Created user:'+str(user))
    return user

def client_login(client, url=True, callback=''):
    """
    Helper function.
    Logs in a test user programmatically
    
    takes: - 'client' instance
           - an optional User() instance or creates one 
               from 'new_test_user()' function if no user specified
           - optional url to login with specified url
           - optional callback to redirect after login
               for e.g.: reverse('tms_timesheets')

    returns a tuple of logged in 'client' instance and a response object
    """

    new_test_user()
    if url:
        url = reverse('auth_login') + '?next=' + reverse('tms_timesheets')
    if callback=='':
        url = reverse('auth_login') + '?next=' + reverse('tms_timesheets')
    else:
        url = reverse('auth_login') + '?next=' + callback
    
    response = client.post(url, {'username': TEST_USER_USERNAME, 'password': TEST_USER_PASSWORD})
    return client, response
