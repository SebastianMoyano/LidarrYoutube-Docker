#!/usr/bin/env python
# -*- coding: utf-8 -*-
# import required modules 
import youtube_dl
import requests
import os

api_key = os.environ.get("API_KEY")
base_url = os.environ["BASE_URL"]
root_dir = os.environ["ROOT_DIR"]
puid = os.environ.get("PUID")
pgid = os.environ.get("PGID")

headers = { "X-Api-Key": api_key }

rootFolder =''
def youtube(artist,track,trackNumber):
    ydl = youtube_dl.YoutubeDL({})
    search_result = ydl.extract_info(
        'ytsearch:"'+artist+' - '+track+' VEVO'+'"',
        download=False  # We only want to extract the info
    )
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.chown(os.path.join(root_dir, artist, trackNumber + '. %(title)s.%(ext)s'), puid, pgid)
,
    }

   
    # Get the first video from the search result
    video = search_result['entries'][0]
    print(video['title'])
    if track.lower() in video['title'].lower():
       print(video['webpage_url'])
       with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video['webpage_url']])

def rescan_folder_in_lidarr(host, api_key, path):
    headers = { "X-Api-Key": api_key }
    rescan_url = f"{host}/api/v1/command"
    data = { "name": "RescanArtist", "artistId": path }
    response = requests.post(rescan_url, headers=headers, json=data)

    if response.status_code == 200:
        print("Rescan successfully initiated")
    else:
        print("Rescan failed with status code", response.status_code)


def get_tracks_with_hasFile(albumId,artist):
    tracks_url = f"{base_url}/track?albumId={albumId}"
    response = requests.get(tracks_url, headers=headers)
    tracks = response.json()
    for track in tracks:

        if track['hasFile'] == False:
            print(track)
            print(track['title'],' by ',artist)
            youtube(artist,track['title'],track['trackNumber'])
            
            
        




missing_url = f"{base_url}/wanted/missing"

response = requests.get(missing_url, headers=headers)

if response.status_code == 200:
    data = response.json()
    missing_albums = data["records"]
    album_ids = []
    for albums in missing_albums:
        album_ids.append(albums['id'])
        print(albums)
        print('#'*8)
        get_tracks_with_hasFile(albums['id'],albums["artist"]["artistName"])
        print(albums["artist"]["artistName"], " - ", albums["title"])
else:
    print("Request failed with status code", response.status_code)

