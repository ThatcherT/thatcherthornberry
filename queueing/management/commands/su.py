from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = "Create su"

    def handle(self, *args, **options):
        # delete all super users
        User.objects.filter(is_superuser=True).delete()
        if not User.objects.filter(username="thatcher", is_superuser=True).first():
            print("creating user object")

            user = User.objects.create(
                username="thatcher", is_superuser=True, is_staff=True,
            )
            user.set_password("pizza891")
            print(user.username, user.email, "pizza891")
            user.save()
        else:
            print("user already exists")
