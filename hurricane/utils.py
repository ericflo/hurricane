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
            pass
    
    return wrapped

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