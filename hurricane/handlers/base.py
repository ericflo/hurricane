from multiprocessing import Queue


class BaseHandler(object):
    """Baseclass for all the handlers.  Each handler is guranteed to be
    executed by one thread only so unless the header spawns threads, the
    code does not have to be thread safe.

    Each handler class has one channel which is `HANDLER:import.name`
    which is used by the default auto subscription process to subscribe
    to the handler's channel.  As a matter of fact a handler is treaded
    as a singleton when it comes to auto subscriptions.
    """

    @classmethod
    def channel(cls):
        """The channel for a handler."""
        return 'HANDLER:%s.%s' % (cls.__module__, cls.__name__)

    def __init__(self, settings, app_manager):
        self.settings = settings
        self.publisher = app_manager.publisher
        self.subscription_manager = app_manager.get_subscription_manager(self)
        self.auto_subscribe(app_manager)

    def auto_subscribe(self, app_manager):
        """Called to subscribe the handlers on init."""
        for handler in app_manager.handler_classes:
            app_manager.subscribe(handler.channel(), self)

    def initialize(self):
        """Called before the run to perform initialization."""
        pass

    def run_base(self):
        """Initializes and runs."""
        self.initialize()
        try:
            self.run()
        except KeyboardInterrupt:
            pass

    def run(self):
        """Runs the handler over the subscription manager."""
        self.subscription_manager.run()

    def receive(self, msg):
        """Called if the handler received data from any of the sources
        it subscribed to.
        """
        pass

    def publish(self, msg):
        """Helper method that publishes a message to its own channel."""
        return self.publisher(self.channel(), msg)


class PurePublishHandler(BaseHandler):
    """Works like a handler but does not subscribe to anything."""

    def auto_subscribe(self, app_manager):
        pass


class PureConsumeHandler(BaseHandler):
    """A consumer that cannot publish from his own channel.  It still
    has access to the publisher but it may not attempt to publish
    from it.
    """

    def publish(self, msg):
        raise RuntimeError('a pure consumer cannot publish')
