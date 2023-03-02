from django.views.generic.base import ContextMixin
from .models import Profile, FriendRequests, Status, Friends, PlayerGameLink, Game
from .serializers import GamesListSerializer, StatusSerializer
from django.db.models import Q
from django.contrib import messages

class LoadAuthenticatedMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['authenticated'] = self.request.user.is_authenticated
        return context

class LoadUserProfileMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if self.request.user.is_authenticated:
            profile = Profile.objects.get(user=self.request.user)
            context['profile'] = profile 

        return context
    
class LoadPendingFriendRequestsMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if self.request.user.is_authenticated:
            profile = Profile.objects.get(user=self.request.user)
            pending_friend_requests = FriendRequests.objects.filter(to_user=profile)
            context["pending_friend_requests"] = pending_friend_requests
            context["pending_friend_requests_count"] = pending_friend_requests.count()

        return context
    
class LoadUserFriendRequestsMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if self.request.user.is_authenticated:
            profile = Profile.objects.get(user=self.request.user)
            user_friend_requests = FriendRequests.objects.filter(from_user=profile)
            context["user_friend_requests"] = user_friend_requests
            context["user_friend_requests_count"] = user_friend_requests.count()

        return context
    
class LoadCurrentFriendsMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if self.request.user.is_authenticated:
            profile = Profile.objects.get(user=self.request.user)
            current_friends = Friends.objects.filter(profile=profile)
            context["current_friends"] = current_friends
            context["current_friends_count"] = current_friends.count()

        return context
    
class LoadStatusesMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if self.request.user.is_authenticated:
            profile = Profile.objects.get(user=self.request.user)
            statuses = Status.objects.filter(profile=profile)
            friends = Friends.objects.filter(profile=profile)
            for friend in friends:
                statuses = statuses | Status.objects.filter(profile=friend.friend)
            statuses = statuses.order_by('-date') 
            statuses = StatusSerializer(statuses, many=True)
            context["statuses"] = statuses.data

        return context
    
class LoadGamesMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if self.request.user.is_authenticated:
            profile = Profile.objects.get(user=self.request.user)
            playerGames = PlayerGameLink.objects.filter(player=profile)
            games = None
            for playerGame in playerGames:
                if (games == None):
                    games = Game.objects.filter(Q(white = playerGame) | Q(black = playerGame))
                games = games | Game.objects.filter(Q(white = playerGame) | Q(black = playerGame))

            gamesList = GamesListSerializer(games, many=True)
            context["games"] = gamesList.data

        return context

class LoadGameMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            game = Game.objects.get(id=self.kwargs['game_id'])
            context["game"] = game
        except Game.DoesNotExist:
            messages.error(self.request, "Game does not exist.")
            context["game"] = None

        return context
