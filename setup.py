#!/usr/bin/env python3

import json
import requests
import webbrowser
import random
import string
from urllib.parse import urlencode, urlparse, parse_qs

def setup():
    print("Complete the Spotify API setup to get your client_id and client_secret")
    print("https://developer.spotify.com/documentation/web-api/tutorials/getting-started")
    with open("config.json", "r") as f:
        config = json.load(f)
    client_id, client_secret = config.get("client_id"), config.get("client_secret")
    if not client_id or not client_secret:
        print("Client ID and client secret not set up")
        client_id = input("Enter your client_id: ")
        client_secret = input("Enter your client_secret: ")
        config["client_id"] = client_id
        config["client_secret"] = client_secret
        with open("config.json", "w") as f:
            json.dump(config, f)
    access_token = get_client_access_token()
    if not access_token:
        print("Setup failed")
        return
    user_access_token = user_login()
    if not user_access_token:
        print("Setup failed")
        return
    gemini_api_key = get_gemini_api_key()
    if not gemini_api_key:
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
        
        print("Login successful. Access token and refresh token have been saved.")
    else:
        print("Failed to get access token:", response.status_code, response.text)

    print("Optionally, you may provide the device_id to play on, in order to be able to wake up your device.")
    print("You can find your device_id by running: ")
    device_id = input("Enter your device_id: ")

    config['device_id'] = device_id
    with open("config.json", "w") as f:
        json.dump(config, f)

    return user_access_token, device_id

def get_gemini_api_key():
    with open("config.json", "r") as f:
        config = json.load(f)
    gemini_api_key = config.get("gemini_api_key")
    if not gemini_api_key:
        gemini_api_key = input("Enter your Gemini API key: ")
        config["gemini_api_key"] = gemini_api_key
        with open("config.json", "w") as f:
            json.dump(config, f)
    return gemini_api_key
