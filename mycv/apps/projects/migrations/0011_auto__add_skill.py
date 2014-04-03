# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Skill'
        db.create_table(u'projects_skill', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.TextField')(default='', max_length=500, blank=True)),
        ))
        db.send_create_signal(u'projects', ['Skill'])


    def backwards(self, orm):
        # Deleting model 'Skill'
        db.delete_table(u'projects_skill')


    models = {
        u'projects.client': {
            'Meta': {'ordering': "('order_index', '-end_date')", 'object_name': 'Client'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '2000'}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_draft': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'order_index': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'title': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'website': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '200', 'blank': 'True'})
        },
        u'projects.clientobjective': {
            'Meta': {'object_name': 'ClientObjective'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'objectives'", 'to': u"orm['projects.Client']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order_index': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'projects.project': {
            'Meta': {'ordering': "('order_index',)", 'object_name': 'Project'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'projects'", 'null': 'True', 'to': u"orm['projects.Client']"}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '2000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_draft': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'order_index': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'source_url': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'stack_items': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['projects.StackItem']", 'symmetrical': 'False'})
        },
        u'projects.projectfeature': {
            'Meta': {'object_name': 'ProjectFeature'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'features'", 'to': u"orm['projects.Project']"})
        },
        u'projects.skill': {
            'Meta': {'object_name': 'Skill'},
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '500', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'projects.stackitem': {
            'Meta': {'object_name': 'StackItem'},
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['projects']