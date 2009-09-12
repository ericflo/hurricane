from datetime import datetime
import threading
import uuid
import mimetypes
import os
from Queue import Queue, Empty

import simplejson

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

from hurricane.handlers.base import BaseHandler
from hurricane.base import Message
from hurricane.utils import RingBuffer, HttpResponse

class CometHandler(BaseHandler):
    def initialize(self):
        self.requests = Queue(0)
        self.server = HTTPServer(self.handle_request)
        self.server.listen(self.settings.COMET_PORT)
        self.thread = threading.Thread(target=IOLoop.instance().start).start()
        self.messages = RingBuffer(self.settings.COMET_CACHE_SIZE)
        self.urls = self.get_urls()

    def get_urls(self):
        return (
            ('/comet/', self.comet_view),
            ('/global/', lambda r: self.media_view(r,
                os.path.join(os.path.dirname(__file__), '..', 'media'), '/global/')),
            ('/', lambda r: self.media_view(r, self.settings.MEDIA_ROOT, '/')),
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
            cursor = request.arguments.get('cursor', [None])[0]
            if cursor == 'null' and len(self.messages) > 0:
                self.respond_to_request(request)
            else:
                self.requests.put(request)

    def media_view(self, request, base_path, url_part):
        path = os.path.join(base_path, request.path[len(url_part):].lstrip('/'))    
        try:
            f = open(path).read()
        except (OSError, IOError):
            path = os.path.join(path, 'index.html')
            try:
                f = open(path).read()
            except (OSError, IOError):
                request.write(HttpResponse(404).as_bytes())
                request.finish()
                return
        (content_type, encoding) = mimetypes.guess_type(path)
        length = len(f)
        request.write(HttpResponse(200, content_type, f).as_bytes())
        request.finish()

    def receive(self, msg):
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
