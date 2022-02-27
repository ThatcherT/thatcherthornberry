# these utilities have to do with the spotify api/client
import spotipy
from spotipy.exceptions import SpotifyException
from queueing.utils.constants import sp_oauth

def get_spotify_client(listener):
    sp = spotipy.Spotify(auth=listener.token)
    try:
        # hit api to see if token works
        sp.me()
    except SpotifyException as e:
        # get new token from refresh token
        token_info = sp_oauth.refresh_access_token(listener.refresh_token)
        # update listener with new token info
        listener.token = token_info["access_token"]
        listener.refresh_token = token_info["refresh_token"]
        listener.expires_at = token_info["expires_at"]
        listener.save()
        sp = spotipy.Spotify(auth=listener.token)
    return sp