from simplejson import loads
from Cookie import BaseCookie, Morsel, CookieError
from hurricane.utils import cached_property

_missing = object()


def unquote_header_value(value):
    r"""Unquotes a header value.  (Reversal of :func:`quote_header_value`).
    This does not use the real unquoting but what browsers are actually
    using for quoting.

    :param value: the header value to unquote.
    """
    if value and value[0] == value[-1] == '"':
        # this is not the real unquoting, but fixing this so that the
        # RFC is met will result in bugs with internet explorer and
        # probably some other browsers as well.  IE for example is
        # uploading files with "C:\foo\bar.txt" as filename
        value = value[1:-1].replace('\\\\', '\\').replace('\\"', '"')
    return value


class _ExtendedMorsel(Morsel):
    _reserved = {'httponly': 'HttpOnly'}
    _reserved.update(Morsel._reserved)

    def __init__(self, name=None, value=None):
        Morsel.__init__(self)
        if name is not None:
            self.set(name, value, value)

    def OutputString(self, attrs=None):
        httponly = self.pop('httponly', False)
        result = Morsel.OutputString(self, attrs).rstrip('\t ;')
        if httponly:
            result += '; HttpOnly'
        return result


class _ExtendedCookie(BaseCookie):
    """Form of the base cookie that doesn't raise a `CookieError` for
    malformed keys.  This has the advantage that broken cookies submitted
    by nonstandard browsers don't cause the cookie to be empty.
    """

    def _BaseCookie__set(self, key, real_value, coded_value):
        morsel = self.get(key, _ExtendedMorsel())
        try:
            morsel.set(key, real_value, coded_value)
        except CookieError:
            pass
        dict.__setitem__(self, key, morsel)


def parse_cookie(header, charset='utf-8', errors='ignore'):
    """Parse a cookie.

    :param header: the header to be used to parse the cookie.
    :param charset: the charset for the cookie values.
    :param errors: the error behavior for the charset decoding.
    """
    cookie = _ExtendedCookie()
    if header:
        cookie.load(header)
    result = {}

    # decode to unicode and skip broken items.  Our extended morsel
    # and extended cookie will catch CookieErrors and convert them to
    # `None` items which we have to skip here.
    for key, value in cookie.iteritems():
        if value.value is not None:
            result[key] = unquote_header_value(value.value) \
                .decode(charset, errors)

    return result


class Request(object):
    """Represents a comet request."""

    def __init__(self, path, args, cookies, body):
        self.path = path
        self.args = args
        self.cookies = cookies
        self.body = body

    @cached_property
    def json_body(self):
        return loads(self.body)

    @classmethod
    def from_tornado_request(cls, req, charset='utf-8', errors='ignore'):
        q = dict(req.query)
        for key, value in q.iteritems():
            q[key] = value.decode(charset, errors)
        cookies = parse_cookie(req.headers.get('cookie'))
        return cls(req.path, req.query, cookies, req.body)

    def __repr__(self):
        return '<%s %r>' % (type(self).__name__, self.args)
