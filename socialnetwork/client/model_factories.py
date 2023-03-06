import factory

from .models import *
from django.contrib.auth.models import User

class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Faker('name')
    email = factory.Faker('email')

    class Meta:
        model = User

class ProfileFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    websocket_user_channel = 'test'
    bio = 'test'
    phone = 'test'

    class Meta:
        model = Profile
        django_get_or_create = ('user',)

class StatusCommentFactory(factory.django.DjangoModelFactory):
    comment = factory.Faker('sentence')

    class Meta:
        model = StatusComment 

class StatusFactory(factory.django.DjangoModelFactory):
    status = factory.Faker('sentence')
    profile = factory.SubFactory(ProfileFactory)
    comments = factory.SubFactory(StatusCommentFactory)

    class Meta:
        model = Status
        django_get_or_create = ('profile', 'comments')

class StatusCommentLinkFactory(factory.django.DjangoModelFactory):
    status = factory.SubFactory(StatusFactory)
    comment = factory.SubFactory(StatusCommentFactory)
    profile = factory.SubFactory(ProfileFactory)

    class Meta:
        model = StatusCommentLink
        django_get_or_create = ('status', 'comment', 'profile')

class FriendRequestsFactory(factory.django.DjangoModelFactory):
    from_user = factory.SubFactory(ProfileFactory)
    to_user = factory.SubFactory(ProfileFactory)

    class Meta:
        model = FriendRequests
        django_get_or_create = ('from_user', 'to_user')

class FriendsFactory(factory.django.DjangoModelFactory):
    profile = factory.SubFactory(ProfileFactory)
    friend = factory.SubFactory(ProfileFactory)

    class Meta:
        model = Friends

class PlayerGameLinkFactory(factory.django.DjangoModelFactory):
    player = factory.SubFactory(ProfileFactory)
    accepted = False
    websocket_game_channel = 'test'

    class Meta:
        model = PlayerGameLink
        django_get_or_create = ('player',)

class GameFactory(factory.django.DjangoModelFactory):
    pgn_headers = 'test'
    pgn = '1. e4'
    complete = False
    result = None
    white = factory.SubFactory(PlayerGameLinkFactory)
    black = factory.SubFactory(PlayerGameLinkFactory)
    next_move = 'white'

    class Meta:
        model = Game
        django_get_or_create = ('white', 'black')