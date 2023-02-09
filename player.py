from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from time import sleep
import json

f = open('/home/posterplayer/Documents/posterPlayer/data.json')
data = json.load(f)
f.close()



DEVICE_ID="684d1697e3deb93b5a07afe11b468e1416a926de"
CLIENT_ID="72dc9b1300b5426d844363d7cd55a9a4"
CLIENT_SECRET="714704b00c694161811da07eb4187b98"

while True:
    try:
        reader=SimpleMFRC522()
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                       client_secret=CLIENT_SECRET,
                                                       redirect_uri="http://localhost:8080",
                                                       scope="user-read-playback-state,user-modify-playback-state",
                                                       cache_path="/home/posterplayer/Documents/posterPlayer/.cache"))

        # create an infinite while loop that will always be waiting for a new scan
        while True:
            print("Waiting for record scan...")
            id= reader.read()[0]
            print("Card Value is:",id)

            if (id==635033444568):
                # skip to next track
                sp.next_track(device_id=DEVICE_ID)
            elif (id==906337804359):
                # change shuffle settings
                shuffle = not shuffle
                sp.shuffle(shuffle, device_id=DEVICE_ID)
            elif (id in data['IDs']):
                sp.transfer_playback(device_id=DEVICE_ID, force_play=False)
                # playing another album
                newAlbum = data['Albums'][str(id)]
                sp.start_playback(device_id=DEVICE_ID, context_uri='spotify:' + newAlbum['Spotify ID'])
                print("Now playing " + newAlbum['Album Name'] + "by" + newAlbum['Artist'])
                sleep(2)
            else:
                print("This is not a registered RFID sticker.")
                sleep(2)

    # if there is an error, skip it and try the code again (i.e. timeout issues, no active device error, etc)
    except Exception as e:
        print(e)
        pass

    finally:
        print("Cleaning  up...")
        GPIO.cleanup()
