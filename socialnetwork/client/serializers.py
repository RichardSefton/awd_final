from rest_framework import serializers
from .models import Profile, FriendRequests

class FriendRequestSerializer(serializers.ModelSerializer):
    profileId = serializers.IntegerField(source='profile.id')

    class Meta:
        model = Profile
        fields = ['profileId']

    def create(self, validated_data, user):
        profileId = validated_data['profile']['id']
        profile = Profile.objects.get(id=profileId)
        userProfile = Profile.objects.get(user=user)
        # friendRequest = FriendRequests.objects.create(from_user=userProfile, to_user=profile)
        # friendRequest.save()