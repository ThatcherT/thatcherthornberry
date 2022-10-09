from django.http import JsonResponse
from queueing.models import Listener
from queueing.utils.songs import get_suggested_songs, get_song_matches


def search(request):
    """
    Search for a song
    """
    # get dj from session
    dj = request.session.get("followingDJ")
    listener = Listener.objects.get(name=dj)
    # get search term
    song = request.POST.get("song")
    # get spotify client
    sp = listener.sp_client.sp
    # get list of songs
    song_lst = get_song_matches(song, sp)
    return JsonResponse({"song_lst": song_lst})


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


def now_playing(request):
    """
    Return Spotify Song Obj for song that is playing
    """
    listener = Listener.objects.get(name=request.POST["dj"])
    sp = listener.sp_client.sp
    if not sp:
        return JsonResponse({"success": False, "error": "no spotify client"})
    songObj = sp.current_user_playing_track()
    # this gets something interesting.. like the duration left I believe
    # playback = sp.current_playback()
    return JsonResponse({"songObj": songObj["item"] if songObj else None})


def unfollow_dj(request):
    """
    Unfollow a dj
    """
    request.session.pop("followingDJ")
    return JsonResponse({"success": True})


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


def shuffle(request):
    """
    Shuffle the playlist
    """
    IAmDJ = request.POST.get("IAmDJ")
    listener = Listener.objects.get(name=IAmDJ)
    listener.shuffle()
    return JsonResponse({"success": True})


def start_session(request):
    """
    Start a session for a dj
    """
    IAmDJ = request.POST.get("IAmDJ")
    listener = Listener.objects.get(name=IAmDJ)
    listener.start_session()
    return JsonResponse({"success": True})


def queue(request):
    """
    Queue song, pass dj parameter and song title
    """
    uri = request.POST.get("uri")
    dj = request.POST.get("dj")

    listener = Listener.objects.get(name=dj)
    if listener.session_active:
        listener.q_mgmt.queue_add(uri)
        return JsonResponse({"success": True})

    else:
        listener.queue_song(uri)
        return JsonResponse({"success": True})


def get_djs(request):
    """
    get the listener objects from the database
    """
    djs = Listener.objects.all()
    djs_list = []
    for dj in djs:
        djs_list.append(dj.name)
    return JsonResponse({"djs": djs_list})
