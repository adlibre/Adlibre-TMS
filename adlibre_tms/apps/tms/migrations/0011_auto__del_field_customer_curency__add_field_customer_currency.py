# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Customer.curency'
        db.delete_column('tms_customer', 'curency_id')

        # Adding field 'Customer.currency'
        db.add_column('tms_customer', 'currency',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tms.Currency'], null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Customer.curency'
        db.add_column('tms_customer', 'curency',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tms.Currency'], null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Customer.currency'
        db.delete_column('tms_customer', 'currency_id')


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
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tms.Currency']", 'null': 'True', 'blank': 'True'}),
            'customer_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'customer_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_billable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'saasu_contact_uid': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'xero_contact_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'})
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
            'service_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'xero_item_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'})
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