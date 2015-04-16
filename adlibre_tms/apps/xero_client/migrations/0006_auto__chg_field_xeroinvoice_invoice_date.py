# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding M2M table for field items on 'XeroInvoice'
        m2m_table_name = db.shorten_name('xero_client_xeroinvoice_items')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('xeroinvoice', models.ForeignKey(orm['xero_client.xeroinvoice'], null=False)),
            ('timesheet', models.ForeignKey(orm['tms.timesheet'], null=False))
        ))
        db.create_unique(m2m_table_name, ['xeroinvoice_id', 'timesheet_id'])


        # Changing field 'XeroInvoice.invoice_date'
        db.alter_column('xero_client_xeroinvoice', 'invoice_date', self.gf('django.db.models.fields.DateField')())

    def backwards(self, orm):
        # Removing M2M table for field items on 'XeroInvoice'
        db.delete_table(db.shorten_name('xero_client_xeroinvoice_items'))


        # Changing field 'XeroInvoice.invoice_date'
        db.alter_column('xero_client_xeroinvoice', 'invoice_date', self.gf('django.db.models.fields.DateField')(auto_now_add=True))

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
        'tms.job': {
            'Meta': {'ordering': "['customer', 'service', 'project']", 'object_name': 'Job'},
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tms.Customer']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tms.Project']"}),
            'service': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tms.Service']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
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
        'xero_client.xeroinvoice': {
            'Meta': {'object_name': 'XeroInvoice'},
            'due_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2015, 4, 20, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2015, 4, 15, 0, 0)'}),
            'items': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['tms.Timesheet']", 'symmetrical': 'False'}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'to': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'xero_sync': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        }
    }

    complete_apps = ['xero_client']