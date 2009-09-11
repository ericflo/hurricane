#!/usr/bin/env python

import multiprocessing
import optparse

from django.conf import settings as django_settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module

from hurricane.utils import run_until_stopped

class ApplicationManager(object):
    @run_until_stopped
    def run(self):
        parser = optparse.OptionParser()
        parser.add_option('--settings', dest='settings',
            default='hurricane.default_settings')

        options, args = parser.parse_args()
        settings = import_module(options.settings)
        django_settings.configure(settings)

        self.producer_queue = multiprocessing.Queue()
        self.receiver_queues = []

        for handler in settings.HANDLERS:
            HandlerClass = import_module(handler).Handler
            recv_queue = multiprocessing.Queue()
            handler = HandlerClass(settings, recv_queue, self.producer_queue)
            self.receiver_queues.append(recv_queue)
            multiprocessing.Process(target=handler.run_base).start()

        while True:
            item = self.producer_queue.get()
            for recv_queue in self.receiver_queues:
                recv_queue.put(item)


if __name__ == '__main__':
    app = ApplicationManager()
    app.run()
