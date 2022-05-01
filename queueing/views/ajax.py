from django.http import JsonResponse
from queueing.models import Listener
from queueing.utils.spotify import get_spotify_client
from queueing.utils.songs import get_uri_from_q, get_uri_from_song_name

def follow_dj(request):
    """
    Follow a dj
    """
    followingDJ = request.POST.get("followingDJ")
    Listener.objects.get(name=followingDJ)
    # save to session
    request.session["followingDJ"] = followingDJ
    return JsonResponse({'success': True})


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
    song = request.POST.get("song")
    dj = request.POST.get("dj")
    print('dj = ', dj)
    
    listener = Listener.objects.get(name=dj)

    sp = get_spotify_client(listener)
    uri = get_uri_from_song_name(song, sp)
    # add to queue
    try:
        sp.add_to_queue(uri, device_id=None)
        msg = 'We added {} to the queue!'.format(song)
    except Exception as e:
        print('there was an error trying to add to queue', e)
        msg = 'There was an error trying to add {} to the queue: {}'.format(song, e)
    return JsonResponse({'msg': msg})

def get_djs(request):
    """
    get the listener objects from the database
    """
    djs = Listener.objects.all()
    djs_list = []
    for dj in djs:
        djs_list.append(dj.name)
    return JsonResponse({'djs': djs_list})
