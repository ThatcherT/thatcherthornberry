from decouple import config
import spotipy


sp_oauth = spotipy.oauth2.SpotifyOAuth(
    config("SPOTIFY_CLIENT_ID"),
    config("SPOTIFY_CLIENT_SECRET"),
    config("SPOTIFY_REDIRECT_URI"),
    scope=[
        "user-library-read",
        "user-read-playback-state",
        "user-modify-playback-state",
        "user-read-currently-playing",
        "user-read-recently-played",
    ],
)