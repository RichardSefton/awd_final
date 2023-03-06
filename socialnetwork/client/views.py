from django.shortcuts import redirect
from .forms import NewUserForm, LoginForm, NewStatusPostForm, UserProfile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import User, Status, Profile, FriendRequests, Friends, Game
from django.views.generic import View, TemplateView, ListView, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .tasks import make_thumbnail
#Mixins to load data into the context
from .mixins import LoadAuthenticatedMixin, \
    LoadUserProfileMixin, LoadPendingFriendRequestsMixin, \
        LoadStatusesMixin, LoadUserFriendRequestsMixin, \
            LoadCurrentFriendsMixin, LoadGamesMixin, LoadGameMixin

'''
Home page. 

Requires authenticated user boolean, user profile, pending friend requests, statuses, and status form.
Most loaded from mixins. 

'''
class HomePage(
    LoadAuthenticatedMixin, 
    LoadUserProfileMixin,
    LoadPendingFriendRequestsMixin,
    LoadStatusesMixin, 
    ListView
):
    model = Status
    context_object_name = 'statuses'
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["status_form"] = NewStatusPostForm(self.request.POST)
        return context

'''
Register page. 

requires authenticated boolean as we want to display something different if the user is logged in.

'''
class RegisterPage(LoadAuthenticatedMixin, CreateView):
    model = User
    template_name = 'auth/register.html'
    form_class = NewUserForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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

'''
Login page.

requires authenticated boolean as we want to display something different if the user is logged in.
'''
class LoginPage(LoadAuthenticatedMixin, FormView):
    model = User
    template_name = 'auth/login.html'
    form_class = LoginForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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

# Logs the user out. 
class Logout(View):
    def get(self, request):
        logout(request)
        messages.info(request, "Logged out successfully!")
        return redirect("/")
    
'''
New status view.

Only for authenticated users.
'''
class NewStatusPage(LoginRequiredMixin, View):
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

'''
Profile page.

Only for authenticated users.

Requires authenticated user boolean, user profile and pending friend requests
'''  
class ProfilePage(
    LoginRequiredMixin, 
    LoadAuthenticatedMixin, 
    LoadUserProfileMixin, 
    LoadPendingFriendRequestsMixin,
    FormView
):
    model = Profile
    template_name = 'user/profile.html'
    form_class = UserProfile
    success_url = '/profile'
    
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
        make_thumbnail.delay(profile.id)
        messages.success(self.request, "Profile updated successfully.")
        return valid
    
'''
Friends list page

Only for authenticated users.

Requires authenticated user boolean, pending friend requests, user friend requests, and current friends.
'''
class FriendListPage(
    LoginRequiredMixin, 
    LoadAuthenticatedMixin, 
    LoadPendingFriendRequestsMixin,
    LoadUserFriendRequestsMixin,
    LoadCurrentFriendsMixin,
    ListView
):
    model = Friends
    template_name = 'friends/friendsList.html'

'''
Search page

Only for authenticated users.

Requires authenticated user boolean, pending friend requests, and user friend requests.
'''
class SearchPage(
    LoginRequiredMixin,
    LoadAuthenticatedMixin, 
    LoadPendingFriendRequestsMixin,
    LoadUserFriendRequestsMixin,
    TemplateView
):
    template_name = 'friends/search.html'
    
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

        return self.render_to_response(context)

'''
Games list page

Only for authenticated users.

Requires authenticated user boolean, user profile, pending friend requests, current friends, and games list.
'''
class GamesListPage(
    LoginRequiredMixin, 
    LoadAuthenticatedMixin, 
    LoadUserProfileMixin, 
    LoadPendingFriendRequestsMixin,
    LoadCurrentFriendsMixin,
    LoadGamesMixin,
    ListView    
):
    model = Game
    template_name = 'games/list.html'

'''
Game page

Only for authenticated users.

Requires authenticated user boolean, user profile, pending friend requests, and current game.
'''
class GamePage(
    LoginRequiredMixin, 
    LoadAuthenticatedMixin, 
    LoadUserProfileMixin, 
    LoadPendingFriendRequestsMixin,
    LoadGameMixin,
    TemplateView
):
    template_name = 'games/play.html'
    
    def dispatch(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if not context["game"]:
            return redirect('/games')

        return super().dispatch(request, *args, **kwargs)