#!/usr/bin/env python3

"""
img2song is a program that converts images to music.
"""

import argparse
from setup import setup
from spotifyapi import start_playback

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
        start_playback(uris=["spotify:track:3n3Ppam7vgaVa1iaRUc9Lp"])

if __name__ == "__main__":
    main()
