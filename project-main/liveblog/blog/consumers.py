import json
from channels.generic.websocket import AsyncWebsocketConsumer
import logging


logger = logging.getLogger(__name__)
logger.warning("WebSocket connected")

class BlogConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("live_posts", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("live_posts", self.channel_name)

    async def receive(self, text_data):
        pass

    async def send_post(self, event):
        print("Broadcasting post data:", event["data"])  # Add this
        await self.send(text_data=json.dumps(event["data"]))

    async def delete_post(self, event):
        await self.send(text_data=json.dumps({
        "delete_id": event["data"]["id"]
    }))

