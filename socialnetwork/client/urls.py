from django.urls import path, include
from . import views

app_name = 'client'

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('login', views.login_request, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout_request, name='logout'),
    path('friendslist', views.friendslist, name='friendslist'),
    path('profile', views.profile, name='profile'),
    path('search', views.search, name='search'),
    path('play', views.play, name='play'),
    path('newstatus', views.newstatus_request, name='newstatus'),
    path('friend-request', views.friend_request, name='friend-request'),
    path('pending-friend-requests', views.pending_friend_requests, name='pending-friend-requests'),
    path('friends-list', views.friends_list, name='friends-list'),
    path('friends/<int:profile_id>/confirm', views.confirm_friend_request, name='confirm-friend-request'),
]