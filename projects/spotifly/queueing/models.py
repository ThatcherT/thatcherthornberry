import json
from datetime import datetime

import django_redis
import django_rq
import spotipy
from django.db import models
from spotipy.exceptions import SpotifyException

from queueing.utils.constants import sp_oauth
from queueing.utils.songs import queue_50_songs

scheduler = django_rq.get_scheduler("default")
cache = django_redis.get_redis_connection("default")
queue = django_rq.get_queue("default")


class Listener(models.Model):

    name = models.CharField(max_length=50, unique=True)
    spotify_id = models.CharField(max_length=100, unique=True, blank=True, null=True)
    token = models.TextField(blank=True, null=True)
    refresh_token = models.TextField(blank=True, null=True)
    expires_at = models.TextField(blank=True, null=True)
    number = models.CharField(max_length=10, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(blank=True, null=True)
    max_offset = models.IntegerField(default=5000)

    @property
    def q_mgmt(self):
        """Return a QueueMgmt object for this listener"""
        return self.QueueMgmt(self)

    @property
    def sp_client(self):
        """Return a SpotifyClient object for this listener"""
        return self.SpotifyClient(self)

    @property
    def playback(self):
        # get current playback
        sp = self.sp_client.sp
        try:
            playback = sp.current_playback()
            current_uri = playback["item"]["uri"]
            return current_uri
        except:
            return None

    def __str__(self):
        return self.name

    @property
    def session_active(self):
        """Check if a session is active"""
        for j in scheduler.get_jobs():
            if j.id == self.name:
                return True
        return False

    def queue_song(self, track_uri):
        """Add a song to the redis queue"""
        sp = self.sp_client.sp
        try:
            sp.add_to_queue(track_uri, device_id=None)
        except SpotifyException as e:
            print(e)

    def shuffle(self):
        sp = self.sp_client.sp
        queue_50_songs(sp, self)
        return

    def start_session(self):
        """Start a session. A session is a repeated job which checks playback periodically and decides when to queue the next song."""
        # delete existing with id if exists
        print('Let the Seshing Begin!')
        for j in scheduler.get_jobs():
            if j.id == self.name:
                scheduler.cancel(j)
        # delete existing redis queue
        cache.delete(self.name)
        
        scheduler.schedule(
            scheduled_time=datetime.now(),
            func=self.decide_to_queue,
            interval=10,  # seconds
            repeat=180,  # 3 hours
            id=self.name,
        )
    def stop_session(self):
        """Stop a session"""
        print('Seshing no mo')
        for j in scheduler.get_jobs():
            if j.id == self.name:
                scheduler.cancel(j)
                break
        cache.delete(self.name)
        return False

    def decide_to_queue(self):
        playback = self.playback  # static copy
        if (
            playback == self.q_mgmt.queue_mgmt["current"]
            or self.q_mgmt.queue_mgmt["queue"] == {}
        ):
            # song is still playing or queue empty
            print('Decided not to queue')
            print('playback == current', playback == self.q_mgmt.queue_mgmt["current"])
            print('queue empty', self.q_mgmt.queue_mgmt["queue"] == {})
            return
        else:
            # song is done playing
            print('Decided to queue')
            print('playback == current', playback == self.q_mgmt.queue_mgmt["current"])
            print('queue empty', self.q_mgmt.queue_mgmt["queue"] == {})
            self.q_mgmt.queue_next()

    class SpotifyClient:
        def __init__(self, listener):
            self.listener = listener
            self._sp = spotipy.Spotify(auth=self.listener.token)

        @property
        def sp(self):
            """Get a spotify client for a listener, if token expired refresh"""
            if not self.listener.token:
                # TODO: handle this
                print("MISCONFIGURED_ACCOUNT")
                return None
            if float(self.listener.expires_at) < datetime.now().timestamp():
                print("REFRESHING_EXPIRED_TOKEN")
                self._update_token()
            try:
                # hit api to see if token works
                self._sp.me()
            except SpotifyException as e:
                print("there was an error trying to connect with spotify", e)
                # TODO: deprecate this
                self._update_token()
            return self._sp

        @sp.setter
        def sp(self, value):
            self._sp = value

        def _update_token(self):
            token_info = sp_oauth.refresh_access_token(self.listener.refresh_token)
            # update listener with new token info
            self.listener.token = token_info["access_token"]
            self.listener.refresh_token = token_info["refresh_token"]
            self.listener.expires_at = token_info["expires_at"]
            self.listener.save()
            self.sp = spotipy.Spotify(auth=self.listener.token)

    class QueueMgmt:
        """Manages the redis object which maps to listener.name"""

        def __init__(self, listener):
            """set listener, initialize q_mgmt in redis"""
            self.listener = listener
            # initialize the queue_mgmt object
            queue_mgmt_str = cache.get(self.listener.name)
            if not queue_mgmt_str:  # initialize if not
                # crucial as this will push changes to redis
                cache.set(
                    self.listener.name,
                    json.dumps(
                        {
                            "listener_name": self.listener.name,
                            "current": self.listener.playback,
                            "on_deck": "",
                            "queue": {},
                        }
                    ),
                )

        # too many subclases... no such thing
        class QueueMgmtObj(dict):
            """Necessary to add logic to dict item setters... a lesson learned the hard way"""

            class QueueObj(dict):
                def __setitem__(self, uri, value):
                    if not uri.startswith("spotify:track:"):
                        raise ValueError("Not a track uri")
                    if not value.get("listener_to"):
                        raise ValueError("No listener_to")
                    if not type(value.get("votes")) == int:
                        raise ValueError("No votes")
                    if not value.get("queued_time"):
                        raise ValueError("No queued_time")
                    super().update({uri: value})
                    # TODO: this is oviously a consequence of a poorly architected class structure
                    queue_mgmt = json.loads(cache.get(value["listener_to"]))
                    if queue_mgmt["on_deck"] == "":
                        queue_mgmt["on_deck"] = {uri: value}
                        # queue the song
                        listener = Listener.objects.get(name=value["listener_to"])
                        listener.queue_song(uri)
                    else:
                        queue_mgmt["queue"][uri] = value
                    cache.set(value["listener_to"], json.dumps(queue_mgmt))
                def __delitem__(self, key):
                    listener_name = self[key]["listener_to"]
                    queue_mgmt = json.loads(cache.get(listener_name))
                    del queue_mgmt["queue"][key]
                    cache.set(listener_name, json.dumps(queue_mgmt))
                    super().__delitem__(key)

            def __setitem__(self, key, value):
                if key == "on_deck":
                    listener = Listener.objects.get(name=self["listener_name"])
                    # get first key from value which is a dict
                    uri = list(value.keys())[0]
                    listener.queue_song(uri)
                # any changes to the queue_mgmt var will be saved to redis
                super().__setitem__(key, value)
                cache.set(self["listener_name"], json.dumps(self))

        @property
        def queue_mgmt(self):
            """Get queue_mgmt object from redis, don't forget those sub classes"""
            queue_mgmt = self.QueueMgmtObj(json.loads(cache.get(self.listener.name)))
            # the key queue is a dict, convert to seflf.QueueMgmtObj.QueueObj
            queue_mgmt["queue"] = self.QueueMgmtObj.QueueObj(queue_mgmt["queue"])
            return queue_mgmt

        def __repr__(self):
            return f"QueueMgmt for {self.listener.name}: {self.queue_mgmt}"

        def queue_next(self):
            """If the current song is done playing, set the top song from queue to on deck and then queue it"""
            # TODO: pretty sure this broke
            print('time to queue next :0))))')
            if self.listener.playback != self.queue_mgmt["on_deck"]:
                print("Somebody messed up.. I think the queue will be a bit ahead now")
            # update queue_mgmt
            self.queue_mgmt["current"] = self.listener.playback
            # get song with most votes, if equal votes, get earliest added from self.queue['queued_time]
            on_deck_uri = max(
                self.queue_mgmt["queue"],
                key=lambda x: (
                    self.queue_mgmt["queue"][x]["votes"],
                    -self.queue_mgmt["queue"][x]["queued_time"],
                ),
            )
            print('setting ')
            self.queue_mgmt["on_deck"] = {on_deck_uri:self.queue_mgmt["queue"][on_deck_uri]}
            # rm from queue
            del self.queue_mgmt["queue"][on_deck_uri]
            print('new queue mgmt', self.queue_mgmt['queue'].keys())

        def queue_add(self, song_object):
            """Add track with zero votes"""
            print('Adding to Queue!', song_object['uri'])
            # init song with 0 votes
            # HARD LESSON: the setter doesn't work for sub dicts :')
            track_uri = song_object["uri"]
            self.queue_mgmt["queue"][track_uri] = {
                "votes": 0,
                "queued_time": datetime.now().timestamp(),
                "song_object": song_object,
                "listener_from": "",
                "listener_to": self.listener.name,
            }

        def queue_vote(self, track_uri):
            """Vote for a song in the queue"""
            self.queue_mgmt["queue"][track_uri]["votes"] += 1
