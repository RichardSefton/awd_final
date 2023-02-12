from django.shortcuts import render, redirect
from .forms import NewUserForm, LoginForm, NewStatusPostForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .models import Status, Profile

@require_http_methods(["GET"])
def index(request):
    status_form = None
    profile = None
    statuses = None

    #If the user is logged in, load the forms and profile
    if request.user.is_authenticated:
        status_form = NewStatusPostForm(request.POST)
        profile = Profile.objects.get(user=request.user)
        statuses = Status.objects.filter(profile=profile).order_by('-date')

    return render(request, 'home.html', {
        "authenticated": request.user.is_authenticated,
        "status_form": status_form,
        "statuses": statuses
    })

@require_http_methods(["GET", "POST"])
def register(request):
    form = NewUserForm(request.POST)
    if form.is_valid():
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
    print(form.is_valid())
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

    if request.method == "POST":
        search = request.POST['search']
        if not search == "":
            profiles = Profile.objects.filter(user__username__icontains=search)
            profiles = profiles.exclude(user=request.user)
    
    print(request.user, profiles)
    return render(request, 'friends/search.html', {
        "authenticated": request.user.is_authenticated,
        "profiles": profiles
    })

def play(request):
    return render(request, 'games/play.html')
