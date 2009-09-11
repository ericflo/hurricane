import simplejson
import uuid

from queue import Queue

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
        IOLoop.instance().start()
    
    def handle_request(self, request):
        self.requests.append(request)
    
    def message(self, msg):
        msg = msg._asdict()
        msg.update({
            'id': str(uuid.uuid4()),
            # TODO: Figure out what else we need to add to these messages
        })
        json = simplejson.dumps(msg)
        response = json_http_response(json)
        while True:
            try:
                request = self.requests.get()
            except Queue.Empty:
                return
            request.write(response)
            request.finish()