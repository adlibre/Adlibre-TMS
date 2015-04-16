# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'XeroInvoice.date'
        db.delete_column('xero_client_xeroinvoice', 'date')

        # Adding field 'XeroInvoice.invoice_date'
        db.add_column('xero_client_xeroinvoice', 'invoice_date',
                      self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2015, 4, 15, 0, 0), auto_now_add=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'XeroInvoice.date'
        raise RuntimeError("Cannot reverse this migration. 'XeroInvoice.date' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'XeroInvoice.date'
        db.add_column('xero_client_xeroinvoice', 'date',
                      self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True),
                      keep_default=False)

        # Deleting field 'XeroInvoice.invoice_date'
        db.delete_column('xero_client_xeroinvoice', 'invoice_date')


    models = {
        'xero_client.xeroinvoice': {
            'Meta': {'object_name': 'XeroInvoice'},
            'due_date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2015, 4, 15, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'to': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'xero_sync': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        }
    }

    complete_apps = ['xero_client']