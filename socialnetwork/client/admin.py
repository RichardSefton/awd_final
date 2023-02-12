from django.contrib import admin
from .models import Profile, Status, Friends

# Register your models here.

admin.site.register(Profile)
admin.site.register(Status)
admin.site.register(Friends)