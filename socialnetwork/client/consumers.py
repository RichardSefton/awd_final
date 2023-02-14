import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import Profile

class ProfileSockets(AsyncWebsocketConsumer):
    async def connect(self):
        print(str(self.scope["user"]));

        await self.channel_layer.group_add(
            "user",
            str(self.scope["user"])
        )

        await self.accept()

    # def get_user(self):
    #     return User.objects.get(id=self.user_id)

    # def get_profile(self):
    #     return Profile.objects.get(user=self.user)

    async def disconnect(self, close_code):
        print(self)
        print(close_code)

        await self.channel_layer.group_discard(
            "user",
            str(self.scope["user"])
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['profile_id']

        print('message', message)

        # await self.channel_layer.group_send(
        #     self.profile_id,
        #     {
        #         'type': 'friend_request',
        #         'message': message
        #     }
        # )

    async def send_friend_request(self, profile):
        print(self)
