from datetime import datetime
import random
import string
import time

from hurricane.base import BaseProducer, Message
from hurricane.utils import run_until_stopped

class Producer(BaseProducer):
    @run_until_stopped
    def run(self):
        while True:
            msg = Message('random', datetime.now(), 
                ''.join(random.sample(string.letters, 8)))
            self.queue.put(msg)
            time.sleep(1)
