from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer

#models
from client.models import Profile, FriendRequests, Friends, Game, PlayerGameLink, Status, StatusComment, StatusCommentLink

#serializers
from client.serializers import FriendRequestSerializer, PendingFriendRequests, GameRequestSerializer

class CommentView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [JSONRenderer]

    def post(self, request, **kwargs):
        comment_id = kwargs['comment_id']
        profile = Profile.objects.get(user=request.user)
        # m for model
        mStatus = Status.objects.get(id=comment_id)
        # Its insecure but time is not my friend right now.
        comment = StatusComment.objects.create(comment=request.data['text'])
        comment.save()
        statusCommentLink = StatusCommentLink.objects.create(status=mStatus, comment=comment, profile=profile)
        statusCommentLink.save()
        mStatus.comments.add(comment)
        mStatus.save()
        return Response(status=status.HTTP_200_OK, data={ "saved": True })

class FriendRequestView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [JSONRenderer]

    def post(self, request):
        print(self)
        print(request)
        friendRequestSerializer = FriendRequestSerializer(data=request.data)
        if (friendRequestSerializer.is_valid()):
            friendRequestSerializer.create(friendRequestSerializer.validated_data, request.user)
            return Response(status=status.HTTP_201_CREATED, data=friendRequestSerializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=friendRequestSerializer.errors)

class PendingFriendRequestsView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [JSONRenderer]

    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        friend_requests = FriendRequests.objects.filter(to_user=profile)
        pendingFriendRequestsForm = PendingFriendRequests(friend_requests, many=True)
        return Response(status=status.HTTP_200_OK, data=pendingFriendRequestsForm.data)

class ConfirmFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [JSONRenderer]

    def post(self, request, **kwargs):
        profile_id = kwargs['profile_id']
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

class CancelFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [JSONRenderer]

    def post(self, request, **kwargs):
        profile_id = kwargs['profile_id']
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

class DeclineFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [JSONRenderer]

    def post(self, request, **kwargs):
        profile_id = kwargs['profile_id']
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

class UnfriendRequestView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [JSONRenderer]

    def post(self, request, **kwargs):
        profile_id = kwargs['profile_id']
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
    
class GameInviteRequestView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [JSONRenderer]

    def post(self, request, **kwargs):
        profile_id = kwargs['profile_id']
        profile = Profile.objects.get(user=request.user)
        friend = Profile.objects.get(id=profile_id)

        try:
            friend_record = Friends.objects.get(profile=profile, friend=friend)
        except FriendRequests.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data={"message": "You are not friends with this user"})

        blank_pgn_headers = '[Event "Casual Game"]\n[Site "Social Network"]\n[White "' + str(friend.user) + '"]\n[Black "' + str(profile.user) + '"]\n'
        game = Game.objects.create(pgn_headers=blank_pgn_headers)
        game.save()
        white = PlayerGameLink.objects.create(player=friend, accepted=False)
        black = PlayerGameLink.objects.create(player=profile, accepted=True)
        white.save()
        black.save()
        game.white = white
        game.black = black
        game.save()

        game_request_serializer = GameRequestSerializer(game)  

        return Response(status=status.HTTP_200_OK, data=game_request_serializer.data)