# Generated by Django 3.2.5 on 2021-07-28 01:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("queueing", "0003_alter_follower_following"),
    ]

    operations = [
        migrations.AlterField(
            model_name="follower",
            name="number",
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
