import random


def get_song_matches(song, sp):
    q = "track:" + song
    uri_lst = sp.search(q=q, type="track", market="US")["tracks"]["items"]
    return uri_lst


def get_uri_from_song_artist(song, artist, sp):
    # todo refactor uri_lst to better name
    q = ""
    if artist:
        q += "artist:" + artist + " "
    q += "track:" + song
    print('searching for: ' + q)
    uri_lst = sp.search(q=q, type="track", market="US")["tracks"]["items"]
    if len(uri_lst) == 0:
        uri_lst = sp.search(q=song, type="track", market="US")[
            "tracks"]["items"]
        if len(uri_lst) == 0:
            no_results_msg = f"No results found for `{song} by {artist}`. Try again."
            # if there are no results,  guess we should return a string saying so
            return no_results_msg, None  # return two variables so things work
    uri = uri_lst[0]["id"]
    return uri, uri_lst


# gets the first song URI that shows up from search
def get_uri_from_song_name(song, sp):
    return sp.search(q=f'track: {song}', type="track", market="US")["tracks"]["items"][0]["id"]


def get_uri_from_q(message_body, sp):
    track_by_artist = message_body.partition(" ")[-1]
    if "by" in track_by_artist:
        track_by_artist = track_by_artist.split(" by ")
        track = track_by_artist[0]
        artist = track_by_artist[1]
        q = "artist:" + artist + " track:" + track
    else:
        track = track_by_artist
        q = "track:" + track
    print('searching for: ' + q)
    uri_lst = sp.search(q=q, type="track", market="US")["tracks"]["items"]
    if len(uri_lst) == 0:
        uri_lst = sp.search(q=track_by_artist, type="track", market="US")["tracks"][
            "items"
        ]
        if len(uri_lst) == 0:
            uri_lst = sp.search(q=track, type="track", market="US")[
                "tracks"]["items"]
            if len(uri_lst) == 0:
                no_results_msg = f"No results found for `{track_by_artist}`. Try again."
                # TODO im pretty sure I broke this while refactoring...
                return no_results_msg, None
    uri = uri_lst[0]["id"]
    return uri, uri_lst


# queue 50 random songs
def queue_50_songs(sp, listener):
    for _ in range(50):
        # init empty list to queue next song
        song = []
        while song == []:
            random_offset = random.randint(
                0, listener.max_offset
            )  # get a random song between 0 and current known max offset
            results = sp.current_user_saved_tracks(
                limit=1, offset=random_offset)
            song = list(results["items"])
            if song == []:
                # max_offset is too high rebase it at one under current random offset
                listener.max_offset = random_offset - 1
                listener.save()
            else:
                # iterate through lst
                for item in song:
                    # get uri of songs
                    uri = item["track"]["uri"]
                    # queue each song
                    sp.add_to_queue(uri, device_id=None)
