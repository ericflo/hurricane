import os

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

HANDLERS = (
    'spritzer.spritzer_handler.SpritzerHandler',
    'hurricane.handlers.comet.CometHandler',
)

APPLICATION_MANAGER = 'hurricane.managers.ipc'

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')

TWITTER_USERNAME = 'py_hurricane'
TWITTER_PASSWORD = 'djangoftw'

COMET_PORT = 8000
COMET_CACHE_SIZE = 200