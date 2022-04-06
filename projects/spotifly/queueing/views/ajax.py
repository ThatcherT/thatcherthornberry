from django.http import JsonResponse
from queueing.models import Listener


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
