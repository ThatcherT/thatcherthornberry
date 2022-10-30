import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from queueing.models import Listener
from queueing.utils.songs import get_song_matches, get_suggested_songs


@csrf_exempt
def search(request):
    """
    Search for a song
    """
    # get dj from session
    following_dj = request.session.get("followingDJ")
    listener = Listener.objects.get(name=following_dj)
    # get search term
    song = request.POST.get("song")
    # get spotify client
    sp = listener.sp_client.sp
    # get list of songs
    song_lst = get_song_matches(song, sp)
    return JsonResponse({"song_lst": song_lst})


@csrf_exempt
def suggest(request):
    """
    Use the signed in user to find a song they would like
    """
    iam = request.GET.get("iam")
    listener = Listener.objects.get(name=iam)
    # get spotify client
    sp = listener.sp_client.sp
    # get songs they like
    song_lst = get_suggested_songs(sp)
    return JsonResponse({"song_lst": song_lst})


@csrf_exempt
def now_playing(request):
    """
    Return Spotify Song Obj for song that is playing
    """
    print("getting dj")
    following_dj = request.session.get("followingDJ")
    print("getting listener", following_dj)
    listener = Listener.objects.get(name=following_dj)
    sp = listener.sp_client.sp
    if not sp:
        return JsonResponse({"success": False, "error": "no spotify client"})
    songObj = sp.current_user_playing_track()
    # this gets something interesting.. like the duration left I believe
    # playback = sp.current_playback()
    return JsonResponse({"songObj": songObj["item"] if songObj else None})


@csrf_exempt
def unfollow_dj(request):
    """
    Unfollow a dj
    """
    request.session.pop("followingDJ")
    return JsonResponse({"success": True})


@csrf_exempt
def follow_dj(request):
    """
    Follow a dj
    """
    followingDJ = request.POST.get("followingDJ")
    Listener.objects.get(name=followingDJ)
    # save to session
    request.session["followingDJ"] = followingDJ
    request.session.set_expiry(60 * 60 * 24 * 365 * 10)  # expire in ten year
    return JsonResponse({"followingDJ": followingDJ})


@csrf_exempt
def shuffle(request):
    """
    Shuffle the playlist
    """
    IAmDJ = request.POST.get("IAmDJ")
    listener = Listener.objects.get(name=IAmDJ)
    listener.shuffle()
    return JsonResponse({"success": True})


@csrf_exempt
def session(request):
    """
    Start a session for a dj
    """
    IAmDJ = request.POST.get("IAmDJ")
    stopSession = request.POST.get("stop")
    listener = Listener.objects.get(name=IAmDJ)
    if stopSession:
        listener.stop_session()
        return JsonResponse({"success": True})
    listener.start_session()
    return JsonResponse({"success": True})


@csrf_exempt
def queue_mgmt(request):
    """
    Return the queue management object
    """
    dj = request.POST.get("dj")
    try:
        listener = Listener.objects.get(name=dj)
    except Listener.DoesNotExist:
        return JsonResponse({"q_mgmt": {}})
    return JsonResponse({"q_mgmt": listener.q_mgmt.queue_mgmt})


@csrf_exempt
def vote_song(request):
    dj = request.POST.get("dj")
    listener = Listener.objects.get(name=dj)
    listener.q_mgmt.queue_vote(request.POST.get("songUri"))
    return JsonResponse({"q_mgmt": listener.q_mgmt.queue_mgmt})


@csrf_exempt
def queue(request):
    """
    Queue song, pass dj parameter and song title
    """
    song_object = request.POST.get("songObj")
    # convert json string to python dict
    song_object = json.loads(song_object)
    uri = song_object["uri"]
    dj = request.POST.get("dj")

    listener = Listener.objects.get(name=dj)
    if listener.session_active:
        listener.q_mgmt.queue_add(song_object)
        return JsonResponse({"success": True})

    else:
        listener.queue_song(uri)
        return JsonResponse({"success": True})


@csrf_exempt
def playlists(request):
    """
    Get the playlists for the user
    """
    iam = request.GET.get("IAmDJ")
    listener = Listener.objects.get(name=iam)
    # get spotify client
    sp = listener.sp_client.sp
    playlists = sp.current_user_playlists()
    print(playlists["items"])
    return JsonResponse({"playlists": playlists["items"]})


@csrf_exempt
def get_djs(request):
    """
    get the listener objects from the database
    """
    djs = Listener.objects.all().filter(anon=False)
    djs_list = [dj.name for dj in djs]
    return JsonResponse({"djs": djs_list})
