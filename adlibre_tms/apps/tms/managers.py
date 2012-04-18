from django.db import models

__all__ = ['TimesheetManager', 'ExpenseManager']


class TimesheetManager(models.Manager):
    """ Custom model manager for Timesheet model """

    def get_query_set(self):
        return self.model.QuerySet(self.model)

    def __getattr__(self, attr, *args):
        return getattr(self.get_query_set(), attr, *args)


class ExpenseManager(models.Manager):
    """ Custom model manager for Expense model """

    def get_query_set(self):
        return self.model.QuerySet(self.model)

    def __getattr__(self, attr, *args):
        return getattr(self.get_query_set(), attr, *args)

