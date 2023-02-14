from rest_framework import serializers
from .models import Profile, Friends
from .consumers import ProfileSockets

class FriendRequestSerializer(serializers.ModelSerializer):
    profileId = serializers.IntegerField(source='profile.id')

    class Meta:
        model = Profile
        fields = ['profileId']

    def create(self, validated_data, user):
        profileId = validated_data['profile']['id']
        friend = Profile.objects.get(id=profileId)
        userProfile = Profile.objects.get(user=user)
        newFriend = Friends.objects.create(profile=userProfile, friend=friend)
        userProfile.friends.add(newFriend)
        userProfile.save()    
