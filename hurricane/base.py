import Queue

from collections import namedtuple

from hurricane.utils import run_until_stopped

class PubSubBase(object):
    def __init__(self, settings, in_queue, out_queue):
        self.settings = settings
        self.in_queue = in_queue
        self.out_queue = out_queue

    def initialize(self):
        pass

    def run_base(self):
        self.initialize()
        self.run()

    def run(self):
        raise NotImplemented

class BaseConsumer(PubSubBase):
    @run_until_stopped
    def run(self):
        while True:
            try:
                msg = self.in_queue.get()
            except Queue.Empty:
                continue
            self.message(msg)

    def message(self, msg):
        raise NotImplemented

class BaseProducer(PubSubBase):
    pass

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