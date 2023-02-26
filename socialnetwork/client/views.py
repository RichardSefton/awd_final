from django.shortcuts import render, redirect
from .forms import NewUserForm, LoginForm, NewStatusPostForm, UserProfile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .models import User, Status, Profile, FriendRequests, Friends, Game, PlayerGameLink
from .serializers import GamesListSerializer
from django.db.models import Q
from django.views.generic import View, TemplateView, ListView, DetailView, CreateView, FormView

class HomePage(ListView):
    model = Status
    context_object_name = 'statuses'
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # This page handles both authenticated and unauthenticated users
        # As such, if the user is not authenticated this method will result in
        # errors. So we need to return early if the user is not authenticated.
        if not self.request.user.is_authenticated:
            return context

        profile = Profile.objects.get(user=self.request.user)
        context["profile"] = profile
        context["authenticated"] = self.request.user.is_authenticated
        context["status_form"] = NewStatusPostForm(self.request.POST)
        
        statuses = Status.objects.filter(profile=profile)
        friends = Friends.objects.filter(profile=profile)
        for friend in friends:
            statuses = statuses | Status.objects.filter(profile=friend.friend)
        statuses = statuses.order_by('-date') 
        context["statuses"] = statuses

        pending_friend_requests = FriendRequests.objects.filter(to_user=profile)
        context["pending_friend_requests_count"] = pending_friend_requests.count()

        return context

class RegisterPage(CreateView):
    model = User
    template_name = 'auth/register.html'
    form_class = NewUserForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["authenticated"] = self.request.user.is_authenticated
        context["title"] = "Register"
        return context

    def form_valid(self, form):
        #https://stackoverflow.com/questions/26510242/django-how-to-login-user-directly-after-registration-using-generic-createview
        valid = super(RegisterPage, self).form_valid(form)
        user = form.save()
        print(user)
        user.save()
        login_request = login(self.request, user)
        print(login_request)
        messages.success(self.request, "Registration successful.")
        return valid

class LoginPage(FormView):
    model = User
    template_name = 'auth/login.html'
    form_class = LoginForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["authenticated"] = self.request.user.is_authenticated
        context["title"] = "Login"
        return context
    
    def form_valid(self, form):
        valid = super(LoginPage, self).form_valid(form)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        messages.success(self.request, "Login successful.")
        return valid

class Logout(View):
    def get(self, request):
        logout(request)
        messages.info(request, "Logged out successfully!")
        return redirect("/")
    
class NewStatusPage(View):
    model = Status
    
    def post(self, request):
        form = NewStatusPostForm(request.POST)
        if form.is_valid():
            user = request.user
            profile = Profile.objects.get(user=user)
            newstatus = Status(profile=profile, status=form.cleaned_data.get('status'))
            newstatus.save()
            return redirect('/')
        
        messages.info(request, "Unable to post your status")
        return redirect('/')
    
class ProfilePage(FormView):
    model = Profile
    template_name = 'user/profile.html'
    form_class = UserProfile
    success_url = '/profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["authenticated"] = self.request.user.is_authenticated
        
        profile = Profile.objects.get(user=self.request.user)
        context["profile"] = profile
        
        return context
    
    def form_valid(self, form):
        valid = super(ProfilePage, self).form_valid(form)
        profile = Profile.objects.get(user=self.request.user)
        if form.cleaned_data.get('first_name'):
            profile.user.first_name = form.cleaned_data.get('first_name')
        if form.cleaned_data.get('last_name'):
            profile.user.last_name = form.cleaned_data.get('last_name')
        if form.cleaned_data.get('email'):
            profile.user.email = form.cleaned_data.get('email')
        if form.cleaned_data.get('phone'):
            profile.phone = form.cleaned_data.get('phone')
        if form.cleaned_data.get('bio'):
            profile.bio = form.cleaned_data.get('bio')
        if form.cleaned_data.get('profile_pic'):
            profile.profile_pic = form.cleaned_data.get('profile_pic')
        profile.user.save()
        profile.save()
        messages.success(self.request, "Profile updated successfully.")
        return valid
    
class FriendListPage(ListView):
    model = Friends
    template_name = 'friends/friendsList.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context["authenticated"] = self.request.user.is_authenticated

        profile = Profile.objects.get(user=self.request.user)
        pending_friend_requests = FriendRequests.objects.filter(to_user=profile)
        user_friend_requests = FriendRequests.objects.filter(from_user=profile)
        current_friends = Friends.objects.filter(profile=profile)
        
        context["pending_friend_requests"] = pending_friend_requests
        context["pending_friend_requests_count"] = pending_friend_requests.count()
        context["user_friend_requests"] = user_friend_requests
        context["user_friend_requests_count"] = user_friend_requests.count()
        context["current_friends"] = current_friends
        context["current_friends_count"] = current_friends.count()

        return context

class SearchPage(TemplateView):
    template_name = 'friends/search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["authenticated"] = self.request.user.is_authenticated
        return context
    
    def post(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        search = request.POST['search']
        if not search == "":
            profile = Profile.objects.get(user=request.user)
            profiles = Profile.objects.filter(user__username__icontains=search)
            profiles = profiles.exclude(user=request.user)
            user_friend_requests = FriendRequests.objects.filter(from_user=profile)
            pending_friend_requests = FriendRequests.objects.filter(to_user=profile)

            for user_request in user_friend_requests:
                profiles = profiles.exclude(user=user_request.from_user.user)
                profiles = profiles.exclude(user=user_request.to_user.user)
            for pending_request in pending_friend_requests:
                profiles = profiles.exclude(user=pending_request.from_user.user)
                profiles = profiles.exclude(user=pending_request.to_user.user)
            current_friends = Friends.objects.filter(profile=profile)
            for friend in current_friends:
                profiles = profiles.exclude(user=friend.friend.user)

            context["profiles"] = profiles
            context["profile"] = profile
            context["user_friend_requests"] = user_friend_requests
            context["user_friend_requests_count"] = user_friend_requests.count()
            context["pending_friend_requests"] = pending_friend_requests
            context["pending_friend_requests_count"] = pending_friend_requests.count()

        return self.render_to_response(context)

class GamesListPage(ListView):
    model = Game
    template_name = 'games/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["authenticated"] = self.request.user.is_authenticated
        
        profile = Profile.objects.get(user=self.request.user)
        context["profile"] = profile
        
        friends = Friends.objects.filter(profile=profile)
        context["friends"] = friends
        
        playerGames = PlayerGameLink.objects.filter(player=profile)
        games = None
        for playerGame in playerGames:
            if (games == None):
                games = Game.objects.filter(Q(white = playerGame) | Q(black = playerGame))
            games = games | Game.objects.filter(Q(white = playerGame) | Q(black = playerGame))

        gamesList = GamesListSerializer(games, many=True)
        context["games"] = gamesList.data

        return context

class GamePage(TemplateView):
    template_name = 'games/play.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context["authenticated"] = self.request.user.is_authenticated
        profile = Profile.objects.get(user=self.request.user)
        context["profile"] = profile

        try:
            game = Game.objects.get(id=self.kwargs['game_id'])
            context["game"] = game
        except Game.DoesNotExist:
            messages.error(self.request, "Game does not exist.")
            context["game"] = None

        return context
    
    def dispatch(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if not context["game"]:
            return redirect('/games')

        return super().dispatch(request, *args, **kwargs)