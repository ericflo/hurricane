from hurricane.utils import import_string

class BaseApplicationManager(object):
    
    def __init__(self, settings, publisher):
        self.publisher = publisher
        self.handler_classes = [import_string(handler) for handler in settings.HANDLERS]
        self.handlers = [obj(settings, self) for obj in self.handler_classes]
    
    def publish(self, channel, message):
        raise NotImplementedError
    
    def subscribe(self, channel, handler):
        raise NotImplementedError
    
    def unsubscribe(self, channel, handler):
        raise NotImplementedError


class BasePublisher(object):
    def __call__(self, channel, message):
        raise NotImplementedError