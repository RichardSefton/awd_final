from django.shortcuts import render, redirect
from .forms import NewUserForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# from django.contrib.auth import authenticate, login, logout
# Create your views here.
def index(request):
    return render(request, 'home.html', {
        "authenticated": request.user.is_authenticated
    })

def register(request):
    form = NewUserForm(request.POST)
    if form.is_valid():
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("/")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    
    return render(request, 'register.html', {
        "form": form,
        "title": "Register"
    })

def login_request(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        print('Form is valid')
        print(form.cleaned_data)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        print(username, password)
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('/')
    
    return render(request, 'login.html', {
        "form": form,
        "title": "Login"
    })

def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("/")