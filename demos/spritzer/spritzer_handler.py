from hurricane.handlers.twitter import Handler as TwitterHandler
from hurricane.utils import run_until_stopped

from twitstream import twitstream

class Handler(TwitterHandler):
    
    @run_until_stopped
    def run(self):
        twitstream.spritzer(self.settings.TWITTER_USERNAME,
            self.settings.TWITTER_PASSWORD, self.process_tweet).run()