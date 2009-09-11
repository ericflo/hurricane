import simplejson
import uuid
import threading

from Queue import Queue, Empty

from hurricane.base import BaseConsumer

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

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
        self.urls = self.get_urls()
    
    def get_urls(self):
        return (
            ('/comet/', self.comet_view),
            ('/', self.wsgi_view),
        ) 
    
    def handle_request(self, request):
        for url, view in self.urls:
            if request.path.startswith(url):
                return view(request)
        
    def comet_view(self, request):
        self.requests.put(request)
    
    def wsgi_view(self, request):
        environ = {
            'REQUEST_METHOD': request.method,
            'SCRIPT_NAME':  request.path,
            'PATH_INFO': request.path,
            'QUERY_STRING': request.query,
            'CONTENT_TYPE': request.headers.get('Content-Type'),
            'CONTENT_LENGTH': request.headers['Content-Length'],
            'SERVER_NAME': request.host,
            'SERVER_PORT': self.settings.COMET_PORT,
            'SERVER_PROTOCOL': 'HTTP/1.1',
        }
        def start_response(status, headers):
            request.write('HTTP/1.1 %(status)s\r\n%(headers)s' % {
                'status': status,
                'headers': '\r\n'.join('%s: %s' % (k, v) for k, v in headers)
            })
        wsgi_app = import_module(self.settings.WSGI_CALLABLE).application
        response = wsgi_app(environ, start_response)
        request.write(''.join(response))
        request.finalize()

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
            # TODO: Figure out what else we need to add to these messages
        })
        json = simplejson.dumps(msg)
        response = json_http_response(json)
        while True:
            try:
                request = self.requests.get(block=False)
            except Empty:
                return
            request.write(response)
            request.finish()
