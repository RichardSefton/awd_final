# Generated by Django 4.1.6 on 2023-02-25 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0014_game_playergamelink'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='playergamelink',
            name='color',
        ),
        migrations.RemoveField(
            model_name='playergamelink',
            name='websocket_channel',
        ),
        migrations.AddField(
            model_name='profile',
            name='websocket_game_channel',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]