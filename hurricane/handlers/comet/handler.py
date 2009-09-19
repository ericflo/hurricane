from datetime import datetime
import Cookie # TODO: Swap this out for better cookie parsing
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
        if msg['kind'] == 'comet-response':
            # If the message is a response provided by a dedicated handler,
            # then we can assume a basic structure and use that to respond
            to_ids = msg['raw_data'].pop('to_ids')
            for session_key in to_ids:
                if session_key not in self.requests:
                    continue
                request = self.requests.pop(session_key)
                request.write(HttpResponse(200, 'application/json',
                    simplejson.dumps(msg)).as_bytes())
                request.finish()
        else:
            # If we're listening to another message that gets sent, we have to
            # assume that we should send it to everyone.
            requests = self.requests
            self.requests = []
            for request in requests:
                request.write(HttpResponse(200, 'application/json',
                    simplejson.dumps(msg)).as_bytes())
                request.finish()

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
        """
        This is dumb function, it just passes everything it gets into the
        message stream.  Something else in the stream should be responsible
        for asynchronously figuring out what to do with all these messages.
        """
        data = {
            'body': simplejson.loads(request.body),
            'headers': request.headers,
            'arguments': request.arguments,
        }
        message_kind = 'comet-%s' % (request.method,)
        self.publish(Message(message_kind, datetime.now(), data))
        if request.method == 'POST':
            request.write(HttpResponse(201).as_bytes())
            request.finish()
        else:
            request_id = self.id_for_request(request)
            if request_id:
                self.requests[request_id] = request
            else:
                request.write(HttpResponse(200).as_bytes())
                request.finish()

    def id_for_request(self, request):
        session_id = ''
        if 'Cookie' in request.headers:
            cookies = Cookie.BaseCookie()
            cookies.load(request.headers['Cookie'])
            if 'sessionid' in cookies:
                session_id = cookies['sessionid'].value
        return session_id