
from south.db import db
from django.db import models
from socialgraph.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'UserLink'
        db.create_table('socialgraph_userlink', (
            ('id', models.AutoField(primary_key=True)),
            ('from_user', models.ForeignKey(orm['auth.User'], related_name='following_set')),
            ('to_user', models.ForeignKey(orm['auth.User'], related_name='follower_set')),
            ('date_added', models.DateTimeField(default=datetime.datetime.now)),
        ))
        db.send_create_signal('socialgraph', ['UserLink'])
        
        # Creating unique_together for [to_user, from_user] on UserLink.
        db.create_unique('socialgraph_userlink', ['to_user_id', 'from_user_id'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'UserLink'
        db.delete_table('socialgraph_userlink')
        
        # Deleting unique_together for [to_user, from_user] on UserLink.
        db.delete_unique('socialgraph_userlink', ['to_user_id', 'from_user_id'])
        
    
    
    models = {
        'auth.user': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'socialgraph.userlink': {
            'Meta': {'unique_together': "(('to_user','from_user'),)"},
            'date_added': ('models.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'from_user': ('models.ForeignKey', ["orm['auth.User']"], {'related_name': "'following_set'"}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'to_user': ('models.ForeignKey', ["orm['auth.User']"], {'related_name': "'follower_set'"})
        }
    }
    
    complete_apps = ['socialgraph']
