import os
import sys
import django
import csv
from collections import defaultdict

#Progress bar to track the progress
#From https://gist.github.com/vladignatyev/06860ec2040cb497f0f3
def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush() 

# The current working directory in dev is /com.docker.devenvironment.code
# csv files are in a folder in this directory so should be able to append the string
currentpath = os.path.dirname(os.path.realpath(__file__))
relativepath = "../" # Scrips are in sibling directory
currentpath = os.path.join(currentpath, relativepath)

sys.path.append(currentpath)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "socialnetwork.settings")
#setup django
django.setup()

from client.models import *
from client.forms import *

#Clear the Database
FriendRequests.objects.all().delete()
Friends.objects.all().delete()

Profile.objects.all().delete()
User.objects.all().delete()

newusers = [
    {
        "username": "richard",
        "email": "richard.sefton@googlemail.com",
        "password1": "Password123!",
        "password2": "Password123!"
    },
    {
        "username": "rsefton",
        "email": "richard.sefton@thenavpeople.co.uk",
        "password1": "Password123!",
        "password2": "Password123!"
    },
]

index=0
for user in newusers:
    progress(index, len(newusers), 'Creating Users')
    index+=1
    form = NewUserForm(user)
    if form.is_valid():
        user = form.save()
        user.save()
