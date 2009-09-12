import collections
from functools import wraps
from itertools import islice

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

def import_string(import_name, silent=False):
    """Imports an object based on a string.  This is useful if you want to
    use import paths as endpoints or something similar.  An import path can
    be specified either in dotted notation (``xml.sax.saxutils.escape``)
    or with a colon as object delimiter (``xml.sax.saxutils:escape``).

    If `silent` is True the return value will be `None` if the import fails.

    :param import_name: the dotted name for the object to import.
    :param silent: if set to `True` import errors are ignored and
                   `None` is returned instead.
    :return: imported object
    """
    try:
        if ':' in import_name:
            module, obj = import_name.split(':', 1)
        elif '.' in import_name:
            module, obj = import_name.rsplit('.', 1)
        else:
            return __import__(import_name)
        return getattr(__import__(module, None, None, [obj]), obj)
    except (ImportError, AttributeError):
        if not silent:
            raise

def message_after(it, func):
    seen = False
    for item in it:
        if not seen:
            if func(item):
                seen = True
        else:
            yield item

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