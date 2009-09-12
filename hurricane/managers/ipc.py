import multiprocessing
import Queue

from collections import defaultdict

from hurricane.managers import base


class SubscriptionManager(base.BaseSubscriptionManager):
    def __init__(self, settings, handler, queue):
        super(SubscriptionManager, self).__init__(settings, handler)
        self.queue = queue

    def run(self):
        while True:
            try:
                self.receive(self.queue.get())
            except Queue.Empty:
                pass


class Publisher(base.BasePublisher):
    def __init__(self, settings, pipe):
        self.pipe = pipe
            
    def __call__(self, channel, message):
        self.pipe.send((channel, message))


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
        self._channels[channel].add(handler)
    
    def get_subscription_manager(self, handler):
        return SubscriptionManager(self.settings, handler, self._queues[handler])
    
    def run(self):
        super(ApplicationManager, self).run()
        while True:
            channel, message = self.pipe.recv()
            self.publish(channel, message)
