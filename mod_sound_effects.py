# Author: Kelby Chen
# Purpose: Manage game sounds with pygame

import os
from pygame import mixer

path = os.path.dirname(__file__)
mixer.init()

starting_room = path + '/sound effects/00-StartingRoom.ogg'
# Credit: https://freesound.org/people/RokZRooM/sounds/344778/

cold_room = mixer.Sound(path + '/sound effects/01-ColdRoom.ogg')
# Credit: https://freesound.org/people/Kastenfrosch/sounds/162486/

supply_room = mixer.Sound(path + '/sound effects/02-SupplyRoom.ogg')


# Credit: https://freesound.org/people/Legato87/sounds/72741/


def background():
    mixer.music.set_volume(0.4)
    mixer.music.load(starting_room)
    mixer.music.play(-1)


def cold():
    mixer.Sound.play(cold_room)


def supply():
    mixer.Sound.play(supply_room)
