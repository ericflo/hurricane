from multiprocessing import Queue


class BaseHandler(object):    
    @classmethod
    def channel(cls):
        return '%s.%s' % (cls.__module__, cls.__name__)
        
    def __init__(self, settings, app_manager):
        self.settings = settings
        self.publisher = app_manager.publisher
        self.subscription_manager = app_manager.get_subscription_manager(self)
        self.auto_subscribe(app_manager)

    def auto_subscribe(self, app_manager):
        for handler in app_manager.handler_classes:
            app_manager.subscribe(handler.channel(), self)
            
    def initialize(self):
        pass

    def run_base(self):
        self.initialize()
        self.run()

    def run(self):
        self.subscription_manager.run()
    
    def receive(self, msg):
        pass
    
    def publish(self, msg):
        return self.publisher(self.channel(), msg)
