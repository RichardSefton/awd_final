from django.shortcuts import render, redirect
from .forms import NewUserForm, LoginForm, NewStatusPostForm, UserProfile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .models import Status, Profile, FriendRequests, Friends
from django.forms.models import model_to_dict

@require_http_methods(["GET"])
def index(request):
    status_form = None
    profile = None
    statuses = None
    pending_friend_requests_count = 0

    #If the user is logged in, load the forms and profile
    if request.user.is_authenticated:
        status_form = NewStatusPostForm(request.POST)
        profile = Profile.objects.get(user=request.user)
        statuses = Status.objects.filter(profile=profile)
        friends = Friends.objects.filter(profile=profile)
        for friend in friends:
            statuses = statuses | Status.objects.filter(profile=friend.friend)
        statuses = statuses.order_by('-date')
        pending_friend_requests = FriendRequests.objects.filter(to_user=profile)
        pending_friend_requests_count = pending_friend_requests.count()

    return render(request, 'home.html', {
        "authenticated": request.user.is_authenticated,
        "status_form": status_form,
        "statuses": statuses,
        "pending_friend_requests_count": pending_friend_requests_count,
    })

@require_http_methods(["GET", "POST"])
def register(request):
    form = NewUserForm(request.POST)
    if form.is_valid():
        user = form.save()
        user.save()
        login(request, user)
        messages.success(request, "Registration successful." )
        return redirect("/")
    
    messages.error(request, "Unsuccessful registration. Invalid information.")
    
    return render(request, 'auth/register.html', {
        "form": form,
        "authenticated": request.user.is_authenticated,
        "title": "Register"
    })

@require_http_methods(["GET", "POST"])
def login_request(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('/')
    
    return render(request, 'auth/login.html', {
        "form": form,
        "authenticated": request.user.is_authenticated,
        "title": "Login"
    })

@require_http_methods(["GET"])
def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("/")

@require_http_methods(["POST"])
def newstatus_request(request):
    form = NewStatusPostForm(request.POST)
    if form.is_valid():
        user = request.user
        profile = Profile.objects.get(user=user)
        newstatus = Status(profile=profile, status=form.cleaned_data.get('status'))
        newstatus.save()
        return redirect('/')
    
    messages.info(request, "Unable to post your status")
    return redirect('/')

def friendslist(request):
    return render(request, 'friends/list.html')

def profile(request):
    return render(request, 'user/profile.html')

@require_http_methods(["GET", "POST"])
def search(request):
    if not request.user.is_authenticated:
        return redirect('/')

    profiles = None
    user_friend_requests_count = 0
    user_friend_requests = None
    pending_friend_requests = None
    pending_friend_requests_count = 0
    current_friends = None

    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        user_friend_requests = FriendRequests.objects.filter(from_user=profile)
        user_friend_requests_count = user_friend_requests.count()
        pending_friend_requests = FriendRequests.objects.filter(to_user=profile)
        pending_friend_requests_count = pending_friend_requests.count()

    if request.method == "POST":
        search = request.POST['search']
        if not search == "":
            profiles = Profile.objects.filter(user__username__icontains=search)
            profiles = profiles.exclude(user=request.user)
            for user_request in user_friend_requests:
                profiles = profiles.exclude(user=user_request.from_user.user)
                profiles = profiles.exclude(user=user_request.to_user.user)
            for pending_request in pending_friend_requests:
                profiles = profiles.exclude(user=pending_request.from_user.user)
                profiles = profiles.exclude(user=pending_request.to_user.user)
            current_friends = Friends.objects.filter(profile=profile)
            for friend in current_friends:
                profiles = profiles.exclude(user=friend.friend.user)

    
    return render(request, 'friends/search.html', {
        "authenticated": request.user.is_authenticated,
        "profiles": profiles,
        "profile": profile,
        "user_friend_requests_count": user_friend_requests_count,
        "user_friend_requests": user_friend_requests,
        "pending_friend_requests_count": pending_friend_requests_count,
        "pending_friend_requests": pending_friend_requests,
    })

def play(request):
    return render(request, 'games/play.html')

@require_http_methods(["GET"])
def friends_list(request):
    #If we are not authenticated, redirect. 
    if not request.user.is_authenticated:
        return redirect('/')

    pending_friend_requests = None
    pending_friend_requests_count = 0
    user_friend_requests = None
    user_friend_requests_count = 0
    current_friends = None
    current_friends_count = 0

    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        pending_friend_requests = FriendRequests.objects.filter(to_user=profile)
        pending_friend_requests_count = pending_friend_requests.count()
        user_friend_requests = FriendRequests.objects.filter(from_user=profile)
        user_friend_requests_count = user_friend_requests.count()
        current_friends = Friends.objects.filter(profile=profile)
        current_friends_count = current_friends.count()

    return render(request, 'friends/friendsList.html', {
        "pending_friend_requests_count": pending_friend_requests_count,
        "pending_friend_requests": pending_friend_requests,
        "user_friend_requests": user_friend_requests,
        "user_friend_requests_count": user_friend_requests_count,
        "authenticated": request.user.is_authenticated,
        "current_friends": current_friends,
        "current_friends_count": current_friends_count
    })

@require_http_methods(["GET", "POST"])
def profile_request(request):
    if not request.user.is_authenticated:
        return redirect('/')

    profile_form = None

    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)

    if request.method == "POST":   
        profile_form = UserProfile(request.POST, request.FILES) 
        if profile_form.is_valid():
            print(profile_form.cleaned_data)
            if profile_form.cleaned_data.get('first_name'):
                profile.user.first_name = profile_form.cleaned_data.get('first_name')
            if profile_form.cleaned_data.get('last_name'):
                profile.user.last_name = profile_form.cleaned_data.get('last_name')
            if profile_form.cleaned_data.get('email'):
                profile.user.email = profile_form.cleaned_data.get('email')
            if profile_form.cleaned_data.get('phone'):
                profile.phone = profile_form.cleaned_data.get('phone')
            if profile_form.cleaned_data.get('bio'):
                profile.bio = profile_form.cleaned_data.get('bio')
            if profile_form.cleaned_data.get('profile_pic'):
                profile.profile_pic = profile_form.cleaned_data.get('profile_pic')
            profile.user.save()
            profile.save()


    return render(request, 'user/profile.html', {
        "authenticated": request.user.is_authenticated,
        "profile": profile
    })



