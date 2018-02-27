# Author: Kelby Chen
# Purpose: Manage game sounds with pygame

import os
from pygame import mixer

path = os.path.dirname(__file__)
mixer.init(channels=3)

starting_room = path + '/sound effects/00-StartingRoom.ogg'
# Credit: https://freesound.org/people/RokZRooM/sounds/344778/
cold_room = mixer.Sound(path + '/sound effects/01-ColdRoom.ogg')
# Credit: https://freesound.org/people/Kastenfrosch/sounds/162486/
supply_room = mixer.Sound(path + '/sound effects/02-SupplyRoom.ogg')
# Credit: https://freesound.org/people/Legato87/sounds/72741/
typing_sound = mixer.Sound(path + '/sound effects/SE-Typing.ogg')
# Credit: https://freesound.org/people/Natty23/sounds/257275/
ghoul01_sound = mixer.Sound(path + '/sound effects/SE-Ghoul01.ogg')
# Credit: https://freesound.org/people/limetoe/sounds/317017/
knife_sound = mixer.Sound(path + '/sound effects/SE-Knife.ogg')
# Credit: https://freesound.org/people/JoelAudio/sounds/77611/
enemy_dead = mixer.Sound(path + '/sound effects/SE-EnemyDead.ogg')


# Credit: https://freesound.org/people/limetoe/sounds/249524/

def background():
    mixer.music.set_volume(0.4)
    mixer.music.load(starting_room)
    mixer.music.play(-1)


def cold():
    mixer.Sound.play(cold_room)


def supply():
    mixer.Sound.play(supply_room)


def typing():
    mixer.Sound.set_volume(typing_sound, 0.1)
    mixer.Sound.play(typing_sound)


def ghoul01():
    mixer.Sound.play(ghoul01_sound)


def knife():
    mixer.Sound.play(knife_sound)


def killed_enemy():
    mixer.Sound.play(enemy_dead)
