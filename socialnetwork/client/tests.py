import json
from django.test import TestCase
from django.urls import reverse
from django.urls import reverse_lazy

from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase

from .model_factories import *
from .serializers import *

def returnSuccess(self):
    response = self.client.get(self.good_url)
    response.render()
    self.assertEqual(response.status_code, 200)

def returnFailure(self):
    response = self.client.get(self.bad_url)
    response.render()
    self.assertEqual(response.status_code, 404)

class FriendRequestSerializerTest(APITestCase):
    profile = None
    serialize = None

    def setup(self):
        self.profile = ProfileFactory.create()
        self.serializer = FriendRequestSerializer(data={ "profileId": self.profile.id })

    def tear_down(self):
        self.profile.delete()

    def test_friend_request_serializer(self):
        self.setup()
        if self.serializer.is_valid():
            self.assertEqual(self.serializer.data['profileId'], self.profile.id)
        self.tear_down()

class UserSerializerTest(APITestCase):
    user = None
    serializer = None

    def setup(self):
        self.user = UserFactory.create()
        self.serializer = UserSerializer(self.user)

    def tear_down(self):
        self.user.delete()

    def test_user_serializer(self):
        self.setup()
        self.assertEqual(self.serializer.data['id'], self.user.id)
        self.assertEqual(self.serializer.data['username'], self.user.username)
        self.tear_down()

class ProfileSerializerTest(APITestCase):
    profile = None
    serializer = None

    def setup(self):
        self.profile = ProfileFactory.create()
        self.serializer = ProfileSerializer(self.profile)

    def tear_down(self):
        self.profile.delete()

    def test_profile_serializer(self):
        self.setup()
        self.assertEqual(self.serializer.data['id'], self.profile.id)
        self.assertEqual(self.serializer.data['user']['id'], self.profile.user.id)
        self.assertEqual(self.serializer.data['user']['username'], self.profile.user.username)
        self.assertEqual(self.serializer.data['thumbnail'], None)
        self.tear_down()

class PendingFriendRequestsTest(APITestCase):
    friendRequest = None
    serializer = None

    def setup(self):
        self.friendRequest = FriendRequestsFactory.create()
        self.serializer = PendingFriendRequests(self.friendRequest)

    def tear_down(self):
        self.friendRequest.delete()

    def test_pending_friend_requests(self):
        self.setup()
        self.assertEqual(self.serializer.data['from_user'], self.friendRequest.from_user.id)
        self.assertEqual(self.serializer.data['to_user'], self.friendRequest.to_user.id)
        self.tear_down()

class GameRequestSerializerTest(APITestCase):
    game = None
    serializer = None

    def setup(self):
        self.game = GameFactory.create()
        self.serializer = GameRequestSerializer(self.game)

    def tear_down(self):
        self.game.delete()

    def test_game_request_serializer(self):
        self.setup()
        self.assertEqual(self.serializer.data['id'], self.game.id)
        self.assertEqual(self.serializer.data['pgn'], self.game.pgn)
        self.tear_down()

class PlayerGameLinkSerializerTest(APITestCase):
    playerGameLink = None
    serializer = None

    def setup(self):
        self.playerGameLink = PlayerGameLinkFactory.create()
        self.serializer = PlayerGameLinkSerializer(self.playerGameLink)

    def tear_down(self):
        self.playerGameLink.delete()

    def test_player_game_link_serializer(self):
        self.setup()
        self.assertEqual(self.serializer.data['id'], self.playerGameLink.id)
        self.assertEqual(self.serializer.data['player']['id'], self.playerGameLink.player.id)
        self.assertEqual(self.serializer.data['player']['user']['id'], self.playerGameLink.player.user.id)
        self.assertEqual(self.serializer.data['player']['user']['username'], self.playerGameLink.player.user.username)
        self.assertEqual(self.serializer.data['player']['thumbnail'], None)
        self.tear_down()

class GamesListSerializerTest(APITestCase):
    games = None
    serializer = None

    def setup(self):
        self.games = GameFactory.create_batch(5)
        self.serializer = GamesListSerializer(self.games, many=True)

    def tear_down(self):
        for game in self.games:
            game.delete()

    def find_game(self, id):
        for game in self.games:
            if game.id == id:
                return game
        return None

    def test_game_serializer(self):
        self.setup()
        for row in self.serializer.data:
            game = self.find_game(row['id'])
            self.assertEqual(row['id'], game.id)
            self.assertEqual(row['pgn'], game.pgn)
            self.assertEqual(row['white']['id'], game.white.id)
            self.assertEqual(row['black']['id'], game.black.id)
        self.tear_down()
