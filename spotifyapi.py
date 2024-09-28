import json
import requests
from typing import Optional, List, Any

# https://developer.spotify.com/documentation/web-api/reference/start-a-users-playback

def start_playback(
        context_uri: Optional[str] = None,
        uris: Optional[List[str]] = None,
        offset: Optional[Any] = None,
        position_ms: int = 0,
        device_id: Optional[str] = None
    ):
    """
    @param context_uri: Optional. Spotify URI of the context to play. Valid contexts are albums, artists & playlists. Example: {"context_uri": "spotify:album:1Je1IMUlBXcx1Fz0WE7oPT"}
    @param uris: Optional. A JSON array of the Spotify track URIs to play. Example: {"uris": ["spotify:track:4iV5W9uYEdYUVa79Axb7Rh", "spotify:track:1301WleyT98MSxVHPZCA6M"]}
    @param offset: Optional. Indicates from where in the context playback should start. Only available when context_uri corresponds to an album or playlist object. Example: {"offset": {"position": 5}} or {"offset": {"uri": "spotify:track:1301WleyT98MSxVHPZCA6M"}}
    @param position_ms: Optional. The position in milliseconds to play from.
    @param device_id: Optional. The ID of the device to play on.
    """
    with open("config.json", "r") as f:
        config = json.load(f)
    user_access_token = config["user_access_token"]
    url = "https://api.spotify.com/v1/me/player/play"
    headers = {
        "Authorization": f"Bearer {user_access_token}",
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "context_uri": context_uri,
        "uris": uris,
        "offset": offset,
        "position_ms": position_ms,
        "device_id": device_id
    })
    response = requests.put(url, headers=headers, data=data)
    if response.status_code == 204:
        print("Playback started")
    else:
        print(f"Error {response.status_code}: {response.text}")
