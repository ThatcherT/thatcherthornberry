import spotipy
from decouple import config
from django.http import JsonResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from queueing.models import Listener
from queueing.utils.constants import sp_oauth
from django.core.mail import send_mail


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
    request.session.set_expiry(60*60*24*365*10) # expire in ten year
    return redirect(reverse("home"))


def spotify_connect_link(request):
    """
    return the link users can use to authenticate with spotify
    """
    # get secrets from env with decouple
    client_id = config("SPOTIFY_CLIENT_ID")
    redirect_uri = config("SPOTIFY_REDIRECT_URI")
    scopes = "user-read-private user-read-email user-library-read user-read-playback-state user-modify-playback-state user-read-currently-playing user-read-recently-played"
    url = f'https://accounts.spotify.com/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&scope={scopes}'
    # send url in json response
    return JsonResponse({'url': url})


def sp_redirect(request):
    """
    Use the client authorization code flow to get a token to make requests on behalf of the user
    Store that token and associate it with the listener.
    Spotify redirects users to this view after they have authenticated with spotify.
    """
    print('redirect to sp_redirect')
    # get code from url
    url = request.build_absolute_uri()
    print(url)
    code = url.split("?code=")[1]

    # parse token from code
    token_info = sp_oauth.get_access_token(code)
    token = token_info["access_token"]

    # get spotify username with token
    sp = spotipy.Spotify(token)
    user = sp.current_user()
    print('user log in', user)
    username = user["id"]
    
    

    # create a listener object with token
    listener, created = Listener.objects.get_or_create(
        name=username,
    )
    if created:
        print('created listener', listener)
        subject = "New Listener"
        html_message = "<h1>Someone signed up!</h1>"
        html_message += "<p>Email: " + str(user) + "</p>"
        from_email = config("EMAIL_FROM_USER")
        to_email = "thatcherthornberry@gmail.com"
        send_mail(subject, html_message, from_email, [to_email], html_message=html_message)


    listener.token = token
    listener.refresh_token = token_info["refresh_token"]
    listener.expires_at = token_info["expires_at"]
    listener.save()
    request.session["IAmDJ"] = username
    request.session.set_expiry(60*60*24*365*10) # expire in ten year
    return HttpResponseRedirect(reverse("home"))
