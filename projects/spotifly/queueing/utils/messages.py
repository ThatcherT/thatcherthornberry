from decouple import config
from twilio.twiml.messaging_response import MessagingResponse
from rest_framework.response import Response
from django.http import HttpResponse
from queueing.models import Listener, Follower
from rest_framework import status
from spotipy.exceptions import SpotifyException

from queueing.utils.constants import sp_oauth
from queueing.utils.spotify import get_spotify_client
from queueing.utils.songs import get_uri_from_q, queue_50_songs


def register_message():
    register_msg = (
        f"Please visit this link to authenticate: {sp_oauth.get_authorize_url()}"
    )
    return reply_msg(register_msg)


def follow_message(message_body, from_number):
    # get user from database
    following = message_body.partition(" ")[-1]
    # get user
    print("Trying to follow: ", following)
    try:
        user = Listener.objects.get(name=following)
    # TODO: use django's ObjectDoesNotExist exception
    except:
        err_msg = f"`{following}` doesn't exist. They need to visit http://spotifly.thatcherthornberry.com"
        return reply_msg(err_msg)

    # found user, creating/getting follower object

    follower, _ = Follower.objects.get_or_create(number=from_number)

    follower.following = following
    follower.save()

    follower_msg = f"You are now following {follower.following}. Add a track to their queue by texting 'queue let it happen by tame impala' or 'queue lose yourself to dance'. You get the idea."
    return reply_msg(follower_msg)


def album_mix_message(message_body, from_number):
    # TODO: finish this function and return message
    # get Listener from database
    try:
        listener = Listener.objects.get(number=from_number)
    except:
        err_msg = "You need to register first. Text `register` to get started."
        return reply_msg(err_msg)

    albums = message_body.lower()[4:]  # remove 'mix' and space
    album_lst = albums.split(" and ")

    for album in album_lst:
        try:
            # get album from spotify api
            sp = get_spotify_client(listener)
            results = sp.search(q=album, type="album", market="US")
            album_id = results["albums"]["items"][0]["id"]

            # get list of songs from album
            album_tracks = sp.album_tracks(album_id)
            album_tracks = album_tracks["items"]
        except:
            err_msg = f"`{album}` doesn't exist. They need to visit http://spotifly.thatcherthornberry.com"
            print("Error: ", err_msg)


def shuffle_message(from_number):
    # get Listener from database
    try:
        listener = Listener.objects.get(number=from_number)
    except:
        err_msg = "You need to register first. Text `register` to get started."
        return reply_msg(err_msg)

    sp = get_spotify_client(listener)

    queue_50_songs(sp, listener)

    shuffled_msg = f"We shuffled some songs for you. Enjoy!"
    return reply_msg(shuffled_msg)


def queue_message(message_body, from_number):
    # get follower object from phone nummber
    follower, _ = Follower.objects.get_or_create(number=from_number)
    if not follower.following:
        not_following_msg = f"It appears you aren't following anybody... Try 'follow thatcher'. Or, ask the person what their username is."
        return reply_msg(not_following_msg)

    else:
        listener = Listener.objects.get(name=follower.following)
        if not listener.token:
            missing_token_msg = f"It appears the person you're following hasn't authenticated their account yet. Tell them to visit http://spotifly.thatcherthornberry.com or, if they've done that, tell them to text register to 424-373-5305."
            return reply_msg(missing_token_msg)

    # find track and add to queue
    sp = get_spotify_client(listener)
    uri, uri_lst = get_uri_from_q(message_body, sp)

    # add to queue
    try:
        sp.add_to_queue(uri, device_id=None)
    except SpotifyException as e:
        if "No active device" in e.msg:
            msg = f"It appears {follower.following} is not listening to music right now. Give them the AUX."
            return reply_msg(msg)
        else:
            # some other error must of occured
            unknown_error_msg = f"An unknown error occured! Please try again."
            return reply_msg(unknown_error_msg)

    song = uri_lst[0]
    song_name = song["name"]
    song_artist = song["artists"][0]["name"]
    song_album = song["album"]["name"]

    queue_msg = f"Added `{song_name}` by `{song_artist}` from their album `{song_album}` to `{follower.following}'s` queue."
    return reply_msg(queue_msg)


def idk_message():
    msg = (
        "Sorry. I didn't understand that. The commands are register, follow, and queue."
    )
    return reply_msg(msg)


def reply_msg(msg):
    LOCAL = config("LOCAL", default=False)
    if not LOCAL:
        resp = MessagingResponse()
        resp.message(msg)
        return HttpResponse(str(resp))
    return Response(status=status.HTTP_200_OK)



