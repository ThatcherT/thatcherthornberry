import spotipy
from decouple import config
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


def spotify_connect_link(request):
    """
    return the link users can use to authenticate with spotify
    """
    # get secrets from env with decouple
    client_id = config("SPOTIFY_CLIENT_ID")
    redirect_uri = config("SPOTIFY_REDIRECT_URI")
    scopes = "user-read-private user-read-email"
    url = f'https://accounts.spotify.com/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&scope={scopes}'
    # send url in json response
    return JsonResponse({'url': url})


def sp_redirect(request):
    """
    Use the client authorization code flow to get a token to make requests on behalf of the user
    Store that token and associate it with the listener.
    Spotify redirects users to this view after they have authenticated with spotify.
    """
    # get code from url
    url = request.build_absolute_uri()
    code = url.split("?code=")[1]

    # parse token from code
    token_info = sp_oauth.get_access_token(code)
    token = token_info["access_token"]

    # get spotify username with token
    sp = spotipy.Spotify(token)
    user = sp.current_user()
    username = user["id"]

    # create a listener object with token
    listener, created = Listener.objects.get_or_create(
        name=username,
    )
    listener.token = token
    listener.refresh_token = token_info["refresh_token"]
    listener.expires_at = token_info["expires_at"]
    listener.save()
    request.session["IAmDJ"] = username
    return HttpResponseRedirect(reverse("home"))
