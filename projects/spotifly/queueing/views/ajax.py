from django.http import JsonResponse
from queueing.models import Listener
from queueing.utils.spotify import get_spotify_client
from queueing.utils.songs import get_uri_from_q, get_uri_from_song_name, get_song_matches


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
    sp = get_spotify_client(listener)
    # get list of songs
    song_lst = get_song_matches(song, sp)
    return JsonResponse({'song_lst': song_lst})


def unfollow_dj(request):
    """
    Unfollow a dj
    """
    request.session.pop("followingDJ")
    return JsonResponse({'success': True})


def follow_dj(request):
    """
    Follow a dj
    """
    followingDJ = request.POST.get("followingDJ")
    Listener.objects.get(name=followingDJ)
    # save to session
    request.session["followingDJ"] = followingDJ
    request.session.set_expiry(60*60*24*365*10)  # expire in ten year
    return JsonResponse({'followingDJ': followingDJ})


def shuffle(request):
    """
    Shuffle the playlist
    """
    IAmDJ = request.POST.get('IAmDJ')
    listener = Listener.objects.get(name=IAmDJ)
    listener.shuffle()
    return JsonResponse({'success': True})


def queue(request):
    """
    Queue song, pass dj parameter and song title
    """
    uri = request.POST.get("uri")
    dj = request.POST.get("dj")

    listener = Listener.objects.get(name=dj)

    sp = get_spotify_client(listener)
    # add to queue
    try:
        sp.add_to_queue(uri, device_id=None)
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


def get_djs(request):
    """
    get the listener objects from the database
    """
    djs = Listener.objects.all()
    djs_list = []
    for dj in djs:
        djs_list.append(dj.name)
    return JsonResponse({'djs': djs_list})
