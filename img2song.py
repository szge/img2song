#!/usr/bin/env python3

"""
img2song is a program that converts images to music.
"""

import argparse
from setup import setup
from spotifyapi import start_playback
from activities import activity_to_playlist_uri
from gemini import get_activity_from_image

def main():
    """
    Usage:
    img2song setup
    img2song -i <image_path>
    """
    parser = argparse.ArgumentParser(
        description="convert an image to a Spotify song")
    parser.add_argument("command", nargs='?',
                        help="Setup the application or provide image path")
    parser.add_argument("-i", "--input_image",
                        help="Path to the input image file")
    args = parser.parse_args()

    if args.command == "setup":
        setup()
    else:
        input_image = args.input_image
        if not input_image:
            raise ValueError(
                "No input image provided. Please provide an image path using -i <image_path>")
        activity = get_activity_from_image(input_image)
        start_playback(context_uri=activity_to_playlist_uri[activity])


if __name__ == "__main__":
    main()
