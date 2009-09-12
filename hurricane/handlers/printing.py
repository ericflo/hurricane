from hurricane.handlers.base import BaseHandler

class PrintingHandler(BaseHandler):
    def message(self, msg):
        print msg