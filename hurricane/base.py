class PubSubBase(object):
    def __init__(self, settings, queue):
        self.settings = settings
        self.queue = queue
    
    def run(self):
        raise NotImplemented