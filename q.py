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
    data = {"grant_type": "authorization_code"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    print(json_result)
    token = json_result
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}



def search_for_item(token, search_item):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={search_item}&type=track,artist&limit=1"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)
    print(json_result)
    return json_result

def play_song(token, song_uri):
    url = "https://api.spotify.com/v1/me/player/play"
    headers = get_auth_header(token)
    body = {
        "uris": [song_uri] 
    }

    result = put(url, headers=headers, data=json.dumps(body))
    print(result)


t = get_token()
#search_for_item(t, "tzuyu")
#play_song(t, 'spotify:track:25qp5LiSuet6rvl950jrGD')

#get auth code to control play/pause