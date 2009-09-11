from datetime import datetime

from twitstream import twitstream

from hurricane.base import BaseProducer, Message
from hurricane.utils import run_until_stopped

class Producer(BaseProducer):
    def process_tweet(self, msg):
        msg = Message('tweet', datetime.now(), {'text': msg.get('text')})
        self.queue.put(msg)
        
    
    @run_until_stopped
    def run(self):
        twitstream.track(self.settings.TWITTER_USERNAME,
            self.settings.TWITTER_PASSWORD, self.process_tweet,
            track=','.join(self.settings.TWITTER_KEYWORDS)).run()
