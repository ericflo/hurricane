#!/usr/bin/env python

import multiprocessing
import optparse

from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module

class ApplicationManager(object):
    def run(self):
        parser = optparse.OptionParser()
        parser.add_option('--settings', dest='settings')
        
        options, args = parser.parse_args()
        if not options.settings:
            raise ImproperlyConfigured("You didn't provide a settings module.")
        settings = import_module(options.settings)
        
        self.producer_queue = multiprocessing.Queue()
        
        for producer in settings.PRODUCERS:
            ProducerClass = import_module(producer)
            producer = ProducerClass(settings, self.producer_queue)
            producer.run()
        
        self.receiver_queues = []

        for consumer in settings.CONSUMERS:
            ConsumerClass = import_module(consumer)
            recv_queue = multiprocessing.Queue()
            consumer = ConsumerClass(settings, recv_quee)
            self.receiever_queues.append(recv_queue)
            consumer.run()
        
        while True:
            item = self.producer_queue.get()
            for recv_queue in self.receiver_queues:
                recv_queue.put(item)


if __name__ == '__main__':
    app = ApplicationManager()
    app.run()
