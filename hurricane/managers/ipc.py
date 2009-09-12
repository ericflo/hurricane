import multiprocessing

from collections import defaultdict

from hurricane.managers import base


class Publisher(base.BasePublisher):
    def __init__(self, settings, pipe):
        self.pipe = pipe
            
    def __call__(self, channel, message):
        self.pipe.put((channel, message))


class ApplicationManager(base.BaseApplicationManager):    
    def __init__(self, settings):
        self._channels = defaultdict(set)
        self._queues = defaultdict(multiprocessing.Queue)
        self.pipe, opipe = multiprocessing.Pipe()
        publisher = Publisher(settings, opipe)
        super(ApplicationManager, self).__init__(settings, publisher)

    def publish(self, channel, message):
        for handler in self._channels[channel]:
            self._queues[handler].put(message)
    
    def subscribe(self, channel, handler):
        # Atomic due to defaultdict
        self._queues[handler]
        self._channels[channel].add(handler)