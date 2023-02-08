from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html', {
        "authenticated": bool(request.user.username)
    })

def home(request):
    print(bool(request.user.username))
    return render(request, 'home.html', {
        "authenticated": bool(request.user.username) 
    })

# def login(request):
#     return render(request, 'login.html')