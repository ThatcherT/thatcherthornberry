from django.core.management.base import BaseCommand
from decouple import config

class Command(BaseCommand):
    help = "Create Super User with no input, useful for docker"

    def handle(self, *args, **options):
        from django.contrib.auth import get_user_model

        User = get_user_model()
        password = config('SUPER_USER_PASSWORD')
        
        u = User.objects.create_superuser("thatcher", "thatcher@thatcherthornberry.com", password)
        print("User Created!")
        print("Name...", u.username)
        print("Email...", u.email)
        print("Password...", password)
        print("Password Hash...", u.password)
