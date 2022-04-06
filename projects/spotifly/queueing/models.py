from django.db import models
import spotipy

from queueing.utils.spotify import get_spotify_client
from queueing.utils.songs import get_uri_from_song_artist, queue_50_songs


class Listener(models.Model):
    name = models.CharField(max_length=50, unique=True)
    spotify_id = models.CharField(
        max_length=100, unique=True, blank=True, null=True)
    token = models.TextField(blank=True, null=True)
    refresh_token = models.TextField(blank=True, null=True)
    expires_at = models.TextField(blank=True, null=True)
    number = models.CharField(
        max_length=10, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(blank=True, null=True)
    max_offset = models.IntegerField(default=5000)

    def __str__(self):
        return self.name

    def queue_song(self, song, artist=None):
        # use spotify api to queue song to activate device
        # get oauth to take care of tokens and refresh
        sp = get_spotify_client(self)

        # unique identifier for song
        uri, uri_lst = get_uri_from_song_artist(song, artist, sp)

        # if uri is a string, return it
        if not uri_lst:
            return uri

        # queue song
        sp.add_to_queue(uri, device_id=None)

        song = uri_lst[0]
        song_name = song["name"]
        song_artist = song["artists"][0]["name"]
        success_msg = f"We queued {song_name} by {song_artist} on {self.name}'s device."
        return success_msg

    def shuffle(self):
        sp = get_spotify_client(self)
        queue_50_songs(sp, self)
        return


class Follower(models.Model):
    number = models.CharField(max_length=10, unique=True)
    following = models.CharField(
        max_length=50, default="thatcher"
    )  # corresponds to name
    following_spotify_id = models.CharField(
        max_length=100, null=True, blank=True)
    promo = models.BooleanField(default=False)

    def __str__(self):
        return self.number + " following " + self.following
