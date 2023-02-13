from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("posts/<str:slug>", views.article, name="post"),
]
