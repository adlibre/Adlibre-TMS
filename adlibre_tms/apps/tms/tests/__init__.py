from django.test import TestCase
import unittest
from django.test import Client
from test_settings import *
from helpers import *
from django.core.urlresolvers import reverse
from tms.forms import *
from tms.models import Timesheet, Expense, Job, Employee
from django_any import any_model
import datetime
from django.shortcuts import get_object_or_404
import reporting

class BasicAPPOk(unittest.TestCase):
    """
    Test of app ability to run at all
    """
    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        unittest.TestCase.setUp(self)

    def test_app_has_no_errors(self):
        help = """
        Testing an app that it has no errors when 
        called main Url '/'
        testing if Response 200.
        """
        response = self.client.get('/', {})
        self.failUnlessEqual(response.status_code, 200)
        #print ''
        #print 'BasicAPPOK test passed........................................................OK'


class Auth_Tests(TestCase):
    """
    Bacic test of user login sequence functionality
    """
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_login(self):
        help = """
        Testing an app login programmatically
        
        - tests main login page loads with code 200
        - tests POST to login url with test user data with code 302 and redirect to 
            tms.timesheets view
        
        """
        #testing login page exist and works
        response = self.client.get(reverse('auth_login'), {})
        #print ('Login URL response code: '+str(response.status_code))
        self.failUnlessEqual(response.status_code, 200)

        self.client, response = client_login(self.client, callback=reverse('tms_timesheets'))
        self.assertRedirects(response, 'http://testserver'+reverse('tms_timesheets'))
        #print 'Login test passed.............................................................OK'

    def test_logout(self):
        help = """
        Testing an app logout programmatically
        
        - makes simple login with redirect to tms_timesheets' url
        - tests a logout works
        """
        #logging in
        self.client, response = client_login(self.client, callback=reverse('tms_timesheets'))
        self.assertRedirects(response, 'http://testserver'+reverse('tms_timesheets'))
#
        #logout
        response = self.client.get(reverse('auth_logout'))
        self.failUnlessEqual(response.status_code, 200)
        #print 'Logout test passed............................................................OK'


