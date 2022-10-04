# these utilities have to do with the spotify api/client
import spotipy
from spotipy.exceptions import SpotifyException
from queueing.utils.constants import sp_oauth


# this function returns the spotify client which can execute commands on behalf of the user
# naively, we just test if the client is working, if it doesn't work we try to refresh the token
# then, we return the client not knowing if it worked or not
def get_spotify_client(listener):
    # misconfig db
    if not listener.token:
        return None
    sp = spotipy.Spotify(auth=listener.token)
    try:
        # hit api to see if token works
        sp.me()
    except SpotifyException as e:
        print("there was an error trying to connect with spotify", e)
        print("requesting a new access_token using the refresh_token")
        # get new token from refresh token
        token_info = sp_oauth.refresh_access_token(listener.refresh_token)
        # update listener with new token info
        listener.token = token_info["access_token"]
        listener.refresh_token = token_info["refresh_token"]
        listener.expires_at = token_info["expires_at"]
        listener.save()
        sp = spotipy.Spotify(auth=listener.token)
    return sp
