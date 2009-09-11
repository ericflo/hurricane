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
        
        for producer in settings.PRODUCERS:
            ProducerClass = import_module(producer).Producer
            producer = ProducerClass(settings, self.producer_queue)
            multiprocessing.Process(target=producer.run_base).start()
        
        self.receiver_queues = []

        for consumer in settings.CONSUMERS:
            ConsumerClass = import_module(consumer).Consumer
            recv_queue = multiprocessing.Queue()
            consumer = ConsumerClass(settings, recv_queue)
            self.receiver_queues.append(recv_queue)
            multiprocessing.Process(target=consumer.run_base).start()
        
        while True:
            item = self.producer_queue.get()
            for recv_queue in self.receiver_queues:
                recv_queue.put(item)


if __name__ == '__main__':
    app = ApplicationManager()
    app.run()
