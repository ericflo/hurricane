from __future__ import with_statement

from hurricane.handlers.base import BaseHandler

class LoggingHandler(BaseHandler):
    def message(self, msg):
        with open(self.settings.LOG_FILE, 'a') as f:
            f.write("%s\n" % msg)