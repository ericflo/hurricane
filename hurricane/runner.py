import optparse

from django.utils.importlib import import_module

def main():
    parser = optparse.OptionParser()
    parser.add_option('--settings', dest='settings')
    
    options, args = parser.parse_args()
    settings = import_module(options.settings)
    
    for consumer in settings.CONSUMERS:
        ConsumerClass = import_module(consumer)
        consumer = ConsumerClass(settings)
        consumer.run()
    
    for producer in settings.PRODUCERS:
        ProducerClass = import_module(producer)
        producer = ProducerClass(settings)
        producer.run()
    

if __name__ == '__main__':
    main()
