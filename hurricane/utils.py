import collections
from functools import wraps

def run_until_stopped(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyboardInterrupt, SystemExit):
            try:
                self = args[0]
                self.shutdown()
            except (IndexError, AttributeError):
                pass
    return wrapped

class HttpResponse(object):
    def __init__(self, status_code, content_type=None, body=''):
        self.status_code = status_code
        self.content_type = content_type or 'text/plain'
        self.body = body

    def as_bytes(self):
        response = 'HTTP/1.1 %s\r\n' % self.status_code
        response += 'Content-Length: %s\r\n' % len(self.body)
        response += 'Content-Type: %s\r\n\r\n' % self.content_type
        response += self.body
        return response

class RingBuffer(collections.deque):
    """
    inherits deque, pops the oldest data to make room for the newest data
    when size is reached.

    http://www.daniweb.com/forums/post202523-3.html
    """
    def __init__(self, size):
        collections.deque.__init__(self)
        self.size = size

    def full_append(self, item):
        collections.deque.append(self, item)
        # full, pop the oldest item, left most item
        self.popleft()

    def append(self, item):
        collections.deque.append(self, item)
        if len(self) == self.size:
            self.append = self.full_append

    def get(self):
        return list(self)