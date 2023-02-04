import spotipy
from decouple import config

SCOPE="""
    user-read-private 
    user-read-email 
    user-library-read 
    user-read-playback-state 
    user-read-currently-playing 
    user-modify-playback-state 
    user-read-recently-played 
    user-top-read 
    user-read-playback-position 
    playlist-modify-public 
    playlist-modify-private
    """
    

sp_oauth = spotipy.oauth2.SpotifyOAuth(
    config("SPOTIFY_CLIENT_ID"),
    config("SPOTIFY_CLIENT_SECRET"),
    config("SPOTIFY_REDIRECT_URI"),
    scope=SCOPE,
    
)
