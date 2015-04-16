# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'XeroInvoice.reference'
        db.delete_column('xero_client_xeroinvoice', 'reference')

        # Adding field 'XeroInvoice.summary'
        db.add_column('xero_client_xeroinvoice', 'summary',
                      self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'XeroInvoice.reference'
        db.add_column('xero_client_xeroinvoice', 'reference',
                      self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True),
                      keep_default=False)

        # Deleting field 'XeroInvoice.summary'
        db.delete_column('xero_client_xeroinvoice', 'summary')


    models = {
        'xero_client.xeroinvoice': {
            'Meta': {'object_name': 'XeroInvoice'},
            'date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'due_date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'to': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'xero_sync': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        }
    }

    complete_apps = ['xero_client']