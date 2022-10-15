from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.mail import send_mail

# Create your views here.

from django.http import HttpResponse
import requests
from decouple import config

from me.models import Review
import requests
from bs4 import BeautifulSoup

GITHUB_URL = "https://github.com/"


def get_contributions(usernames):
    """
    Get a github user's public contributions.
    :param usernames: A string or sequence of github usernames.
    """
    contributions = {"users": [], "total": 0}

    if isinstance(usernames, str) or isinstance(usernames, unicode):
        usernames = [usernames]

    for username in usernames:
        response = requests.get("{0}{1}".format(GITHUB_URL, username))

        if not response.ok:
            contributions["users"].append({username: dict(total=0)})
            continue

        bs = BeautifulSoup(response.content, "html.parser")
        total = bs.find("div", {"class": "js-yearly-contributions"}).findNext("h2")
        contributions["users"].append(
            {username: dict(total=int(total.text.split()[0].replace(",", "")))}
        )
        contributions["total"] += int(total.text.split()[0].replace(",", ""))
        total = contributions["total"]

    return total


def index(request, contacted=None):
    contrib = get_contributions("ThatcherT")
    reviews = Review.objects.all()
    context = {"contrib": contrib, "reviews": reviews}
    if contacted:
        context["contact"] = contacted
    return render(request, "me/index.html", context)


def submit_review(request):
    if request.method == "POST":
        # TODO: set up linkedin api with thatcher access token, then check if user is connection

        # get connections from linkedin api
        # connections = requests.get('https://api.linkedin.com/v1/people/~/connections?format=json&oauth2_access_token={0}'.format(config('LINKEDIN_TOKEN')))
        review = Review()
        review.author = request.POST["author"]
        # TODO: get profile picture from linkedin
        review.relation = request.POST["relation"]
        review.title = request.POST["title"]
        review.review = request.POST["review"]
        review.rating = request.POST["rating"]

        review.save()

        # send an email to notify thatcher about the review
        subject = "You've been reviewed on thatcherthornberry.com!"
        message = "Here are the details\n\n"
        message += "Name: {0}\n".format(review.author)
        message += "Relation: {0}\n".format(review.relation)
        message += "Title: {0}\n".format(review.title)
        message += "Review: {0}\n".format(review.review)
        message += "Rating: {0}\n".format(review.rating)

        # now send an email
        email_from = config("EMAIL_FROM_USER")
        recipient_list = [config("EMAIL_FROM_USER")]
        send_mail(subject, message, email_from, recipient_list)
        return redirect(reverse("thank-you") + "#reviews")


def contact_me(request):
    if request.method == "POST":
        subject = "You've been contacted from thatcherthornberry.com!"
        message = "Here are the details\n\n"
        message += "Name: {0}\n".format(request.POST["name"])
        message += "Email: {0}\n".format(request.POST["email"])
        message += "Message: {0}\n".format(request.POST["message"])

        # now send an email
        email_from = config("EMAIL_FROM_USER")
        recipient_list = [config("EMAIL_FROM_USER")]
        send_mail(subject, message, email_from, recipient_list)
        return redirect(reverse("index-contacted", args=["contacted"]) + "#contact")


def projects(request):
    return render(request, "me/projects.html")
