import spotipy
from spotipy.oauth2 import SpotifyOAuth
from time import sleep

DEVICE_ID="XXX"
CLIENT_ID="XXX"
CLIENT_SECRET="XXX"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                client_secret=CLIENT_SECRET,
                                                redirect_uri="http://localhost:8080",
                                                scope="user-read-playback-state,user-modify-playback-state"))


# sp.start_playback(device_id=DEVICE_ID, context_uri='spotify:album:7ycBtnsMtyVbbwTfJwRjSP')


print(sp.playlist("2vMhJgtldJSxZl3hrdAam0")['owner'])