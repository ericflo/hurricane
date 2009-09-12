import Queue

from hurricane.utils import run_until_stopped

class Message(object):
    def __init__(self, kind, timestamp, raw_data):
        self.kind = kind
        self.timestamp = timestamp
        self.raw_data = raw_data

    def _asdict(self):
        return {
            'kind': self.kind,
            'timestamp': self.timestamp,
            'raw_data': self.raw_data
        }
    
    def __str__(self):
        return str(self._asdict())