class TMSMainUrlsTest(TestCase):

    def setUp(self):
        """
        Test's init sequence.

        - saves test data directly into model needed for tests
            Creates random timesheet
        """
        # Every test needs a client.
        self.client = Client()
        self.client, self.response = client_login(self.client, callback=reverse('tms_timesheets'))
        self.datetime = datetime.datetime.now
        self.user = new_test_user()
        self.job_model = any_model(Job, is_active=True)
        try:
            self.employee = any_model(Employee, user = self.user)
        except:
            #employee with this user already exists
            self.employee = Employee.objects.get(user=self.user)
        self.timesheet1 = any_model(Timesheet,
                                    employee=self.employee,
                                    is_submitted=False,
                                    is_billed=False,
                                    comment='Django_tests comment for timesheet model1')
        self.expense1 = any_model(Expense,
                                    comment='Django_tests comment for expense model1')

    def test_timesheets_render_data(self):
        help = """
        Tests for APP 'tms.views.timesheets' basic functiuonality:

        - tries to log in
        - checks tms.timesheets view returns response with code 200 (view url works)
        - checks if response form exists
        - checks if data can be saved to model
        - checks response for test data from test's init model
        """
        #print help
        #checking if page loads ok
        response = self.client.get(reverse('tms_timesheets'), {})
        self.failUnlessEqual(response.status_code, 200)

        #checking for Form exists in the context
        self.assertContains(response, 'form')
        self.failUnlessEqual(response.context['form'].initial, {})

        #checking for test data inserted into context in context
        self.assertContains(response, self.timesheet1.comment)

        #print 'tms.timesheets render entries test passed..................................OK'


    def test_timesheets_add_entry_with_form(self):
        help = """
        Tests for APP 'tms.views.timesheets' ADDING functiuonality:

        - checks for ability to POST form data to view
        - checks for view returns with code 200 and form with errors
            in response to faulty form POST data
        - checks for valid data posting to view.
            Form should return a valid HttpResponse html data,
            containing rendered current added entry
            checked by part of unique string in entry
        - checks it does not contain edit string
            required to trigger AXAJ actions of replace
            edited item on JavaScript side.
        """
        #print help

        # trying to post form data to view with bad POST data
        # checking response contains form and
        # error (form errors exist so it should have at least one)
        response = self.client.post(reverse('tms_timesheets'), {
                            "job": '200',
                            "date_start_day": "8",
                            "date_start_yearmonth": "2011-9",
                            "date_start_datepicker": "",
                            "start_time_hour": "16",
                            "start_time_minute": "0",
                            "end_time_hour": "16",
                            "end_time_minute": "0",
                            "comment": "some test comment",
                            "save": "Save",
                            "data_id": "",
                                                                  })
        self.failUnlessEqual(response.status_code, 200)
        self.assertContains(response, 'form')
        self.assertContains(response, 'error')

        # testing valid data posting to view. Form should return
        # a valid HttpResponse html data, containing rendered current added entry
        # by part of unique string in entry
        # checking it does not contain edit string
        # required to trigger AXAJ actions on JavaScript side.
        response = self.client.post(reverse('tms_timesheets'), {
                                "job": '1',
                                "date_start_day": "8",
                                "date_start_yearmonth": "2011-9",
                                "date_start_datepicker": "",
                                "start_time_hour": "16",
                                "start_time_minute": "0",
                                "end_time_hour": "16",
                                "end_time_minute": "0",
                                "comment": "some test comment",
                                "save": "Save",
                                "data_id": " ",
                                                                      })
        self.failUnlessEqual(response.status_code, 200)
        self.assertContains(response, 'return timesheet_editbtn_press')
        self.assertNotContains(response, 'form')
        self.assertNotContains(response, 'edited_item_returned')
        #print 'tms.timesheets test passed.................................................OK'




    def test_timesheets_edit_actions(self):
        help = """
        Tests for APP 'tms.views.timesheet' EDITING functiuonality:

        - checks for a valid HttpResponse html data,
            containing rendered current added entry
            by part of unique string in entry
            checking it contains edit string
            required to trigger AXAJ EDIT actions on JavaScript side.
        - testing invalid data posting to view.
            View should return form with errors and 200 status
        """
        #print help
        #trying to access url of editing test database entry and get the form
        response = self.client.get(reverse('tms_timesheets'), {})
        self.failUnlessEqual(response.status_code, 200)

        # checks for a valid HttpResponse html data,
        # containing rendered current added entry
        # by part of unique string in entry
        # checking it contains edit string
        # required to trigger AXAJ actions on JavaScript side.
        response = self.client.post(reverse('tms_timesheets'), {
                            "job": '1',
                            "date_start_day": "8",
                            "date_start_yearmonth": "2011-9",
                            "date_start_datepicker": "",
                            "start_time_hour": "16",
                            "start_time_minute": "0",
                            "end_time_hour": "16",
                            "end_time_minute": "0",
                            "comment": "some test comment",
                            "save": "Save",
                            "data_id": "1",
                                                                  })
        self.failUnlessEqual(response.status_code, 200)
        self.assertContains(response, 'return timesheet_editbtn_press')
        self.assertNotContains(response, 'form')
        self.assertContains(response, 'edited_item_returned')

        # testing invalid data posting to view.
        # View should return form with errors and 200 status
        response = self.client.post(reverse('tms_timesheets'), {
                            "job": '2000', #faulty job pk ID
                            "date_start_day": "8",
                            "date_start_yearmonth": "2011-9",
                            "date_start_datepicker": "",
                            "start_time_hour": "16",
                            "start_time_minute": "0",
                            "end_time_hour": "16",
                            "end_time_minute": "0",
                            "comment": "some test comment",
                            "save": "Save",
                            "data_id": "1",
                                                                  })
        self.failUnlessEqual(response.status_code, 200)
        self.assertContains(response, 'form')
        self.assertContains(response, 'error')
        #print 'tms.timesheets.edit test passed............................................OK'

    def test_timesheet_del_urls(self):
        help = """
        Tests for APP 'tms.views.timesheet_del' DELETING functiuonality:

        - tries to log in
        - checks 'tms_timesheet_del' view returns response with code 400
        - checks POST to this view returns code 400
        - checks empty POST to this view returns 400 too
        - checks post with variable returns 200 and desired model PK (for AJAX manipulations)
        """
        #print help
        #trying to access url of deleting test database entry
        response = self.client.get(reverse('tms_timesheet_del'), {})
        self.failUnlessEqual(response.status_code, 400)

        # empty POST to this view returns 400 too
        response = self.client.post(reverse('tms_timesheet_del'), {})
        self.failUnlessEqual(response.status_code, 400)

        # post with variable returns 200 and desired model PK (for AJAX manipulations)
        response = self.client.post(reverse('tms_timesheet_del'), {'data_id': self.timesheet1.pk})
        self.failUnlessEqual(response.content, str(self.timesheet1.pk))
        #print 'tms.timesheet.del test passed...............................................OK'



