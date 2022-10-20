from django.urls import path
from queueing.views import views, ajax

urlpatterns = [
    # website stuff
    path("", views.home, name="home"),
    path("invite-link/<str:username>/", views.invite_link, name="invite_link"),
    # ajax requests
    path("ajax/follow-dj/", ajax.follow_dj, name="follow_dj"),
    path("ajax/unfollow-dj/", ajax.unfollow_dj, name="unfollow_dj"),
    path("ajax/queue/", ajax.queue, name="queue"),
    path("ajax/search/", ajax.search, name="search"),
    path("ajax/suggest/", ajax.suggest, name="suggest"),
    path("ajax/shuffle/", ajax.shuffle, name="shuffle"),
    path("ajax/session/", ajax.session, name="session"),
    path("ajax/queue-mgmt/", ajax.queue_mgmt, name="queue_mgmt"),
    path("ajax/get-djs/", ajax.get_djs, name="get_djs"),
    path("ajax/now-playing/", ajax.now_playing, name="now_playing"),
    # spotify web api
    path("redirect/", views.sp_redirect),
    path(
        "spotify/connect-link/", views.spotify_connect_link, name="spotify_connect_link"
    ),
]
