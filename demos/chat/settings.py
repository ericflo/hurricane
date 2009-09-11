import os

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

HANDLERS = (
    'hurricane.handlers.comet',
    'chat.chat_handler',
)

LOG_FILE = 'message-log.txt'

COMET_PORT = 8000
COMET_CACHE_SIZE = 200

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')