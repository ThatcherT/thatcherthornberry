from decouple import config
from django.core.mail import send_mail
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Test Email"

    def handle(self, *args, **options):
        # send email to thatcher, notifying him that somebody signed up
        subject = "New Listener"
        html_message = "<h1>Someone signed up!</h1>"
        html_message += "<p>Email: " + "</p>"
        recipient_list = "fourelevenseventy@gmail.com"
        sent = send_mail(
            subject=subject,
            message=html_message,
            from_email=None,
            recipient_list=[recipient_list],
        )
        print(sent)
