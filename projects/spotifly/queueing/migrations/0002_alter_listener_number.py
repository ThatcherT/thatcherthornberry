# Generated by Django 3.2.5 on 2021-07-27 23:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("queueing", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="listener",
            name="number",
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
