from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from queueing.views import views, SMS, ajax 

urlpatterns = [
    path("", views.home, name="home"),
    path('spotify/connect-link/', views.spotify_connect_link, name="spotify_connect_link"),
    path('ajax/follow-dj/', ajax.follow_dj, name="follow_dj"),
    path('ajax/queue/', ajax.queue, name="queue"),
    path('ajax/shuffle/', ajax.shuffle, name="shuffle"),
    path('ajax/get-djs/', ajax.get_djs, name="get_djs"),
    path("redirect/", views.sp_redirect),
    path("sms/", SMS.SMS.as_view()),
    path("sms-failed/", SMS.sms_failed),
    path("send/", SMS.send.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
