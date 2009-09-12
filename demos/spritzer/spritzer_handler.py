from twitstream import twitstream

from hurricane.handlers.twitter import Handler as TwitterHandler


class Handler(TwitterHandler):
    def run(self):
        twitstream.spritzer(self.settings.TWITTER_USERNAME,
            self.settings.TWITTER_PASSWORD, self.process_tweet).run()