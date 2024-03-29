import os
import random

import spotipy
from queueing.utils.constants import SCOPE
from decouple import config
from django.core.mail import send_mail
from django.http import JsonResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from queueing.models import Listener
from queueing.utils.constants import sp_oauth


def home(request):
    """
    Render html
    """
    return render(request, "index.html")


def invite_link(request, username):
    """
    The person that clicked this link wants to follow the dj and open the app.
    """
    # get the listener with username
    try:
        listener = Listener.objects.get(name=username)
    except Listener.DoesNotExist:
        # something went wrong here...  just redirect them to the site.. I'm sure they can figure it out
        return redirect(reverse("home"))
    # set the dj in the session
    request.session["followingDJ"] = listener.name
    request.session.set_expiry(60 * 60 * 24 * 365 * 10)  # expire in ten year
    return redirect(reverse("home"))


def playlist_sink_link(request):
    """
    We're gonna call it Sync Links. This function 
    """
    return


def spotify_connect_link(request):
    """
    return the link users can use to authenticate with spotify
    """
    # get secrets from env with decouple
    client_id = config("SPOTIFY_CLIENT_ID")
    redirect_uri = config("SPOTIFY_REDIRECT_URI")
    scope = SCOPE
    url = f"https://accounts.spotify.com/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&scope={scope}"
    print(url)
    # send url in json response
    return JsonResponse({"url": url})


def sp_redirect(request):
    """
    Use the client authorization code flow to get a token to make requests on behalf of the user
    Store that token and associate it with the listener.
    Spotify redirects users to this view after they have authenticated with spotify.
    """
    # listdir of root directory
    root_dir = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
    # if root_dir contains a file called .cache, remove it
    if os.path.isfile(os.path.join(root_dir, ".cache")):
        print("removing cache! this wasnt supposed to be here....")
        os.remove(os.path.join(root_dir, ".cache"))

    # get code from url
    uri = request.build_absolute_uri()
    code = uri.split("?code=")[1]
    # parse token from code OPTIMIZE: this creates a file called .cache, we don't need it
    token_info = sp_oauth.get_access_token(code=code)
    if os.path.isfile(os.path.join(root_dir, ".cache")):
        print("removing cache! this was expected, but not optimal")
        os.remove(os.path.join(root_dir, ".cache"))
    token = token_info["access_token"]

    # get spotify username with token
    sp = spotipy.Spotify(auth=token)
    not_in_dashboard = False
    try:
        user = sp.current_user()
        username = user["id"]
    except:
        # generate a username using queueing/random_names/adjectives.txt and queueing/random_names/animals.txt
        # get the adjectives
        not_in_dashboard = True
        with open("queueing/random_names/adjectives.txt", "r") as f:
            adjectives = f.read().splitlines()
        # get the animals
        with open("queueing/random_names/animals.txt", "r") as f:
            animals = f.read().splitlines()

        # get a random adjective and animal
        adjective = random.choice(adjectives)

        # get random animal that starts with the first letter of the adjective
        animals_ = [animal for animal in animals if animal[0] == adjective[0]]

        animal = random.choice(animals_)
        # create a username
        username = adjective + " " + animal
        request.session["anonymous"] = True
        print("user not in dashboard!")

    # create a listener object with token
    listener, created = Listener.objects.get_or_create(
        name=username,
    )
    if created:
        try:
            subject = "New Listener"
            html_message = "<h1>Someone signed up!</h1>"
            html_message += "<p>Email: " + str(username) + "</p>"
            from_email = config("EMAIL_HOST_USER")
            to_email = config("EMAIL_HOST_USER")
            send_mail(
                subject, html_message, from_email, [to_email], html_message=html_message
            )
        except:
            print("email failed to send")
    if not_in_dashboard:
        listener.anon = True
    listener.token = token
    listener.refresh_token = token_info["refresh_token"]
    listener.expires_at = token_info["expires_at"]
    listener.save()

    request.session["IAmDJ"] = username
    request.session.set_expiry(60 * 60 * 24 * 365 * 10)  # expire in ten year
    return HttpResponseRedirect(reverse("home"))
