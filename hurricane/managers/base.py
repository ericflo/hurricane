import multiprocessing

from hurricane.utils import import_string


class BaseSubscriptionManager(object):
    def __init__(self, settings, handler):
        self.settings = settings
        self.handler = handler

    def receive(self, message):
        self.handler.receive(message)


class BaseApplicationManager(object):
    
    def __init__(self, settings, publisher):
        self.publisher = publisher
        self.settings = settings
        self.handler_classes = [import_string(handler) for handler in settings.HANDLERS]
        self.handlers = [obj(settings, self) for obj in self.handler_classes]
    
    def subscribe(self, channel, handler):
        raise NotImplementedError
    
    def unsubscribe(self, channel, handler):
        # TODO: Implement this in the subclasses
        raise NotImplementedError
    
    def run(self):
        for handler in self.handlers:
            multiprocessing.Process(target=handler.run_base).start()
    
    def get_subscription_manager(self, handler):
        raise NotImplementedError    


class BasePublisher(object):
    def __call__(self, channel, message):
        raise NotImplementedError