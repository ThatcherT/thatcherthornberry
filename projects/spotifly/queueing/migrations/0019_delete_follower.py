# Generated by Django 3.2.6 on 2022-10-07 21:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("queueing", "0018_auto_20220120_1410"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Follower",
        ),
    ]