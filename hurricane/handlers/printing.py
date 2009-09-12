from hurricane.handlers.base import BaseHandler

class PrintingHandler(BaseHandler):
    def receive(self, msg):
        print msg