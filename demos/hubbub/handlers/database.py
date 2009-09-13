import simplejson

from django.contrib.auth.models import User

from messaging.models import Message

from hurricane.handlers.base import PureConsumeHandler

class DatabaseHandler(PureConsumeHandler):
    def receive(self, msg):
        dct = msg._asdict()
        user_id = dct['raw_data'].get('user', 1) # TODO: Remove this default user
        dct['user'] = User.objects.get(id=user_id)
        dct['raw_data'] = simplejson.dumps(dct['raw_data'])
        Message.objects.create(**dct)