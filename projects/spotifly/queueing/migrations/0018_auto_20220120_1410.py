# Generated by Django 3.2.6 on 2022-01-20 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("queueing", "0017_listener_max_offset"),
    ]

    operations = [
        migrations.AlterField(
            model_name="follower",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="listener",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
    ]
