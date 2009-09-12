from hurricane.handlers.base import PureConsumeHandler


class PrintingHandler(PureConsumeHandler):

    def receive(self, msg):
        print msg
