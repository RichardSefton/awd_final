from django.urls import re_path, path

from . import consumers

websocket_urlpatterns = [
    path('ws/user', consumers.ProfileSockets.as_asgi()),
    path('ws/game/<int:game_id>', consumers.GameSockets.as_asgi()),
]