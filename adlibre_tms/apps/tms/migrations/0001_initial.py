# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Employee'
        db.create_table('tms_employee', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
        ))
        db.send_create_signal('tms', ['Employee'])

        # Adding model 'Project'
        db.create_table('tms_project', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64)),
            ('project_code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32)),
            ('is_billable', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('tms', ['Project'])

        # Adding model 'Customer'
        db.create_table('tms_customer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('customer_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64)),
            ('customer_code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32)),
            ('is_billable', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('saasu_contact_uid', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
        ))
        db.send_create_signal('tms', ['Customer'])

        # Adding model 'Service'
        db.create_table('tms_service', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('service_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64)),
            ('service_code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32)),
            ('is_billable', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('saasu_item_uid', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
        ))
        db.send_create_signal('tms', ['Service'])

        # Adding model 'Job'
        db.create_table('tms_job', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tms.Customer'])),
            ('service', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tms.Service'])),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tms.Project'])),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('tms', ['Job'])

        # Adding model 'Timesheet'
        db.create_table('tms_timesheet', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('employee', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tms.Employee'])),
            ('job', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tms.Job'])),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('is_submitted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_billed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('tms', ['Timesheet'])

        # Adding model 'ExpenseType'
        db.create_table('tms_expensetype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('expense_type_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64)),
            ('expense_type_code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32)),
            ('saasu_account_uid', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
        ))
        db.send_create_signal('tms', ['ExpenseType'])

        # Adding model 'PaymentMethod'
        db.create_table('tms_paymentmethod', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('payment_method_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64)),
            ('payment_method_code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32)),
        ))
        db.send_create_signal('tms', ['PaymentMethod'])

        # Adding model 'Currency'
        db.create_table('tms_currency', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('currency_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64)),
            ('currency_code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32)),
            ('currency_symbol', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('tms', ['Currency'])

        # Adding model 'Expense'
        db.create_table('tms_expense', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('employee', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tms.Employee'])),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tms.Customer'])),
            ('expense_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tms.ExpenseType'])),
            ('payment_method', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tms.PaymentMethod'])),
            ('currency', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tms.Currency'])),
            ('is_receipted', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_submitted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_billed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_taxable', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('expense_amount', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('local_amount', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('tax_amount', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('expense_date', self.gf('django.db.models.fields.DateField')()),
            ('claim_date', self.gf('django.db.models.fields.DateField')()),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('tms', ['Expense'])

        # Adding model 'BillingRecurrence'
        db.create_table('tms_billingrecurrence', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('job', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tms.Job'], unique=True)),
            ('recurrence', self.gf('recurrence.fields.RecurrenceField')()),
        ))
        db.send_create_signal('tms', ['BillingRecurrence'])

        # Adding model 'RetainerRecurrence'
        db.create_table('tms_retainerrecurrence', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('job', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tms.Job'])),
            ('amount', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('start', self.gf('django.db.models.fields.DateField')()),
            ('end', self.gf('django.db.models.fields.DateField')()),
            ('recurrence', self.gf('recurrence.fields.RecurrenceField')()),
        ))
        db.send_create_signal('tms', ['RetainerRecurrence'])

        # Adding model 'Retainer'
        db.create_table('tms_retainer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('job', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tms.Job'])),
            ('start', self.gf('django.db.models.fields.DateField')()),
            ('end', self.gf('django.db.models.fields.DateField')()),
            ('amount', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('amount_used', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('tms', ['Retainer'])

        # Adding model 'TimesheetRetainerAllocation'
        db.create_table('tms_timesheetretainerallocation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timesheet', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tms.Timesheet'])),
            ('retainer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tms.Retainer'])),
            ('is_billed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('tms', ['TimesheetRetainerAllocation'])

        # Adding unique constraint on 'TimesheetRetainerAllocation', fields ['timesheet', 'retainer']
        db.create_unique('tms_timesheetretainerallocation', ['timesheet_id', 'retainer_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'TimesheetRetainerAllocation', fields ['timesheet', 'retainer']
        db.delete_unique('tms_timesheetretainerallocation', ['timesheet_id', 'retainer_id'])

        # Deleting model 'Employee'
        db.delete_table('tms_employee')

        # Deleting model 'Project'
        db.delete_table('tms_project')

        # Deleting model 'Customer'
        db.delete_table('tms_customer')

        # Deleting model 'Service'
        db.delete_table('tms_service')

        # Deleting model 'Job'
        db.delete_table('tms_job')

        # Deleting model 'Timesheet'
        db.delete_table('tms_timesheet')

        # Deleting model 'ExpenseType'
        db.delete_table('tms_expensetype')

        # Deleting model 'PaymentMethod'
        db.delete_table('tms_paymentmethod')

        # Deleting model 'Currency'
        db.delete_table('tms_currency')

        # Deleting model 'Expense'
        db.delete_table('tms_expense')

        # Deleting model 'BillingRecurrence'
        db.delete_table('tms_billingrecurrence')

        # Deleting model 'RetainerRecurrence'
        db.delete_table('tms_retainerrecurrence')

        # Deleting model 'Retainer'
        db.delete_table('tms_retainer')

        # Deleting model 'TimesheetRetainerAllocation'
        db.delete_table('tms_timesheetretainerallocation')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'tms.billingrecurrence': {
            'Meta': {'ordering': "['job']", 'object_name': 'BillingRecurrence'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tms.Job']", 'unique': 'True'}),
            'recurrence': ('recurrence.fields.RecurrenceField', [], {})
        },
        'tms.currency': {
            'Meta': {'ordering': "['currency_name']", 'object_name': 'Currency'},
            'currency_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'currency_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'currency_symbol': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'tms.customer': {
            'Meta': {'ordering': "['customer_name']", 'object_name': 'Customer'},
            'customer_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'customer_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_billable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'saasu_contact_uid': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'})
        },
        'tms.employee': {
            'Meta': {'ordering': "['user']", 'object_name': 'Employee'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'tms.expense': {
            'Meta': {'object_name': 'Expense'},
            'claim_date': ('django.db.models.fields.DateField', [], {}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tms.Currency']"}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tms.Customer']"}),
            'employee': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tms.Employee']"}),
            'expense_amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'expense_date': ('django.db.models.fields.DateField', [], {}),
            'expense_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tms.ExpenseType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_billed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_receipted': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_submitted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_taxable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'local_amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'payment_method': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tms.PaymentMethod']"}),
            'tax_amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'tms.expensetype': {
            'Meta': {'ordering': "['expense_type_name']", 'object_name': 'ExpenseType'},
            'expense_type_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'expense_type_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'saasu_account_uid': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'})
        },
        'tms.job': {
            'Meta': {'ordering': "['customer', 'service', 'project']", 'object_name': 'Job'},
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tms.Customer']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tms.Project']"}),
            'service': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tms.Service']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'tms.paymentmethod': {
            'Meta': {'ordering': "['payment_method_name']", 'object_name': 'PaymentMethod'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'payment_method_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'payment_method_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'})
        },
        'tms.project': {
            'Meta': {'ordering': "['project_name']", 'object_name': 'Project'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_billable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'project_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'project_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'})
        },
        'tms.retainer': {
            'Meta': {'ordering': "['job']", 'object_name': 'Retainer'},
            'amount': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'amount_used': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'end': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tms.Job']"}),
            'start': ('django.db.models.fields.DateField', [], {})
        },
        'tms.retainerrecurrence': {
            'Meta': {'ordering': "['job']", 'object_name': 'RetainerRecurrence'},
            'amount': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'end': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tms.Job']"}),
            'recurrence': ('recurrence.fields.RecurrenceField', [], {}),
            'start': ('django.db.models.fields.DateField', [], {})
        },
        'tms.service': {
            'Meta': {'ordering': "['service_name']", 'object_name': 'Service'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_billable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'saasu_item_uid': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'service_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'service_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'})
        },
        'tms.timesheet': {
            'Meta': {'ordering': "('start_time',)", 'object_name': 'Timesheet'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'employee': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tms.Employee']"}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_billed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_submitted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'job': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tms.Job']"}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'tms.timesheetretainerallocation': {
            'Meta': {'ordering': "['timesheet', 'retainer']", 'unique_together': "(('timesheet', 'retainer'),)", 'object_name': 'TimesheetRetainerAllocation'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_billed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'retainer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tms.Retainer']"}),
            'timesheet': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tms.Timesheet']"})
        }
    }

    complete_apps = ['tms']