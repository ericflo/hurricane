from hurricane.handlers import HandlerType, get_handlers

class HandlerBase(object):    
    @classmethod
    def channel(cls):
        return '%s.%s' % (cls.__module__, cls.__name__)
        
    def __init__(self, settings, app_manager):
        self.settings = settings
        self.publisher = app_manager.publisher
        for handler in app_manager.handler_classes:
            app_manager.subscribe(handler.channel())
            

    def initialize(self):
        pass

    def run_base(self):
        self.initialize()
        self.run()

    def run(self):
        raise NotImplemented
    
    def publish(self, msg):
        return self.publisher(self.channel(), msg)