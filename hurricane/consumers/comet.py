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
    
    def handle_request(self, request):
        self.requests.put(request)
    
    def shutdown(self):
        print 'Shutting Down'
        IOLoop.instance().stop()
    
    def message(self, msg):
        print "HAI %s" % (msg,)
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
