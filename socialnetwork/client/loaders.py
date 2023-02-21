from .models import Profile, Status, FriendRequests
from .forms import NewStatusPostForm

def loadUserData(request):
    authenticated = request.user.is_authenticated
    profile = None

    if (authenticated):
        profile = Profile.objects.get(user=request.user)

    return [authenticated, profile]

def loadUserLandingData(request, profile):
    status_form = None
    statuses = None
    pending_friend_requests_count = 0

    if request.user.is_authenticated:
        status_form = NewStatusPostForm(request.POST)
        statuses = Status.objects.filter(profile=profile).order_by('-date')
        pending_friend_requests = FriendRequests.objects.filter(to_user=profile)
        pending_friend_requests_count = pending_friend_requests.count()

    return [status_form, statuses, pending_friend_requests_count]