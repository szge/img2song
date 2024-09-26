# img2song
CLI for automatically choosing and playing a Spotify song based on an image

## Setup

1. Complete the [Spotify API setup](https://developer.spotify.com/documentation/web-api/tutorials/getting-started), making sure Redirect URIs has "http://localhost:3000". Then, get your `client_id` and `client_secret` ready
2. `pip install -r requirements.txt`
3. Run `./img2song.py setup` and follow the instructions to login and give permissions.

## Usage

`img2song` is intended to mostly be used with other programs.

For example, to an application to automatically play songs depending on what you're looking at on your screen.