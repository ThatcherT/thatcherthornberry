# Generated by Django 4.1.6 on 2023-02-11 00:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("portability", "0002_alter_post_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="date",
            field=models.DateField(auto_now_add=True),
        ),
    ]
