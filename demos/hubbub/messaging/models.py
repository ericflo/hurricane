import datetime

import simplejson

from django.db import models

from django.contrib.auth.models import User

class Message(models.Model):
    kind = models.CharField(max_length=20)
    user = models.ForeignKey(User, related_name='messages')
    timestamp = models.DateTimeField(default=datetime.datetime.now)
    raw_data = models.TextField()
    
    @property
    def data(self):
        return simplejson.loads(self.raw_data)
    
    def __unicode__(self):
        return self.raw_data