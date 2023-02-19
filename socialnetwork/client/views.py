from django.shortcuts import render, redirect
from .forms import NewUserForm, LoginForm, NewStatusPostForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .models import Status, Profile, FriendRequests, Friends
from .serializers import FriendRequestSerializer, PendingFriendRequests
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

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
        statuses = Status.objects.filter(profile=profile).order_by('-date')
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
    profiles = None
    pending_friend_requests_count = 0

    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        pending_friend_requests_count = FriendRequests.objects.filter(to_user=profile).count()

    if request.method == "POST":
        search = request.POST['search']
        if not search == "":
            profiles = Profile.objects.filter(user__username__icontains=search)
            profiles = profiles.exclude(user=request.user)
    
    return render(request, 'friends/search.html', {
        "authenticated": request.user.is_authenticated,
        "profiles": profiles,
        "profile": profile,
        "pending_friend_requests_count": pending_friend_requests_count,
    })

def play(request):
    return render(request, 'games/play.html')

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

def friends_list(request):
    pending_friend_requests = None
    pending_friend_requests_count = 0
    user_friend_requests = None
    user_friend_requests_count = 0
    current_friends = None
    current_friends_count = 0

    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        print(profile.id)
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

@api_view(["POST"])
def confirm_friend_request(request, profile_id):
    print(profile_id);
    from_user = Profile.objects.get(id=profile_id)
    to_user = Profile.objects.get(user=request.user)
    friend_request = FriendRequests.objects.filter(from_user=from_user, to_user=to_user)
    print(friend_request)

    if friend_request.count() == 1:
        friend = Friends(profile=from_user, friend=to_user)
        print(friend)
        friend.save()
        friend_request.delete()
        friend_request.save()
        

        return Response(status=status.HTTP_200_OK)

    return Response(status=status.HTTP_400_BAD_REQUEST)
        