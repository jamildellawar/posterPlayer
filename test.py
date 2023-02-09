import spotipy
from spotipy.oauth2 import SpotifyOAuth
from time import sleep

DEVICE_ID="684d1697e3deb93b5a07afe11b468e1416a926de"
CLIENT_ID="72dc9b1300b5426d844363d7cd55a9a4"
CLIENT_SECRET="714704b00c694161811da07eb4187b98"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                client_secret=CLIENT_SECRET,
                                                redirect_uri="http://localhost:8080",
                                                scope="user-read-playback-state,user-modify-playback-state"))


# sp.start_playback(device_id=DEVICE_ID, context_uri='spotify:album:7ycBtnsMtyVbbwTfJwRjSP')


print(sp.playlist("2vMhJgtldJSxZl3hrdAam0")['owner'])