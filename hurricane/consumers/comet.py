import threading
import uuid
import mimetypes
from Queue import Queue, Empty

import simplejson

from django.utils._os import safe_join

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

from hurricane.base import BaseConsumer
from hurricane.utils import RingBuffer


def json_http_response(json):
    return 'HTTP/1.1 200 OK\r\nContent-Length: %d\r\nContent-Type: application/json\r\n\r\n%s' % (
        len(json),
        json
    )

class Consumer(BaseConsumer):
    def initialize(self):
        self.requests = Queue(0)
        self.server = HTTPServer(self.handle_request)
        self.server.listen(self.settings.COMET_PORT)
        self.thread = threading.Thread(target=IOLoop.instance().start).start()
        self.messages = RingBuffer(self.settings.COMET_CACHE_SIZE)
        self.urls = self.get_urls()
    
    def get_urls(self):
        return (
            ('/media/', self.media_view),
            ('/comet/', self.comet_view),
        ) 
    
    def handle_request(self, request):
        for url, view in self.urls:
            if request.path.startswith(url):
                return view(request)
        
    def comet_view(self, request):
        self.requests.put(request)
    
    def media_view(self, request):
        path = safe_join(self.settings.MEDIA_ROOT, request.path[len('/media/'):])
        try:
            f = open(path).read()
        except (OSError, IOError):
            path = safe_join(path, 'index.html')
            try:
                f = open(path).read()
            except (OSError, IOError):
                request.write('HTTP/1.1 404 NOT FOUND')
                request.finalize()
                return
        (content_type, encoding) = mimetypes.guess_type(path)
        if not content_type:
            content_type = 'text/plain'
        length = len(f)
        request.write('HTTP/1.1 200 OK\r\nContent-Length: %s\r\nContent-Type: %s\r\n\r\n%s' % (
            length,
            content_type,
            f
        ))
        request.finish()

    def shutdown(self):
        print 'Shutting Down'
        IOLoop.instance().stop()
    
    def message(self, msg):
        msg = msg._asdict()
        dt = msg.pop('timestamp')
        epoch = int(dt.strftime('%s'))
        usec = dt.microsecond
        timestamp = epoch + (usec / 1000000.0)
        msg.update({
            'id': str(uuid.uuid4()),
            'timestamp': timestamp,
        })
        self.messages.append(msg)
        self.respond_to_requests()
    
    def respond_to_requests(self):
        while True:
            try:
                request = self.requests.get(block=False)
            except Empty:
                return
            print request.arguments
            cursor = request.arguments.get('cursor', [None])[0]
            seen = False
            messages_to_send = []
            for msg in self.messages:
                if not seen and msg['id'] == cursor:
                    seen = True
                if seen:
                    messages_to_send.append(msg)                    
            messages_to_send = messages_to_send or list(self.messages)
            json = simplejson.dumps({'messages': messages_to_send})
            response = json_http_response(json)
            request.write(response)
            request.finish()
