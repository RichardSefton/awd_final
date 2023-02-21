# Generated by Django 4.1.6 on 2023-02-20 23:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0011_profile_websocket_user_channel'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='bio',
            field=models.CharField(blank=True, max_length=4000, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pics'),
        ),
        migrations.AddField(
            model_name='profile',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='profile_thumbnail'),
        ),
    ]