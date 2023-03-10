# Generated by Django 4.1.6 on 2023-03-02 20:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0020_rename_next_mode_game_next_move'),
    ]

    operations = [
        migrations.CreateModel(
            name='StatusComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=4000)),
                ('commenter', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='client.profile')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.status')),
            ],
        ),
    ]
