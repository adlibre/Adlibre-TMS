from django.contrib import admin

from tms.models import *
from tms.forms import ExpenseTypeAdminForm, CustomerAdminForm, ServiceAdminForm


class TimesheetAdmin(admin.ModelAdmin):
    list_display = ('employee', 'job', 'start_time', 'end_time', 'comment', 'is_submitted', 'is_billed')
    list_filter = ('employee', 'job', 'is_submitted', 'is_billed')
    actions = ['saasu_export_selected', 'mark_as_billed', 'mark_as_submitted', 'unmark_as_billed', 'unmark_as_submitted']

    def saasu_export_selected(self, request, queryset):
        # TODO: Add intermediate page / view
        rows_exported = queryset.filter(is_submitted=True, is_billed=False).saasu_export()
        try:
            int(rows_exported)
            if rows_exported == 1:
                message_bit = "1 timesheet was"
            elif rows_exported == 0:
                return self.message_user(request, "0 timesheets were successfully exported. (Must be marked as is_submitted to export)")
            else:
                message_bit = "%s timesheets were" % rows_exported
            self.message_user(request, "%s successfully exported." % message_bit)
        except:
            self.message_user(request, rows_exported)

    saasu_export_selected.short_description = "Export selected timesheets as SAASU Sale Items"

    def mark_as_billed(self, request, queryset):
        rows_updated = queryset.update(is_billed=True)
        if rows_updated == 1:
            message_bit = "1 timesheet was"
        else:
            message_bit = "%s timesheets were" % rows_updated
        self.message_user(request, "%s successfully updated." % message_bit)
    mark_as_billed.short_description = 'MARK selected timesheets as Billed'

    def unmark_as_billed(self, request, queryset):
        rows_updated = queryset.update(is_billed=False)
        if rows_updated == 1:
            message_bit = "1 timesheet was"
        else:
            message_bit = "%s timesheets were" % rows_updated
        self.message_user(request, "%s successfully updated." % message_bit)
    unmark_as_billed.short_description = 'UNMARK selected timesheets as Billed'

    def mark_as_submitted(self, request, queryset):
        rows_updated = queryset.update(is_submitted=True)
        if rows_updated == 1:
            message_bit = "1 timesheet was"
        else:
            message_bit = "%s timesheets were" % rows_updated
        self.message_user(request, "%s successfully updated." % message_bit)
    mark_as_submitted.short_description = "MARK selected timesheets as Submitted"

    def unmark_as_submitted(self, request, queryset):
        rows_updated = queryset.update(is_submitted=False)
        if rows_updated == 1:
            message_bit = "1 timesheet was"
        else:
            message_bit = "%s timesheets were" % rows_updated
        self.message_user(request, "%s successfully updated." % message_bit)
    unmark_as_submitted.short_description = "UNMARK selected timesheets as Submitted"

admin.site.register(Timesheet, TimesheetAdmin)


class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('employee', 'customer', 'expense_type', 'payment_method', 'currency', 'expense_date', 'claim_date', 'comment', 'is_submitted', 'is_billed')
    list_filter = ('employee', 'customer', 'is_submitted', 'is_billed')
    actions = ['saasu_export_selected', 'mark_as_billed', 'mark_as_submitted', 'unmark_as_billed', 'unmark_as_submitted']

    def saasu_export_selected(self, request, queryset):
        # TODO: Add intermediate page / view
        rows_exported = queryset.filter(is_submitted=True, is_billed=False).saasu_export()
        try:
            int(rows_exported)
            if rows_exported == 1:
                message_bit = "1 expense was"
            elif rows_exported == 0:
                return self.message_user(request, "0 expenses were successfully exported. (Must be marked as is_submitted to export)")
            else:
                message_bit = "%s expenses were" % rows_exported
            self.message_user(request, "%s successfully exported." % message_bit)
        except:
            self.message_user(request, rows_exported)
    saasu_export_selected.short_description = "Export selected expenses as SAASU Purchase Items"

    def mark_as_billed(self, request, queryset):
        rows_updated = queryset.update(is_billed=True)
        if rows_updated == 1:
            message_bit = "1 timesheet was"
        else:
            message_bit = "%s timesheets were" % rows_updated
        self.message_user(request, "%s successfully updated." % message_bit)
    mark_as_billed.short_description = 'MARK selected expenses as Billed'

    def unmark_as_billed(self, request, queryset):
        rows_updated = queryset.update(is_billed=False)
        if rows_updated == 1:
            message_bit = "1 timesheet was"
        else:
            message_bit = "%s timesheets were" % rows_updated
        self.message_user(request, "%s successfully updated." % message_bit)
    unmark_as_billed.short_description = 'UNMARK selected expenses as Billed'

    def mark_as_submitted(self, request, queryset):
        rows_updated = queryset.update(is_submitted=True)
        if rows_updated == 1:
            message_bit = "1 timesheet was"
        else:
            message_bit = "%s timesheets were" % rows_updated
        self.message_user(request, "%s successfully updated." % message_bit)
    mark_as_submitted.short_description = "MARK selected expenses as Submitted"

    def unmark_as_submitted(self, request, queryset):
        rows_updated = queryset.update(is_submitted=False)
        if rows_updated == 1:
            message_bit = "1 timesheet was"
        else:
            message_bit = "%s timesheets were" % rows_updated
        self.message_user(request, "%s successfully updated." % message_bit)
    unmark_as_submitted.short_description = "UNMARK selected expenses as Submitted"

admin.site.register(Expense, ExpenseAdmin)


class CustomerAdmin(admin.ModelAdmin):
    form = CustomerAdminForm

admin.site.register(Customer, CustomerAdmin)


class ServiceAdmin(admin.ModelAdmin):
    form = ServiceAdminForm

admin.site.register(Service, ServiceAdmin)

admin.site.register(Project)
admin.site.register(Employee)
admin.site.register(Job)


class ExpenseTypeAdmin(admin.ModelAdmin):
    form = ExpenseTypeAdminForm

admin.site.register(ExpenseType, ExpenseTypeAdmin)

admin.site.register(PaymentMethod)
admin.site.register(Currency)
