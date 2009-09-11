from hurricane.base import BaseConsumer

class Consumer(BaseConsumer):
    def message(self, msg):
        print str(msg)