from dotenv import load_dotenv
import os
import base64
from requests import post, get, put
import json

load_dotenv()


client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = client_id + ':' + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}


def search_for_track(token, track, qt):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={track}&type=track&limit=" + qt

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)
    #print(json_result)
    return json_result

def search(token, search_item, qt):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={search_item}&type=track,artist&limit=" + qt

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)
    #print(json_result)
    return json_result

def play_song(token, song_uri):
    url = "https://api.spotify.com/v1/me/player/play"
    headers = get_auth_header(token)
    body = {
        "uris": [song_uri] 
    }

    result = put(url, headers=headers, data=json.dumps(body))
    print(result)

def print_tracks_pretty(search_result_json):
    tracks = search_result_json.get("tracks", {}).get("items", [])
    if not tracks:
        print("No tracks found.")
        return

    for i, track in enumerate(tracks, start=1):
        track_name = track.get("name")
        artists = ", ".join([artist.get("name") for artist in track.get("artists", [])])
        album_name = track.get("album", {}).get("name")
        track_url = track.get("external_urls", {}).get("spotify")
        release_date = track.get("album", {}).get("release_date")

        print(f"{i}. {track_name}")
        print(f"   Artists: {artists}")
        print(f"   Album: {album_name} ({release_date})")
        print(f"   URL: {track_url}")
        print("-" * 40)


if __name__ == "__main__":
    t = get_token()
    s = input("Enter your search:")
    qt = input("How many results:")
    ret = search_for_track(t, s, qt)
    print_tracks_pretty(ret)

    #play_song(t, 'spotify:track:25qp5LiSuet6rvl950jrGD')