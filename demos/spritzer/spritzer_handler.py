from twitstream import twitstream

from hurricane.handlers.twitter import TwitterHandler

class SpritzerHandler(TwitterHandler):
    def run(self):
        twitstream.spritzer(self.settings.TWITTER_USERNAME,
            self.settings.TWITTER_PASSWORD, self.process_tweet).run()