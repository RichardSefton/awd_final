from django.urls import path, include
from . import api

app_name = 'api'

urlpatterns = [
    path('friends/<int:profile_id>/confirm', api.confirm_friend_request, name='confirm-friend-request'),
    path('friends/<int:profile_id>/cancel', api.cancel_friend_request, name='cancel-friend-request'),
    path('friends/<int:profile_id>/decline', api.decline_friend_request, name='decline-friend-request'),
    path('friends/<int:profile_id>/unfriend', api.unfriend_request, name='unfriend_request'),
    path('friend-request', api.friend_request, name='friend-request'),
    path('pending-friend-requests', api.pending_friend_requests, name='pending-friend-requests'),
]