import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import Profile

class ProfileSockets(AsyncWebsocketConsumer):
    def save_channel(self):
        profile = Profile.objects.get(user=self.user)
        profile.websocket_user_channel = self.channel_name
        profile.save()
    
    async def connect(self):
        self.user = self.scope["user"]
        print('connect', "user_"+str(self.user.id), self.channel_name)
        await self.channel_layer.group_add(
            "user_"+str(self.user.id),
            self.channel_name
        )

        await database_sync_to_async(self.save_channel)()

        await self.accept()

    def get_user(self):
        return User.objects.get(id=self.user_id)

    def get_profile(self, profile_id):
        return Profile.objects.get(id=profile_id)

    def get_user_profile(self):
        return Profile.objects.get(user=self.user)

    def get_profile_user(self, profile):
        print(profile.user)
        return profile.user

    async def disconnect(self, close_code):
        print(self)
        print(close_code)

        await self.channel_layer.group_discard(
            "user_"+str(self.user.id),
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json['action']
        if action == 'friend_request':
            await self.friend_request_handler(text_data_json)

    async def friend_request_handler(self, json_data):
        profile_id = json_data['profileId']
        requestProfile = await database_sync_to_async(self.get_profile)(profile_id)
        profile = await database_sync_to_async(self.get_user_profile)()
        profile_user = await database_sync_to_async(self.get_profile_user)(profile)
        
        print(self.channel_layer)

        if (requestProfile.websocket_user_channel == None):
            requestProfile.websocket_user_channel = "blank"

        await self.channel_layer.send(
            requestProfile.websocket_user_channel,
            {
                'type': 'friend_request',
                'message': {
                    'request_from': profile_user.username,
                }
            }
        )

    async def friend_request(self, event):
        print('friend_request', self.scope["user"], event)

        await self.send(text_data=json.dumps({
            'request_from': event['message']['request_from']
        }))