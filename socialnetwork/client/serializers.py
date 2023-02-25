from rest_framework import serializers
from .models import Profile, FriendRequests, Game, PlayerGameLink
from django.contrib.auth.models import User

class FriendRequestSerializer(serializers.ModelSerializer):
    profileId = serializers.IntegerField(source='profile.id')

    class Meta:
        model = Profile
        fields = ['profileId']

    def create(self, validated_data, user):
        profileId = validated_data['profile']['id']
        profile = Profile.objects.get(id=profileId)
        userProfile = Profile.objects.get(user=user)
        friendRequest = FriendRequests.objects.create(from_user=userProfile, to_user=profile)
        friendRequest.save()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Profile
        fields = ['id', 'user']

class PendingFriendRequests(serializers.ModelSerializer):
    
    class Meta:
        model = FriendRequests
        fields = ['from_user', 'to_user']

class GameRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['id', 'pgn']

class PlayerGameLinkSerializer(serializers.ModelSerializer):
    player = ProfileSerializer(many=False)

    class Meta:
        model = PlayerGameLink
        fields = ['id', 'player']

class GamesListSerializer(serializers.ModelSerializer):
    white = PlayerGameLinkSerializer(many=False)
    black = PlayerGameLinkSerializer(many=False)

    class Meta:
        model = Game
        fields = ['id', 'pgn', 'white', 'black']