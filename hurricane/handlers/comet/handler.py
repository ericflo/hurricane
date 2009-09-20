from datetime import datetime
import threading

import os
from Queue import Queue, Empty

import simplejson

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

from hurricane.handlers.base import BaseHandler
from hurricane.base import Message
from hurricane.utils import RingBuffer, HttpResponse, json_timestamp
from hurricane.handlers.comet import views
from hurricane.handlers.comet.utils import parse_cookie

GLOBAL_MEDIA_ROOT = os.path.join(os.path.dirname(__file__), '..', '..', 'media')

class CometHandler(BaseHandler):
    """
    This is the basic class for writing comet applications.
    """
    
    def auto_subscribe(self, app_manager):
        """
        We override this method because we don't want to receive our own
        messages.  To accomplish this, we add a conditional that prevents us
        from subscribing to our own channel.
        """
        for handler in app_manager.handler_classes:
            if handler.channel() != self.channel():
                app_manager.subscribe(handler.channel(), self)
    
    def initialize(self):
        self.requests = {}
        self.pending_requests = self.requests
        self.server = HTTPServer(self.handle_request)
        self.server.listen(self.settings.COMET_PORT)
        self.thread = threading.Thread(target=IOLoop.instance().start).start()
        self.urls = self.get_urls()
        self.post_init()

    def receive(self, msg):
        msg = msg._asdict()
        msg.update({
            'timestamp': json_timestamp(msg.pop('timestamp')),
        })
        if not self.pre_comet_response(msg):
            return
        to_ids = msg['raw_data'].pop('to_ids', None)
        if msg['kind'] == 'comet-response' and to_ids:
            # If the message is a response provided by a dedicated handler,
            # then we can use the specific 'to_ids' parameter to decide who
            # to send the message to.
            for session_key in to_ids:
                if session_key not in self.requests:
                    continue
                request = self.requests.pop(session_key)
                request.write(HttpResponse(200, 'application/json',
                    simplejson.dumps(msg['raw_data'])).as_bytes())
                request.finish()
        else:
            # If we're listening to another message that gets sent, we have to
            # assume that we should send it to everyone.
            requests = self.requests.values()
            self.requests.clear()
            for request in requests:
                request.write(HttpResponse(200, 'application/json',
                    simplejson.dumps(msg['raw_data'])).as_bytes())
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
        request_id = self.id_for_request(request)
        if not request_id:
            request.write(HttpResponse(403).as_bytes())
            request.finish()
            return
        
        data = {
            'headers': request.headers,
            'arguments': request.arguments,
            'remote_ip': request.remote_ip,
            'request_id': request_id,
        }
        message_kind = 'comet-%s' % (request.method,)
        if request.method == 'POST':
            data['body'] = simplejson.loads(request.body)
            request.write(HttpResponse(201).as_bytes())
            request.finish()
        else:
            self.pending_requests[request_id] = request
        self.publish(Message(message_kind, datetime.now(), data))

    def id_for_request(self, request):
        session_id = ''
        if 'Cookie' in request.headers:
            cookies = parse_cookie(request.headers['Cookie'])
            if 'sessionid' in cookies:
                session_id = cookies['sessionid']
        return session_id
    
    def pre_comet_response(self, msg):
        return True
    
    def post_init(self):
        pass


class UserAwareCometHandler(CometHandler):
    def post_init(self):
        self.pending_requests = {}

    def pre_comet_response(self, msg):
        if msg['kind'] == 'comet-user':
            req = self.pending_requests.pop(msg['raw_data']['request_id'], None)
            if not req:
                return False
            self.requests[msg['raw_data']['user_id']] = req
            return False
        return True


class BroadcastCometHandler(CometHandler):
    """
    A Comet Handler which does nothing but broadcast messages over HTTP to
    anyone who will listen.  It cannot send messages back into the stream.
    """
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
            'timestamp': json_timestamp(msg.pop('timestamp')),
        })
        self.messages.append(msg)
        while True:
            try:
                request = self.requests.get(block=False)
            except Empty:
                return
            self.respond_to_request(request)

    def handle_request(self, request):
        for url, view in self.urls:
            if request.path.startswith(url):
                return view(request)
        request.write(HttpResponse(404).as_bytes())
        request.finish()

    def comet_view(self, request):
        cursor = request.arguments.get('cursor', [None])[0]
        if cursor == 'null' and len(self.messages) > 0:
            self.respond_to_request(request)
        else:
            self.requests.put(request)
    
    def respond_to_request(self, request):
        cursor = request.arguments.get('cursor', [None])[0]
        messages = list(self.messages.after_match(lambda x: x['uuid'] == cursor,
                                                  full_fallback=True))
        json = simplejson.dumps({'messages': messages})
        response = HttpResponse(200, 'application/json', json)
        try:
            request.write(response.as_bytes())
        except IOError:
            return
        request.finish()
