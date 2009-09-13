from datetime import datetime
import threading
import uuid

import os
from Queue import Queue, Empty

import simplejson

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

from hurricane.handlers.base import BaseHandler
from hurricane.base import Message
from hurricane.utils import RingBuffer, HttpResponse, json_timestamp
from hurricane.handlers.comet import views
from hurricane.handlers.comet.request import Request

GLOBAL_MEDIA_ROOT = os.path.join(os.path.dirname(__file__), '..', '..', 'media')

class CometHandler(BaseHandler):
    def initialize(self):
        self.requests = Queue(0)
        self.server = HTTPServer(self.handle_request)
        self.server.listen(self.settings.COMET_PORT)
        self.thread = threading.Thread(target=IOLoop.instance().start).start()
        self.messages = RingBuffer(self.settings.COMET_CACHE_SIZE)
        self.urls = self.get_urls()

    def receive(self, msg):
        msg = msg._asdict()
        msg.update({
            'id': str(uuid.uuid4()),
            'timestamp': json_timestamp(msg.pop('timestamp')),
        })
        self.messages.append(msg)
        self.respond_to_requests()

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
        
    ### THE BELOW HAVE A BAD ABSTRACTION
    ### TODO: Fix the abstraction

    def comet_view(self, request):
        if request.method == 'POST':
            self.publish(Message('comet', datetime.now(),
                simplejson.loads(request.body)))
            request.write(HttpResponse(201).as_bytes())
            request.finish()
        else:
            cursor = request.arguments.get('cursor', [None])[0]
            if cursor == 'null' and len(self.messages) > 0:
                self.respond_to_request(request)
            else:
                self.requests.put(request)

    def respond_to_request(self, request):
        cursor = request.arguments.get('cursor', [None])[0]
        messages = list(self.messages.after_match(lambda x: x['id'] == cursor,
                                                  full_fallback=True))
        json = simplejson.dumps({'messages': messages})
        response = HttpResponse(200, 'application/json', json)
        try:
            request.write(response.as_bytes())
        except IOError:
            return
        request.finish()

    def respond_to_requests(self):
        while True:
            try:
                request = self.requests.get(block=False)
            except Empty:
                return
            self.respond_to_request(request)
