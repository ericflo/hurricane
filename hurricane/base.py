import uuid


class Message(object):
    def __init__(self, kind, timestamp, raw_data):
        self.kind = kind
        self.timestamp = timestamp
        self.raw_data = raw_data
        self.uuid = str(uuid.uuid4())

    def _asdict(self):
        return {
            'kind': self.kind,
            'timestamp': self.timestamp,
            'raw_data': self.raw_data,
            'uuid': self.uuid,
        }
    
    def __str__(self):
        return str(self._asdict())

    def __repr__(self):
        return '<%s %r>' % (type(self).__name__, str(self))
