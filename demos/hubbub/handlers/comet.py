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

class CometHandler(BaseHandler):
    def initialize(self):
        self.requests = Queue(0)
        self.server = HTTPServer(self.handle_request)
        self.server.listen(self.settings.COMET_PORT)
        self.thread = threading.Thread(target=IOLoop.instance().start).start()
        self.messages = RingBuffer(200) # TODO: REPLACE THIS WITH A DIFFERENT MECHANISM

    def receive(self, msg):
        msg = msg._asdict()
        msg.update({
            'id': str(uuid.uuid4()),
            'timestamp': json_timestamp(msg.pop('timestamp')),
        })
        self.messages.append(msg)
        self.respond_to_requests()

    def handle_request(self, request):
        if request.method == 'POST':
            self.publish(Message('hubbub', datetime.now(),
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
