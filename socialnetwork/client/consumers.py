import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import Profile, Game, PlayerGameLink

'''
Main profile websockets consumer
'''
class ProfileSockets(AsyncWebsocketConsumer):
    def save_channel(self):
        profile = Profile.objects.get(user=self.user)
        profile.websocket_user_channel = self.channel_name
        profile.save()
    
    async def connect(self):
        self.user = self.scope["user"]
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
        await self.send(text_data=json.dumps({
            'request_from': event['message']['request_from']
        }))

'''
Game websockets consumer
'''
class GameSockets(AsyncWebsocketConsumer):   
    def save_channel(self):
        profile = Profile.objects.get(user=self.user)
        game = Game.objects.get(id=self.game_id)
        if game.white.player.id == profile.id:
            game.white.websocket_game_channel = self.channel_name
            game.white.accepted = True
            game.white.save()
        else:
            game.black.websocket_game_channel = self.channel_name
            game.black.accepted = True
            game.black.save()
        game.save()
        
    async def connect(self):
        self.user = self.scope["user"]
        self.game_id = self.scope['url_route']['kwargs']['game_id']
        self.game = await database_sync_to_async(Game.objects.get)(id=self.game_id)

        await self.channel_layer.group_add(
            "game_"+str(self.user.id)+"_"+str(self.game_id),
            self.channel_name
        )

        await database_sync_to_async(self.save_channel)()
        await self.accept()

    async def disconnect(self, close_code):
        print(self)
        print(close_code)

        await self.channel_layer.group_discard(
            "game_"+str(self.user.id),
            self.channel_name
        )

    def save_game_move(self):
        self.game.save()

    def make_player_move(self, pgn):
        self.game.pgn = pgn
        if (self.game.next_move == 'white'):
            self.game.next_move = 'black'
        else:
            self.game.next_move = 'white'
        self.game.save()

    def get_user_from_player(self, game, player):
        if (player == 'white'):
            return game.white.player
        else:
            return game.black.player
        
    def get_user_profile(self):
        return Profile.objects.get(user=self.user)
    
    def get_player_websocket(self, game, player):
        if (player == 'white'):
            return game.white.websocket_game_channel
        else:
            return game.black.websocket_game_channel

    '''
    Make a player move and ping the move to the other player. 
    '''
    async def make_move(self, json_data):
        pgn = json_data['pgn']
        pgn = pgn.replace('\n', '')
        pgn = pgn.replace('*', '')
        move_made = False
        profile = await database_sync_to_async(self.get_user_profile)()
        whitePlayer = await database_sync_to_async(self.get_user_from_player)(self.game, 'white')
        blackPlayer = await database_sync_to_async(self.get_user_from_player)(self.game, 'black')
        whiteWebsocket = await database_sync_to_async(self.get_player_websocket)(self.game, 'white')
        blackWebsocket = await database_sync_to_async(self.get_player_websocket)(self.game, 'black')

        if whitePlayer.id == profile.id:
            if self.game.next_move == 'white':
                await database_sync_to_async(self.make_player_move)(pgn)
                move_made = True
        elif blackPlayer.id == profile.id:
            if self.game.next_move == 'black':
                await database_sync_to_async(self.make_player_move)(pgn)
                move_made = True

        if move_made:
            await self.channel_layer.send(
                whiteWebsocket,
                {
                    'type': 'send_move',
                    'message': {
                        'move_played': move_made,
                    }
                }
            )
            await self.channel_layer.send(
                blackWebsocket,
                {
                    'type': 'send_move',
                    'message': {
                        'move_played': move_made,  
                    }
                }
            )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json['action']
        if action == 'move':
            await self.make_move(text_data_json)

    async def send_move(self, event):
        print('send_move', self.scope["user"], event)

        await self.send(text_data=json.dumps({
            'move_played': event['message']['move_played']
        }))