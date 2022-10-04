from decouple import config
from django.core.mail import send_mail


def new_listener_email(listener_email):
    # send email to thatcher, notifying him that somebody signed up
    subject = "New Listener"
    html_message = "<h1>Someone signed up!</h1>"
    html_message += "<p>Email: " + listener_email + "</p>"
    from_email = config("EMAIL_FROM_USER")
    to_email = "thatcherthornberry@gmail.com"
    send_mail(subject, html_message, from_email, [to_email], html_message=html_message)

    # send an email to person thanking them, giving them info
    subject2 = "Thank you for signing up!"
    html_message2 = "<h1>Thank you for signing up!</h1>"
    html_message2 += "<p>I have to manually add you to a database to grant you access to my app. I will email you when you have access.</p>"
    html_message2 += (
        "<p>After that, you will receive a text with more instructions.</p>"
    )
    from_email2 = config("EMAIL_FROM_USER")
    to_email = listener_email
    send_mail(
        subject2, html_message2, from_email2, [to_email], html_message=html_message2
    )
