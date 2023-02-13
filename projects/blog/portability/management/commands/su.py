from decouple import config
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create Django admin super user"

    def handle(self, *args, **options):
        # delete all super users
        User.objects.filter(is_superuser=True).delete()
        if not User.objects.filter(username="thatcher", is_superuser=True).first():
            print("creating user object")

            user = User.objects.create(
                username="thatcher",
                is_superuser=True,
                is_staff=True,
            )
            password = config("DJANGO_ADMIN_PASSWORD")
            user.set_password(password)
            print(user.username, user.email, password)
            user.save()
        else:
            print("user already exists")
