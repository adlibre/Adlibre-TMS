# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'XeroInvoice'
        db.create_table('xero_client_xeroinvoice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('to', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('due_date', self.gf('django.db.models.fields.DateField')()),
            ('invoice_no', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('reference', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal('xero_client', ['XeroInvoice'])


    def backwards(self, orm):
        # Deleting model 'XeroInvoice'
        db.delete_table('xero_client_xeroinvoice')


    models = {
        'xero_client.xeroinvoice': {
            'Meta': {'object_name': 'XeroInvoice'},
            'date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'due_date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice_no': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'to': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['xero_client']