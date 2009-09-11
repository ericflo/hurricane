from hurricane.base import BaseConsumer

class Handler(BaseConsumer):
    def message(self, msg):
        print str(msg)