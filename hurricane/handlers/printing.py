from hurricane.handlers.base import PureConsumeHandler

from pprint import pprint

class PrintingHandler(PureConsumeHandler):

    def receive(self, msg):
        print pprint(msg._asdict())
