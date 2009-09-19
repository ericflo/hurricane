from datetime import datetime
import threading

import os

import simplejson

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

from hurricane.handlers.base import BaseHandler
from hurricane.base import Message
from hurricane.utils import HttpResponse, json_timestamp
from hurricane.handlers.comet import views

GLOBAL_MEDIA_ROOT = os.path.join(os.path.dirname(__file__), '..', '..', 'media')

class CometHandler(BaseHandler):
    """
    The following methods can be overidden in subclasses:
        * defer_message(for_users, msg, seen_users)
        * messages_for
        * id_for_request
    """
    def initialize(self):
        self.requests = {}
        self.server = HTTPServer(self.handle_request)
        self.server.listen(self.settings.COMET_PORT)
        self.thread = threading.Thread(target=IOLoop.instance().start).start()
        self.urls = self.get_urls()

    def receive(self, msg):
        msg = msg._asdict()
        msg.update({
            'timestamp': json_timestamp(msg.pop('timestamp')),
        })
        for_users = msg.pop('for')
        if for_users is None:
            # this means send to all users
            sent_to = set()
            for request_id, request in self.requests.iteritems():
                if request_id in sent_to:
                    continue
                sent_to.add(request_id)
                request.write(HttpResponse(200, 'application/json', 
                    simplejson.dumps({'messages': [msg]})))
                request.finish()
            # defer the message, but mark people that shouldn't be resent
            self.defer_message(None, msg, seen_users=sent_to)
        else:
            # for_users is a list of user ids to send the message to, let's do 
            # that now
            for user in for_users:
                if user in self.requests:
                    request = self.requests[user]
                    request.write(HttpResponse(200, 'application/json',
                        simplejson.dumps({'messages': [msg]})))
                    request.finish()
                else:
                    # the user isn't here, defer the message for them
                    self.defer_message(user, msg)

    def get_urls(self):
        return (
            ('/comet/', self.comet_view),
            ('/global/', views.get_media_view(GLOBAL_MEDIA_ROOT, '/global/')),
            ('/', views.get_media_view(self.settings.MEDIA_ROOT, '/')),
        )

    def handle_request(self, request):
        for url, view in self.urls:
            if request.path.startswith(url):
                return view(request)
        request.write(HttpResponse(404).as_bytes())
        request.finish()

    def comet_view(self, request):
        if request.method == 'POST':
            self.publish(Message('comet', datetime.now(),
                simplejson.loads(request.body)))
            request.write(HttpResponse(201).as_bytes())
            request.finish()
        else:
            existing_messages = self.messages_for(request)
            if existing_messages:
                request.write(HttpResponse(200, 'applicaiton/json', 
                    simplejson.dumps({'messages': existing_messages})))
                request.finish()
                return
            self.requests[self.id_for_request(request)] = request
