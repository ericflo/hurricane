from collections import namedtuple

class PubSubBase(object):
    def __init__(self, settings, queue):
        self.settings = settings
        self.queue = queue
    
    def run(self):
        raise NotImplemented

Message = namedtuple('Message', 'kind timestamp raw_data')
