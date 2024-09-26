#!/usr/bin/env python3

"""
img2song is a program that converts images to music.
"""

import argparse
import json
import os
import sys
import requests
import webbrowser
import random
import string
from urllib.parse import urlencode, urlparse, parse_qs
import json
from typing import Optional, List

def setup():
    print("Complete the Spotify API setup to get your client_id and client_secret")
    print("https://developer.spotify.com/documentation/web-api/tutorials/getting-started")
    client_id = input("Enter your client_id: ")
    client_secret = input("Enter your client_secret: ")
    with open("config.json", "w") as f:
        json.dump({"client_id": client_id, "client_secret": client_secret}, f)
    access_token = get_client_access_token()
    if not access_token:
        print("Setup failed")
        return
    user_access_token = user_login()
    if not user_access_token:
        print("Setup failed")
        return
    print("Setup complete")

def get_client_access_token():
    with open("config.json", "r") as f:
        config = json.load(f)
    client_id = config["client_id"]
    client_secret = config["client_secret"]
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }

    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        access_token = response.json().get("access_token")
        # print("Access token:", access_token)
        return access_token
    else:
        print("Failed to get access token:", response.status_code, response.text)
        return None

def user_login():
    with open("config.json", "r") as f:
        config = json.load(f)
    client_id = config["client_id"]
    client_secret = config["client_secret"]
    redirect_uri = 'http://localhost:3000'
    
    state = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    scope = 'user-read-playback-state user-modify-playback-state user-read-currently-playing'
    
    auth_url = 'https://accounts.spotify.com/authorize?' + urlencode({
        'response_type': 'code',
        'client_id': client_id,
        'scope': scope,
        'redirect_uri': redirect_uri,
        'state': state
    })
    
    webbrowser.open(auth_url)
    
    print("A browser window should have opened. Please log in and authorize the application.")
    print("After authorization, you will be redirected to a localhost URL. Copy the entire URL and paste it here:")
    callback_url = input("Enter the callback URL: ").strip()
    
    parsed_url = urlparse(callback_url)
    auth_code = parse_qs(parsed_url.query).get('code', [None])[0]
    
    if not auth_code:
        print("Failed to get authorization code.")
        return None
    
    token_url = 'https://accounts.spotify.com/api/token'
    data = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': redirect_uri,
        'client_id': client_id,
        'client_secret': client_secret,
    }
    response = requests.post(token_url, data=data)
    
    if response.status_code == 200:
        tokens = response.json()
        user_access_token = tokens.get('access_token')
        user_refresh_token = tokens.get('refresh_token')
        
        config['user_access_token'] = user_access_token
        config['user_refresh_token'] = user_refresh_token
        with open("config.json", "w") as f:
            json.dump(config, f)
        
        print("Login successful. Access token and refresh token have been saved.")
        return user_access_token
    else:
        print("Failed to get access token:", response.status_code, response.text)
        return None

def start_playback(context_uri: Optional[str] = None, uris: Optional[List[str]] = None, offset: Optional = None, position_ms: Optional[int] = None):
    with open("config.json", "r") as f:
        config = json.load(f)
    user_access_token = config["user_access_token"]
    url = "https://api.spotify.com/v1/me/player/play"
    headers = {
        "Authorization": f"Bearer {user_access_token}",
        "Content-Type": "application/json"
    }
    data = json.dumps({
        # "uris": ["spotify:track:3n3Ppam7vgaVa1iaRUc9Lp"],
        "position_ms": 0
    })
    response = requests.put(url, headers=headers, data=data)
    if response.status_code == 204:
        print("Playback started")
    else:
        print(f"Error {response.status_code}: {response.text}")

def main():
    """
    Usage:
    img2song setup
    img2song -i <image_path>
    """
    parser = argparse.ArgumentParser(description="convert an image to a Spotify song")
    parser.add_argument("command", nargs='?', help="Setup the application or provide image path")
    parser.add_argument("-i", "--input_image", help="Path to the input image file")
    args = parser.parse_args()
    
    if args.command == "setup":
        setup()
    else:
        start_playback(context_uri=args.input_image)

if __name__ == "__main__":
    main()
