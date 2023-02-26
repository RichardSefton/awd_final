from django.urls import path, include
from . import views

app_name = 'client'

urlpatterns = [
    path('', views.HomePage.as_view(), name='index'),
    path('index', views.HomePage.as_view(), name='index'),
    path('login', views.LoginPage.as_view(), name='login'),
    path('register', views.RegisterPage.as_view(), name='register'),
    path('logout', views.Logout.as_view(), name='logout'),
    path('profile', views.ProfilePage.as_view(), name='profile'),
    path('friends-list', views.FriendListPage.as_view(), name='friends-list'),
    path('search', views.SearchPage.as_view(), name='search'),
    path('newstatus', views.NewStatusPage.as_view(), name='newstatus'),
    path('games', views.GamesListPage.as_view(), name='games'),
    path('play/<int:game_id>', views.GamePage.as_view(), name='play'),
]