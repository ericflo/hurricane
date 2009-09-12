import time
import socket

from collections import defaultdict

try:
    import cPickle as pickle
except ImportError:
    import pickle

from hurricane.base import Message
from hurricane.managers import base

# This is the reason that we can't name this manager module stomp, and have to
# name it stompqueue instead.
import stomp

class SubscriptionManager(base.BaseSubscriptionManager):
    def __init__(self, settings, handler, channels):
        super(SubscriptionManager, self).__init__(settings, handler)
        self.host = settings.STOMP_HOST
        self.port = settings.STOMP_PORT
        self.destination_base = settings.STOMP_DESTINATION_BASE
        self.channels = channels
    
    def on_message(self, headers, message):
        decoded_msg = pickle.loads(message)
        self.receive(decoded_msg)
    
    def run(self):
        connected = False
        while not connected:
            # try and connect to the stomp server
            # sometimes this takes a few goes so we try until we succeed
            try:
                self.conn = stomp.Connection(host_and_ports=[(self.host, self.port)])
                # register out event hander above
                self.conn.set_listener(self.handler.channel(), self)
                self.conn.start()
                self.conn.connect()
                for channel in self.channels:
                    topic = self.destination_base + channel
                    self.conn.subscribe(destination=topic, ack='auto')
                connected = True
            except socket.error:
                pass
        
        while 1:
            time.sleep(20)


class Publisher(base.BasePublisher):
    def __init__(self, settings):
        self.host = settings.STOMP_HOST
        self.port = settings.STOMP_PORT
        self.destination_base = settings.STOMP_DESTINATION_BASE
        self.conn = stomp.Connection([(self.host, self.port)])
        self.conn.start()
        self.conn.connect()
    
    def __call__(self, channel, message):
        encoded_msg = pickle.dumps(message)
        self.conn.send(encoded_msg, destination=self.destination_base + channel)

class ApplicationManager(base.BaseApplicationManager):
    def __init__(self, settings):
        self._handler_subscriptions = defaultdict(set)
        publisher = Publisher(settings)
        super(ApplicationManager, self).__init__(settings, publisher)

    def publish(self, channel, message):
        self.publisher(channel, message)
    
    def subscribe(self, channel, handler):
        self._handler_subscriptions[handler].add(channel)
    
    def get_subscription_manager(self, handler):
        return SubscriptionManager(self.settings, handler, self._handler_subscriptions[handler])
    
    def run(self):
        super(ApplicationManager, self).run()
