from hurricane.models import Item
from hurricane.base import BaseConsumer

class Consumer(BaseConsumer):
    def message(self, msg):
        Item.objects.create(
            kind=msg.kind,
            timestamp=msg.timestamp,
            raw_data=msg.raw_data,
        )