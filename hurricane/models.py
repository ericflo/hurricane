from datetime import datetime

from django.db import models
from django.utils import simplejson

class Item(models.Model):
    kind = models.CharField(max_length=20)
    timestamp = models.DateTimeField(default=datetime.now)
    raw_data = models.TextField()
    
    @property
    def data(self):
        return simplejson.loads(self.raw_data)
