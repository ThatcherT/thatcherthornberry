from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from queueing.models import Listener, Follower
from decouple import config
from twilio.rest import Client


class Command(BaseCommand):
    help = "send marketing text"

    def handle(self, *args, **options):
        # get all listeners
        listeners = Listener.objects.all()

        # get all followers
        followers = Follower.objects.all()

        # check which of followers number is not a listener number
        for follower in followers:
            if follower.number not in [listener.number for listener in listeners]:
                if not follower.promo:

                    # use twilio api to send message asking them to sign up for spotfily

                    number = follower.number
                    message = "Want to allow others to queue songs to your device? Visit http://spotifly.thatcherthornberry.com"

                    ACCOUNT_SID = config("ACCOUNT_SID")
                    AUTH_TOKEN = config("AUTH_TOKEN")

                    # get the twilio client
                    client = Client(ACCOUNT_SID, AUTH_TOKEN)

                    # send the message
                    client.messages.create(
                        to=number, from_="+14243735305", body=message
                    )