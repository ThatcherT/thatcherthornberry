# Generated by Django 3.2.5 on 2021-07-28 03:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("queueing", "0005_listener_spotify_id"),
    ]

    operations = [
        migrations.RenameField(
            model_name="listener",
            old_name="code",
            new_name="token",
        ),
        migrations.AddField(
            model_name="follower",
            name="following_spotify_id",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
