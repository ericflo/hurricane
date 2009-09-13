import collections
from functools import wraps
from itertools import islice


class cached_property(object):
    """A decorator that converts a function into a lazy property.  The
    function wrapped is called the first time to retrieve the result
    and than that calculated result is used the next time you access
    the value::

        class Foo(object):

            @cached_property
            def foo(self):
                # calculate something important here
                return 42

    The class has to have a `__dict__` in order for this property to
    work.
    """

    # implementation detail: this property is implemented as non-data
    # descriptor.  non-data descriptors are only invoked if there is
    # no entry with the same name in the instance's __dict__
    # this allows us to completely get rid of the access function call
    # overhead.  If one choses to invoke __get__ by hand the property
    # will still work as expected because the lookup logic is replicated
    # in __get__ for manual invocation.

    def __init__(self, func, name=None, doc=None):
        self.__name__ = name or func.__name__
        self.__doc__ = doc
        self.func = func

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        value = obj.__dict__.get(self.__name__, _missing)
        if value is _missing:
            value = self.func(obj)
            obj.__dict__[self.__name__] = value
        return value

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

    def remove(self, item):
        raise TypeError('you cannot remove an item from the ring buffer')

    def __delitem__(self, x):
        raise TypeError('you cannot slice or delete from the ring buffer')

    def clear(self):
        super(RingBuffer, self).clear()
        self.append = type(self).append

    def _full_append(self, item):
        collections.deque.append(self, item)
        # full, pop the oldest item, left most item
        self.popleft()

    def append(self, item):
        collections.deque.append(self, item)
        if len(self) == self.size:
            self.append = self._full_append

    def after_match(self, func, full_fallback=False):
        """Returns an iterator for all the elements after the first
        match.  If `full_fallback` is `True`, it will return all the
        messages if the function never matched.
        """
        iterator = iter(self)
        for item in iterator:
            if func(item):
                return iterator
        if full_fallback:
            iterator = iter(self)
        return iterator

def json_timestamp(dt):
    epoch = int(dt.strftime('%s'))
    usec = dt.microsecond
    timestamp = epoch + (usec / 1000000.0)
    return timestamp
