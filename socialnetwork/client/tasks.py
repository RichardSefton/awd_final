from celery import shared_task
from client.models import Profile
from PIL import Image as img
import io
from django.core.files.uploadedfile import SimpleUploadedFile

@shared_task
def make_thumbnail(profile_id):
    profile = Profile.objects.get(pk=profile_id)
    image = img.open(str(profile.profile_pic))
    x_scale_factor = image.size[0]/100
    thumbnail = image.resize((100, int(image.size[1]/x_scale_factor)))
        
    byteArr = io.BytesIO()
    print('byteArr', byteArr)
    thumbnail.save(byteArr, format='jpeg')
    print(thumbnail)
    file = SimpleUploadedFile('thumb_'+str(profile.profile_pic), byteArr.getvalue())
    print(file)
    profile.thumbnail = file
    profile.save()
    print('done')