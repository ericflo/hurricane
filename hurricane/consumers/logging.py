from hurricane.base import BaseConsumer

class Handler(BaseConsumer):
    def message(self, msg):
        f = open(self.settings.LOG_FILE, 'a')
        f.write(str(msg) + '\n')
        f.close()