# prohibited view... Does not need testing

#    def test_timesheet_detail_urls(self):
#        help = """
#        Tests for APP 'tms.views.timesheet' basic functiuonality:
#
#        - tries to log in
#        - checks 'tms_timesheet_detail' view returns response with code 200
#        - checks response for test data from test's init model
#        - check for test model context in response
#        """
#        print help
#        #testing detail view exists and running with code 200
#        response = self.client.get(reverse('tms_timesheet_detail', args=[self.timesheet1.pk]), {})
#        self.failUnlessEqual(response.status_code, 200)
#
#        #check for test model context in response
#        self.assertContains(response, self.timesheet1.comment)
#        print 'tms.timesheet.details test passed...........................................OK'

    def test_expenses_urls(self):
        help = """
        Tests for APP 'tms.views.expenses' basic functiuonality:

        - tries to log in
        - checks 'tms_expenses' view returns response with code 200
        - checks POST to this view returns code 400
        - checks empty POST to this view returns 400 too
        - checks post with right variable returns 200 and redirect to new updated page
        """
        #print help
        #trying to access url of deleting test database entry
        response = self.client.get(reverse('tms_expenses'), {})
        self.failUnlessEqual(response.status_code, 200)

        # faulty post to this page returns normal form/list page
        response = self.client.post(reverse('tms_expenses'), {})
        self.failUnlessEqual(response.status_code, 200)

        #print 'tms.expenses test passed..................................................OK'



    def test_expenses_form(self):
        help = """
        Tests for FORM 'expenses' working check:

        - creates an instance of a form with specified test model
        - tries to compare created instance to original model
        """
        #print help
        form = ExpenseForm(instance=self.expense1)
        self.failUnlessEqual(form.instance.comment, self.expense1.comment)
        #print 'tms.forms.expenses test passed...............................................OK'

    def test_expenses_adding_new_entry_with_form(self):
        help = """
        Tests for APP 'tms.views.expenses' ADDING functiuonality:

        - checks for ability to POST form data to view
        - checks for view returns with code 200 and form with errors
            in response to faulty form POST data
        - checks for valid data posting to view.
            Form should return a valid HttpResponse html data,
            containing rendered current added entry
            checked by part of unique string in entry template
        - checks it does not contain edit string
            required to trigger AXAJ actions of replace
            edited item on JavaScript side.
        """
        #print help

        # trying to post form data to view with bad POST data
        # checking response contains form and
        # error (form errors exist so it should have at least one)
        response = self.client.post(reverse('tms_expenses'), {
                        "currency": "2000", #Invalid form field
                        "expense_date_day": "8",
                        "expense_date_yearmonth": "2011-9",
                        "expense_date_datepicker": "",
                        "claim_date_day": "8",
                        "claim_date_yearmonth": "2011-9",
                        "claim_date_datepicker": "",
                        "customer": "1",
                        "expense_type": "1",
                        "comment": "some test comment test for expenses",
                        "is_receipted": "on",
                        "payment_method": "1",
                        "is_taxable": "on",
                        "expense_amount": "3345",
                        "tax_amount": "23",
                        "local_amount": "3346",
                        "save": "Save",
                        "data_id": "",
                        })
        self.failUnlessEqual(response.status_code, 200)
        self.assertContains(response, 'form')
        self.assertContains(response, 'error')

        # testing valid data posting to view. Form should return
        # a valid HttpResponse html data, containing rendered current added entry
        # by part of unique string in entry
        # checking it does not contain edit string
        # required to trigger AXAJ actions on JavaScript side.
        response = self.client.post(reverse('tms_expenses'), {
                        "currency": "1",
                        "expense_date_day": "8",
                        "expense_date_yearmonth": "2011-9",
                        "expense_date_datepicker": "",
                        "claim_date_day": "8",
                        "claim_date_yearmonth": "2011-9",
                        "claim_date_datepicker": "",
                        "customer": "1",
                        "expense_type": "1",
                        "comment": "some test comment test for expenses",
                        "is_receipted": "on",
                        "payment_method": "1",
                        "is_taxable": "on",
                        "expense_amount": "3345",
                        "tax_amount": "23",
                        "local_amount": "3346",
                        "save": "Save",
                        "data_id": "",
                                                                      })
        self.failUnlessEqual(response.status_code, 200)
        self.assertContains(response, 'return expense_editbtn_press')
        self.assertNotContains(response, 'form')
        self.assertNotContains(response, 'edited_item_returned')
        #print 'tms.expenses adding new entry with form test passed.......................OK'

    def test_expenses_edit_actions(self):
        help = """
        Tests for APP 'tms.views.expenses' EDITING functiuonality:

        - checks for a valid HttpResponse html data,
            containing rendered current added entry
            by part of unique string in entry
            checking it contains edit string
            required to trigger AXAJ EDIT actions on JavaScript side.
        - testing invalid data posting to view.
            View should return form with errors and 200 status
        """
        #print help
        #trying to access url of editing test database entry and get the form
        response = self.client.get(reverse('tms_timesheets'), {})
        self.failUnlessEqual(response.status_code, 200)

        # checks for a valid HttpResponse html data,
        # containing rendered current added entry
        # by part of unique string in entry
        # checking it contains edit string
        # required to trigger AXAJ actions on JavaScript side.
        response = self.client.post(reverse('tms_expenses'), {
                        "currency": "1",
                        "expense_date_day": "8",
                        "expense_date_yearmonth": "2011-9",
                        "expense_date_datepicker": "",
                        "claim_date_day": "8",
                        "claim_date_yearmonth": "2011-9",
                        "claim_date_datepicker": "",
                        "customer": "1",
                        "expense_type": "1",
                        "comment": "some test comment test for expenses",
                        "is_receipted": "on",
                        "payment_method": "1",
                        "is_taxable": "on",
                        "expense_amount": "3345",
                        "tax_amount": "23",
                        "local_amount": "3346",
                        "save": "Save",
                        "data_id": "1",
                                                                  })
        self.failUnlessEqual(response.status_code, 200)
        self.assertContains(response, 'return expense_editbtn_press')
        self.assertNotContains(response, 'form')
        self.assertContains(response, 'edited_item_returned')

        # testing invalid data posting to view.
        # View should return form with errors and 200 status
        response = self.client.post(reverse('tms_expenses'), {
                        "currency": "2000", #faulty data in here
                        "expense_date_day": "8",
                        "expense_date_yearmonth": "2011-9",
                        "expense_date_datepicker": "",
                        "claim_date_day": "8",
                        "claim_date_yearmonth": "2011-9",
                        "claim_date_datepicker": "",
                        "customer": "1",
                        "expense_type": "1",
                        "comment": "some test comment test for expenses",
                        "is_receipted": "on",
                        "payment_method": "1",
                        "is_taxable": "on",
                        "expense_amount": "3345",
                        "tax_amount": "23",
                        "local_amount": "3346",
                        "save": "Save",
                        "data_id": "1",
                                                                  })
        self.failUnlessEqual(response.status_code, 200)
        self.assertContains(response, 'form')
        self.assertContains(response, 'error')
        #print 'tms.expenses.edit test passed..............................................OK'

    def test_expense_del_urls(self):
        help = """
        Tests for APP 'tms.views.timesheet_del' DELETING functiuonality:

        - tries to log in
        - checks 'tms_expense_del' GET to view returns response with code 400
        - checks POST to this view returns code 400
        - checks empty POST to this view returns 400 too
        - checks post with variable returns 200 and desired model PK (for AJAX manipulations)
        """
        #print help
        #trying to access url of deleting test database entry
        response = self.client.get(reverse('tms_expense_del'), {})
        self.failUnlessEqual(response.status_code, 400)

        # empty POST to this view returns 400 too
        response = self.client.post(reverse('tms_expense_del'), {})
        self.failUnlessEqual(response.status_code, 400)

        # post with variable returns 200 and desired model PK (for AJAX manipulations)
        response = self.client.post(reverse('tms_expense_del'), {'data_id': self.expense1.pk})
        self.failUnlessEqual(response.content, str(self.expense1.pk))
        #print 'tms.expense.del test passed...............................................OK'


