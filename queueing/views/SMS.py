from braces.views import CsrfExemptMixin
from decouple import config
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from queueing.utils.messages import (album_mix_message, follow_message,
                                     idk_message, queue_message,
                                     register_message, shuffle_message)


@api_view(("POST",))
@csrf_exempt
def sms_failed(request):
    """
    Send failure message if twilio webhook triggers it
    """
    resp = MessagingResponse()
    resp.message("We're sorry, something went wrong on our end.")
    return HttpResponse(str(resp))


class send(APIView):
    """
    Send a message to a certain number, this is a utility function
    """

    def post(self, request, format=None):
        """
        Send a message to a certain number
        """
        # get the number from the request
        number = request.data.get("number")
        # get the message from the request
        message = request.data.get("message")
        # get the twilio account info from the request
        ACCOUNT_SID = config("ACCOUNT_SID")
        AUTH_TOKEN = config("AUTH_TOKEN")
        # get the twilio client
        client = Client(ACCOUNT_SID, AUTH_TOKEN)
        # send the message
        client.messages.create(to=number, from_="+14243735305", body=message)
        return Response(status=status.HTTP_200_OK)


class SMS(CsrfExemptMixin, APIView):
    """
    All Texts are Routed Here. Then, we'll send messages to the other relevant api functions.

    We'll get the response from those functions.

    So, what can we do?

    1. If user registers -> create account, then reply with spotify auth url.
    2. If user follows someone -> create account if needed, associate account with listener, reply with message
    3. If user queues a song -> check if listener exists, if not, reply asking them to follow someone. If they exist, add song to queue for associated account.

    """

    authentication_classes = []

    def post(self, request, format=None):
        message_body = request.data.get("Body").lower()

        if message_body[-1] == " ":
            message_body = message_body[:-1]

        # Get the sender's phone number from the request
        from_number = str(request.data.get("From"))[2:]  # skip the +1

        # register flow
        if message_body.startswith("register"):
            return register_message()

        # follow flow
        elif message_body.startswith("follow"):
            return follow_message(message_body, from_number)

        # mix album
        elif message_body.startswith("mix"):
            return album_mix_message(message_body, from_number)

        # shuffle
        elif message_body.lower().startswith("shuffle"):
            return shuffle_message(from_number)

        # queue flow
        elif message_body.lower().startswith("queue"):
            return queue_message(message_body, from_number)

        else:
            return idk_message()
