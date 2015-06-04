# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'XeroExpenseClaim'
        db.create_table('xero_client_xeroexpenseclaim', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('xero_sync', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('to', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('summary', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal('xero_client', ['XeroExpenseClaim'])

        # Adding M2M table for field items on 'XeroExpenseClaim'
        m2m_table_name = db.shorten_name('xero_client_xeroexpenseclaim_items')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('xeroexpenseclaim', models.ForeignKey(orm['xero_client.xeroexpenseclaim'], null=False)),
            ('expense', models.ForeignKey(orm['tms.expense'], null=False))
        ))
        db.create_unique(m2m_table_name, ['xeroexpenseclaim_id', 'expense_id'])

        # Adding model 'XeroItemList'
        db.create_table('xero_client_xeroitemlist', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('xero_client', ['XeroItemList'])

        # Adding model 'XeroAccountList'
        db.create_table('xero_client_xeroaccountlist', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('xero_client', ['XeroAccountList'])

        # Adding model 'XeroContactList'
        db.create_table('xero_client_xerocontactlist', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('xero_client', ['XeroContactList'])


    def backwards(self, orm):
        # Deleting model 'XeroExpenseClaim'
        db.delete_table('xero_client_xeroexpenseclaim')

        # Removing M2M table for field items on 'XeroExpenseClaim'
        db.delete_table(db.shorten_name('xero_client_xeroexpenseclaim_items'))

        # Deleting model 'XeroItemList'
        db.delete_table('xero_client_xeroitemlist')

        # Deleting model 'XeroAccountList'
        db.delete_table('xero_client_xeroaccountlist')

        # Deleting model 'XeroContactList'
        db.delete_table('xero_client_xerocontactlist')


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
            'saasu_account_uid': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'xero_account_id': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'})
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
        'xero_client.xeroaccountlist': {
            'Meta': {'object_name': 'XeroAccountList'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'xero_client.xerocontactlist': {
            'Meta': {'object_name': 'XeroContactList'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'xero_client.xeroexpenseclaim': {
            'Meta': {'object_name': 'XeroExpenseClaim'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'items': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['tms.Expense']", 'symmetrical': 'False'}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'to': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'xero_sync': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'xero_client.xeroinvoice': {
            'Meta': {'object_name': 'XeroInvoice'},
            'due_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2015, 6, 7, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2015, 6, 2, 0, 0)'}),
            'items': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['tms.Timesheet']", 'symmetrical': 'False'}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'to': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'xero_sync': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'xero_client.xeroitemlist': {
            'Meta': {'object_name': 'XeroItemList'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['xero_client']