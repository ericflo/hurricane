import os

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

CONSUMERS = (
    'hurricane.consumers.printing',
    'hurricane.consumers.comet',
)

PRODUCERS = (
    'hurricane.producers.random_data',
)

LOG_FILE = 'message-log.txt'

COMET_PORT = 8000

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')