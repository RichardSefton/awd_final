from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

#models
from client.models import Profile, FriendRequests, Friends

#serializers
from client.serializers import FriendRequestSerializer, PendingFriendRequests

@api_view(["POST"])
def friend_request(request):
    friendRequestSerializer = FriendRequestSerializer(data=request.data)
    if (friendRequestSerializer.is_valid()):
        friendRequestSerializer.create(friendRequestSerializer.validated_data, request.user)
        return Response(status=status.HTTP_201_CREATED, data=friendRequestSerializer.data)

    return Response(status=status.HTTP_400_BAD_REQUEST, data=friendRequestSerializer.errors)

@api_view(["GET"])
def pending_friend_requests(request):
    profile = Profile.objects.get(user=request.user)
    friend_requests = FriendRequests.objects.filter(to_user=profile)
    pendingFriendRequestsForm = PendingFriendRequests(friend_requests, many=True)
    print(pendingFriendRequestsForm)
    return Response(status=status.HTTP_200_OK, data=pendingFriendRequestsForm.data)


@api_view(["POST"])
def confirm_friend_request(request, profile_id):
    from_user = Profile.objects.get(id=profile_id)
    to_user = Profile.objects.get(user=request.user)

    try:
        friend_request = FriendRequests.objects.get(from_user=from_user, to_user=to_user)
        friend_request.delete()
        friend = Friends(profile=from_user, friend=to_user)
        friend.save()
        friend = Friends(profile=to_user, friend=from_user)
        friend.save()
    except FriendRequests.DoesNotExist:
        friend_request = None

    try:
        friend_request = FriendRequests.objects.get(from_user=to_user, to_user=from_user)
        friend_request.delete()
    except FriendRequests.DoesNotExist:
        friend_request = None

    return Response(status=status.HTTP_200_OK)

@api_view(["POST"])
def cancel_friend_request(request, profile_id):
    from_user = Profile.objects.get(user=request.user)
    to_user = Profile.objects.get(id=profile_id)
    
    try:
        friend_request = FriendRequests.objects.get(from_user=from_user, to_user=to_user)
        friend_request.delete()
    except FriendRequests.DoesNotExist:
        friend_request = None

    #Need to perform the same action for the other user
    try:
        friend_request = FriendRequests.objects.get(from_user=to_user, to_user=from_user)
        friend_request.delete()
    except FriendRequests.DoesNotExist:
        friend_request = None

    return Response(status=status.HTTP_200_OK)

@api_view(["POST"])
def decline_friend_request(request, profile_id):
    from_user = Profile.objects.get(id=profile_id)
    to_user = Profile.objects.get(user=request.user)
    
    try:
        friend_request = FriendRequests.objects.get(from_user=from_user, to_user=to_user)
        friend_request.delete()
    except FriendRequests.DoesNotExist:
        friend_request = None

    #Need to perform the same action for the other user
    try:
        friend_request = FriendRequests.objects.get(from_user=to_user, to_user=from_user)
        friend_request.delete()
    except FriendRequests.DoesNotExist:
        friend_request = None

    return Response(status=status.HTTP_200_OK)

# Create your views here.
@api_view(["POST"])
def unfriend_request(request, profile_id):
    profile = Profile.objects.get(user=request.user)
    friend = Profile.objects.get(id=profile_id)
    
    try:
        friend_record = Friends.objects.get(profile=profile, friend=friend)
        friend_record.delete()
    except FriendRequests.DoesNotExist:
        friend_record = None

    #Need to perform the same action for the other user
    try:
        friend_record = Friends.objects.get(profile=friend, friend=profile)
        friend_record.delete()
    except FriendRequests.DoesNotExist:
        friend_record = None

    return Response(status=status.HTTP_200_OK)