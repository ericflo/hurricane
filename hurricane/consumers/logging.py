from hurricane.base import BaseConsumer

class Consumer(BaseConsumer):
    def message(self, msg):
        f = open(self.settings.LOG_FILE, 'a')
        f.write(str(msg) + '\n')
        f.close()