from decouple import config
import spotipy


sp_oauth = spotipy.oauth2.SpotifyOAuth(
    config("SPOTIFY_CLIENT_ID"),
    config("SPOTIFY_CLIENT_SECRET"),
    config("SPOTIFY_REDIRECT_URI"),
    scope=[
        "user-read-private",
        "user-read-email" "user-library-read",
        "user-read-playback-state",
        "user-read-currently-playing",
        "user-modify-playback-state",
        "user-read-recently-played",
        "user-top-read",
    ],
)
