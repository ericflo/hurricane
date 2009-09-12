from datetime import datetime
import random
import string
import time

from hurricane.base import Message
from hurricane.handlers.base import BaseHandler

class RandomDataHandler(BaseHandler):
    def run(self):
        while True:
            msg = Message('random', datetime.now(),
                ''.join(random.sample(string.letters, 8)))
            self.publish(msg)
            time.sleep(1)
