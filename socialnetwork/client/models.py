from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Profile. Extends the default User model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    websocket_user_channel = models.CharField(max_length=256, null=True, blank=True)
    bio = models.CharField(max_length=4000, null=True, blank=True)
    phone = models.CharField(max_length=32, null=True, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics', null=True, blank=True)
    thumbnail = models.ImageField(upload_to='profile_thumbnail', null=True, blank=True)

    def __unicode__(self):
        return self.user.username

#Creates a profile when a user is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

#Saves the profile when a user is saved
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

# Status comment model
class StatusComment(models.Model):
    comment = models.CharField(max_length=4000, null=False, blank=False)

# Status model
class Status(models.Model):
    status = models.CharField(max_length=200)
    profile = models.ForeignKey(Profile, on_delete=models.DO_NOTHING)
    date = models.DateTimeField(auto_now_add=True)
    comments = models.ManyToManyField(StatusComment, through='StatusCommentLink')

    def __str__(self):
        return self.status
    
# Status comment link model. Links a users comment to a status
class StatusCommentLink(models.Model):
    status = models.ForeignKey(Status, on_delete=models.DO_NOTHING)
    comment = models.ForeignKey(StatusComment, on_delete=models.DO_NOTHING)
    profile = models.ForeignKey(Profile, on_delete=models.DO_NOTHING)

# Friend request model
class FriendRequests(models.Model):
    from_user = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, related_name='from_user')
    to_user = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, related_name='to_user')

    class Meta:
        unique_together = ('from_user', 'to_user')

# Friends model. Links two users as friends
class Friends(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, related_name='profile')
    friend = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, related_name='friend')
    friend_since = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('profile', 'friend')

# Links a player to a game
class PlayerGameLink(models.Model):
    player = models.ForeignKey(Profile, on_delete=models.DO_NOTHING)
    accepted = models.BooleanField(default=False)
    websocket_game_channel = models.CharField(max_length=256, null=True, blank=True)

# Game model
class Game(models.Model):
    pgn_headers = models.CharField(max_length=4000, null=True, blank=True)
    pgn = models.CharField(max_length=4000, default='1.')
    complete = models.BooleanField(default=False)
    result = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='result')
    white = models.ForeignKey(PlayerGameLink, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='white')
    black = models.ForeignKey(PlayerGameLink, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='black')
    next_move = models.CharField(max_length=32, default='white')