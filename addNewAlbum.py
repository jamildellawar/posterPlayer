from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from time import sleep
import json

DEVICE_ID="684d1697e3deb93b5a07afe11b468e1416a926de"
CLIENT_ID="72dc9b1300b5426d844363d7cd55a9a4"
CLIENT_SECRET="714704b00c694161811da07eb4187b98"



while True:
    try:
        reader=SimpleMFRC522()
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                       client_secret=CLIENT_SECRET,
                                                       redirect_uri="http://localhost:8080",
                                                       scope="user-read-playback-state,user-modify-playback-state"))

        # create an infinite while loop that will always be waiting for a new scan
        while True:
            f = open('data.json')
            data = json.load(f)
            f.close()

            print("Waiting for new RFID to be scanned...")
            id= reader.read()[0]
            print("Card Value is:",id)
            if id == 635033444568 or id == 906337804359:
                print("This ID is either the skip or shuffle RFID. We cannot change this")

            elif id in data["IDs"]:
                currentID = data["Items"][str(id)]
                print("This ID is already being used. Would you like to replace this value?")
                print("Currently, it is linked to " + currentID["Item Name"] + " by " + currentID["Creator"])
                if input("Please enter (y/n)") == "y":
                    print("Please enter the Spotify Album URL that you'd like to link to this RFID sticker.")
                    spotifyAlbumURL = input()
                    spotifyAlbumID = spotifyAlbumURL.split("/")[4].split("?")[0]
                    print("new spotify album id")
                    print(spotifyAlbumID)
                    with open('data.json', 'r') as f:
                        new_data = data

                        # Change Album ID
                        new_data['Items'][str(id)]['Spotify ID'] = spotifyAlbumID
                        albumInfo = sp.album(spotifyAlbumID)

                        # Change Album Name
                        new_data['Items'][str(id)]['Album Name'] = albumInfo['name']

                        # Change Album Artist Names
                        artists_typed = ""
                        artist_ids = []
                        if len(albumInfo['artists']) == 1:
                            artists_typed = albumInfo['artists'][0]['name']
                        elif len(albumInfo['artists']) == 2:
                            artists_typed = albumInfo['artists'][0]['name'] + " and " + albumInfo['artists'][1]['name']
                        else:
                            for artist in albumInfo['artists'][:-1]:
                                artists_typed += artist['name'] + ', ' 
                            artists_typed += "and " + albumInfo['artists'][-1]['name']
                    
                        new_data['Items'][str(id)]['Artist'] = artists_typed
                    
                    with open('data.json', "w") as f:
                        json.dump(new_data, f, indent = 4)
                    print("Done")
            else:
                print("Please enter the Spotify URL that you'd like to link to this RFID sticker.")
                spotifyURL = input()
                spotifyID = spotifyURL.split("/")[4].split("?")[0]
                try:
                    itemInfo = sp.album(spotifyID)
                    ifAlbum = True
                except Exception:
                    itemInfo = sp.playlist(spotifyID)
                    ifAlbum = False

                if ifAlbum:
                    artists_typed = ""
                    artist_ids = []
                    if len(itemInfo['artists']) == 1:
                        artists_typed = itemInfo['artists'][0]['name']
                    elif len(itemInfo['artists']) == 2:
                        artists_typed = itemInfo['artists'][0]['name'] + " and " + itemInfo['artists'][1]['name']
                    else:
                        for artist in itemInfo['artists'][:-1]:
                            artists_typed += artist['name'] + ', ' 
                        artists_typed += "and " + itemInfo['artists'][-1]['name']
                    creator = artists_typed
                else:
                    creator = itemInfo['creator']

                with open('data.json', 'r') as f:
                    data = json.load(f)
                    new_data = data
                    new_data["IDs"].append(id)
                    new_data["Items"][str(id)] = {
                        "Spotify ID": spotifyID,
                        "Item Name": albumInfo['name'],
                        "Creator": artists_typed
                    }

                with open('data.json', 'w') as f:
                    json.dump(new_data, f, indent = 4)


            

    # if there is an error, skip it and try the code again (i.e. timeout issues, no active device error, etc)
    except Exception as e:
        print(e)
        pass

    finally:
        print("Cleaning  up...")
        GPIO.cleanup()
