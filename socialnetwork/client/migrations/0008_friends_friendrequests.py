# Generated by Django 4.1.6 on 2023-02-14 20:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0007_remove_profile_friends_delete_friends'),
    ]

    operations = [
        migrations.CreateModel(
            name='Friends',
            fields=[
                ('friend_since', models.DateTimeField(auto_now_add=True)),
                ('friend', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='friend', to='client.profile')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='profile', to='client.profile')),
            ],
        ),
        migrations.CreateModel(
            name='FriendRequests',
            fields=[
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='from_user', to='client.profile')),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='to_user', to='client.profile')),
            ],
        ),
    ]
