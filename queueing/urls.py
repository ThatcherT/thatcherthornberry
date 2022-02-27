from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from queueing import views

urlpatterns = [
    path("", views.home, name="home"),
    path("home/", views.home, name="home"),
    path("home/<dj>/", views.home, name="home"),
    path("sms/", views.SMS.as_view()),
    path("sms-failed/", views.sms_failed),
    path("redirect/", views.sp_redirect),
    path("register/<code>/", views.register, name="register"),
    path("send/", views.send.as_view()),
    path("queue/", views.queue, name="queue"),
    path("choose-dj/", views.choose_dj, name="choose-dj"),
    path("shuffle/", views.shuffle, name="shuffle"),
    path('auth/<listener_name>/', views.auth, name='auth'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
