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
        parser.add_option('--settings', dest='settings')
        
        options, args = parser.parse_args()
        if not options.settings:
            raise ImproperlyConfigured("You didn't provide a settings module.")
        settings = import_module(options.settings)
        django_settings.configure(settings)
        
        self.producer_queue = multiprocessing.Queue()
        
        for producer in settings.PRODUCERS:
            ProducerClass = import_module(producer).Producer
            producer = ProducerClass(settings, self.producer_queue)
            multiprocessing.Process(target=producer.run).start()
        
        self.receiver_queues = []

        for consumer in settings.CONSUMERS:
            ConsumerClass = import_module(consumer).Consumer
            recv_queue = multiprocessing.Queue()
            consumer = ConsumerClass(settings, recv_queue)
            self.receiver_queues.append(recv_queue)
            multiprocessing.Process(target=consumer.run).start()
        
        while True:
            item = self.producer_queue.get()
            for recv_queue in self.receiver_queues:
                recv_queue.put(item)


if __name__ == '__main__':
    app = ApplicationManager()
    app.run()
