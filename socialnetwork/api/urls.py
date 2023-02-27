from django.urls import path, include
from . import api

app_name = 'api'

urlpatterns = [
    path('friends/<int:profile_id>/confirm', api.ConfirmFriendRequestView.as_view(), name='confirm-friend-request'),
    path('friends/<int:profile_id>/cancel', api.CancelFriendRequestView.as_view(), name='cancel-friend-request'),
    path('friends/<int:profile_id>/decline', api.DeclineFriendRequestView.as_view(), name='decline-friend-request'),
    path('friends/<int:profile_id>/unfriend', api.UnfriendRequestView.as_view(), name='unfriend_request'),
    path('friend-request', api.FriendRequestView.as_view(), name='friend-request'),
    path('pending-friend-requests', api.PendingFriendRequestsView.as_view(), name='pending-friend-requests'),
    path('game/invite/<int:profile_id>', api.GameInviteRequestView.as_view(), name='game_invite'),
]