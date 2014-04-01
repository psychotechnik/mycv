# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'StackItem'
        db.create_table(u'projects_stackitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')(default='', max_length=250, blank=True)),
        ))
        db.send_create_signal(u'projects', ['StackItem'])

        # Adding model 'ProjectFeature'
        db.create_table(u'projects_projectfeature', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['projects.Project'])),
        ))
        db.send_create_signal(u'projects', ['ProjectFeature'])

        # Adding M2M table for field stack_items on 'Project'
        m2m_table_name = db.shorten_name(u'projects_project_stack_items')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm[u'projects.project'], null=False)),
            ('stackitem', models.ForeignKey(orm[u'projects.stackitem'], null=False))
        ))
        db.create_unique(m2m_table_name, ['project_id', 'stackitem_id'])


    def backwards(self, orm):
        # Deleting model 'StackItem'
        db.delete_table(u'projects_stackitem')

        # Deleting model 'ProjectFeature'
        db.delete_table(u'projects_projectfeature')

        # Removing M2M table for field stack_items on 'Project'
        db.delete_table(db.shorten_name(u'projects_project_stack_items'))


    models = {
        u'projects.project': {
            'Meta': {'object_name': 'Project'},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '2000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_draft': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'stack_items': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['projects.StackItem']", 'symmetrical': 'False'})
        },
        u'projects.projectfeature': {
            'Meta': {'object_name': 'ProjectFeature'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['projects.Project']"})
        },
        u'projects.stackitem': {
            'Meta': {'object_name': 'StackItem'},
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['projects']