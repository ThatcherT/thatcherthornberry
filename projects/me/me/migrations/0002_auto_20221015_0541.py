# Generated by Django 3.1 on 2022-10-15 05:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("me", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="review",
            options={"ordering": ["-created_at"]},
        ),
    ]
