from datetetime import datetime
import random
import string
import time

from hurricane.base import PubSubBase, Message

class RandomDataProducder(PubSubBase):
    def run(self):
        while True:
            msg = Message('random', datetime.now(), 
                ''.join(random.sample(string.letters, 8)))
            self.queue.put(msg)
            time.sleep(1)