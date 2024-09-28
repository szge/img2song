from enum import Enum, auto

class Activity(Enum):
    CODING = auto()
    NONE_OF_THE_ABOVE = auto()

activities_list = list(Activity)

activity_to_playlist_uri = {
    Activity.CODING: "spotify:playlist:3JW7Vc4dRw83P1x1fH1J9U",
    Activity.NONE_OF_THE_ABOVE:"spotify:playlist:37i9dQZF1DXdPec7aLTmlC",
}
