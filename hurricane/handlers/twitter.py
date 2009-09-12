from datetime import datetime

from twitstream import twitstream

from hurricane.base import Message
from hurricane.handlers.base import BaseHandler
from hurricane.utils import run_until_stopped

class TwitterHandler(BaseHandler):
    def process_tweet(self, msg):
        msg = Message('tweet', datetime.now(), msg)
        self.publish(msg)


    @run_until_stopped
    def run(self):
        twitstream.track(self.settings.TWITTER_USERNAME,
            self.settings.TWITTER_PASSWORD, self.process_tweet,
            track=','.join(self.settings.TWITTER_KEYWORDS)).run()