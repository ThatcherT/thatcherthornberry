from decouple import config
import spotipy


sp_oauth = spotipy.oauth2.SpotifyOAuth(
    config("SPOTIPY_CLIENT_ID"),
    config("SPOTIPY_CLIENT_SECRET"),
    config("SPOTIPY_REDIRECT_URI"),
    scope=[
        "user-library-read",
        "user-read-playback-state",
        "user-modify-playback-state",
        "user-read-currently-playing",
        "user-read-recently-played",
    ],
)