class ReportsWorking(TestCase):
    """
    Various tests of reports
    """
    def setUp(self):
        """
        Crating a test environment with logged in
        client and at least one timesheet model
        and one Expense and Job models.
        """
        self.client = Client()
        self.client, self.response = client_login(self.client, callback=reverse('tms_timesheets'))
        self.datetime = datetime.datetime.now
        self.user = new_test_user()
        self.job_model = any_model(Job, is_active=True)
        try:
            self.employee = any_model(Employee, user = self.user)
        except:
            #employee with this user already exists
            self.employee = Employee.objects.get(user=self.user)
        self.timesheet1 = any_model(Timesheet,
                                    employee=self.employee,
                                    is_submitted=False,
                                    is_billed=False,
                                    start_time='2011-08-29 20:57:34.848614',
                                    end_time='2011-08-29 22:57:34.848614',
                                    comment='Django_tests comment for timesheet model1')
        self.expense1 = any_model(Expense,
                                  expense_date='2011-09-10',
                                  claim_date='2011-09-10',
                                  is_receipted=True,
                                  is_submitted=False,
                                  is_billed=False,
                                  is_taxable=True,
                                  comment='Django_tests comment for expense model1')
        self.reports_list = reporting.all_reports()

        self.reporting_post_data = { 'consultant': '',
                      'date_end_datepicker' : '',
                      'date_end_day': '13',
                      'date_end_yearmonth': '2011-9',
                      'date_start_datepicker': '',
                      'date_start_day': '16',
                      'date_start_yearmonth': '2011-8',
                      'generate': 'Generate',
                      }

    def test_reports_working(self):
        help = """
        Tests for APP 'reporting' main functionality:

        - loggs in
        - checks 'reports' GET to view returns response with code 200
        - checks for existence of every test url in view response
        - checks for number of reports is greater than 3 (in the time of writing we have 4 reports)
        """
        #print help
        response = self.client.get(reverse('reports'), {})
        self.failUnlessEqual(response.status_code, 200)

        #verifying all reports exist
        for slug, report in self.reports_list:
            self.assertContains(response, slug)

        #checking it has more than 3 reports
        self.assertGreater(self.reports_list.count, 3)
        #print 'reporting.reports test passed...............................................OK'


    def test_report_days_consultant_contains_data(self):
        help = """
        Tests for APP 'report_detail' report 'days_consultant' functionality:

        - loggs in
        - checks 'report_detail' with 'days_consultant' report returns 200 status code
        - checks cotains report test data model comment
        """
        #print help

        response = self.client.get('/reporting/days_consultant/')
        self.failUnlessEqual(response.status_code, 200)


        response = self.client.post('/reporting/days_consultant/', self.reporting_post_data)
        self.assertContains(response, self.timesheet1.comment)
        #print 'reporting.days_consultant test passed......................................OK'

    def test_report_expense_summary_consultant_contains_data(self):
        help = """
        Tests for APP 'report_detail' report 'expense_summary_consultant' functionality:

        - loggs in
        - checks 'report_detail' with 'expense_summary_consultant' report returns 200 status code
        - checks cotains report test data model comment
        """
        #print help

        response = self.client.get('/reporting/expense_summary_consultant/')
        self.failUnlessEqual(response.status_code, 200)

        response = self.client.post('/reporting/expense_summary_consultant/', self.reporting_post_data)
        self.assertContains(response, self.expense1.comment)
        #print 'reporting.expense_summary_consultant test passed...........................OK'

    def test_report_expense_summary_client_contains_data(self):
        help = """
        Tests for APP 'report_detail' report 'expense_summary_client' functionality:

        - loggs in
        - checks 'report_detail' with 'expense_summary_client' report returns 200 status code
        - checks cotains report test data model comment
        """
        #print help

        response = self.client.get('/reporting/expense_summary_client/')
        self.failUnlessEqual(response.status_code, 200)

        response = self.client.post('/reporting/expense_summary_client/', self.reporting_post_data)
        self.assertContains(response, self.expense1.comment)
        #print 'reporting.expense_summary_client test passed...............................OK'

    def test_report_project_details_contains_data(self):
        help = """
        Tests for APP 'report_detail' report 'project_details' functionality:

        - loggs in
        - checks 'report_detail' with 'project_details' report returns 200 status code
        - checks cotains report test data model comment
        """
        #print help

        response = self.client.get('/reporting/project_details/')
        self.failUnlessEqual(response.status_code, 200)


        response = self.client.post('/reporting/project_details/', self.reporting_post_data)
        self.assertContains(response, self.timesheet1.comment)
        #print 'reporting.project_details test passed......................................OK'


