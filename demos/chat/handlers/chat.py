import datetime

from hurricane.handlers.base import BaseHandler

from hurricane.base import Message
from hurricane.utils import RingBuffer, json_timestamp

class ChatHandler(BaseHandler):
    
    def auto_subscribe(self, app_manager):
        """
        We override this method because we don't want to receive our own
        messages.  To accomplish this, we add a conditional that prevents us
        from subscribing to our own channel.
        """
        for handler in app_manager.handler_classes:
            if handler.channel() != self.channel():
                app_manager.subscribe(handler.channel(), self)
    
    def initialize(self):
        self.messages = RingBuffer(self.settings.COMET_CACHE_SIZE)

    def receive(self, msg):
        msg = msg._asdict()
        msg.update({
            'timestamp': json_timestamp(msg.pop('timestamp')),
        })
        if msg['kind'] == 'comet-GET':
            self.handle_GET(msg)
        elif msg['kind'] == 'comet-POST':
            self.handle_POST(msg)
        else:
            self.messages.append(msg)
    
    def handle_POST(self, msg):
        msg['raw_data'] = msg['raw_data']['body']
        self.messages.append(msg)
        message = Message(
            'comet-response',
            datetime.datetime.now(),
            {'messages': [msg]}
        )
        self.publish(message)
    
    def handle_GET(self, msg):
        cursor = msg['raw_data']['arguments'].get('cursor', ['null'])[0]
        messages = list(self.messages.after_match(lambda x: x['uuid'] == cursor,
                                                  full_fallback=True))
        if not messages:
            return

        message = Message(
            'comet-response',
            datetime.datetime.now(),
            {'to_ids': [msg['raw_data']['request_id']], 'messages': messages}
        )
        self.publish(message)