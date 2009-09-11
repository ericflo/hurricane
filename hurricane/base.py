import Queue

from collections import namedtuple

class PubSubBase(object):
    def __init__(self, settings, queue):
        self.settings = settings
        self.queue = queue
    
    def run(self):
        raise NotImplemented

class BaseConsumer(object):
    def run(self):
        while True:
            try:
                msg = self.queue.get()
            except Queue.Empty:
                continue
            self.message(msg)
    
    def message(self, msg):
        raise NotImplemented

class BaseProducer(object):
    pass

Message = namedtuple('Message', 'kind timestamp raw_data')