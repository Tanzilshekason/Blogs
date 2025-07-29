import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import LivePost, Comment
from django.contrib.auth import get_user_model

User = get_user_model()

class LivePostConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("live_posts", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("live_posts", self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        await self.channel_layer.group_send(
            "live_posts",
            {
                'type': 'new_post',
                'message': data
            }
        )

    async def new_post(self, event):
        await self.send(text_data=json.dumps(event['message']))


class CommentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.post_id = self.scope['url_route']['kwargs']['post_id']
        self.room_group_name = f'post_{self.post_id}_comments'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        comment = await self.save_comment(data)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'new_comment',
                'comment': {
                    'user': comment.user.username,
                    'content': comment.content,
                    'created_at': comment.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                }
            }
        )

    async def new_comment(self, event):
        await self.send(text_data=json.dumps(event['comment']))

    @database_sync_to_async
    def save_comment(self, data):
        user = User.objects.get(username=data['user'])
        post = LivePost.objects.get(id=self.post_id)
        return Comment.objects.create(user=user, post=post, content=data['content'])
