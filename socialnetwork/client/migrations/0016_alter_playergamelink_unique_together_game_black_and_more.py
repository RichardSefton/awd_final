# Generated by Django 4.1.6 on 2023-02-25 15:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0015_remove_playergamelink_color_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='playergamelink',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='game',
            name='black',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='black', to='client.playergamelink'),
        ),
        migrations.AddField(
            model_name='game',
            name='white',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='white', to='client.playergamelink'),
        ),
        migrations.RemoveField(
            model_name='playergamelink',
            name='game',
        ),
    ]
