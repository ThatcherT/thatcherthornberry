from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from queueing.models import Listener, Follower
from decouple import config
from twilio.rest import Client


class Command(BaseCommand):
    help = "send marketing text"

    def handle(self, *args, **options):
        # get all followers
        followers = Follower.objects.all()

        # check which of followers number is not a listener number
        for follower in followers:
            # set promo to True
            follower.promo = True
            # save changes
            follower.save()
