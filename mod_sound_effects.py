# Author: Kelby Chen
# Purpose: Manage game sounds with pygame

import os
from pygame import mixer

path = os.path.dirname(__file__)
mixer.init(channels=3)

# Sound credits @ EOF
background_sound = path + '/sound effects/00-StartingRoom.ogg'
cold_room = mixer.Sound(path + '/sound effects/01-ColdRoom.ogg')
supply_room = mixer.Sound(path + '/sound effects/02-SupplyRoom.ogg')
typing_sound = mixer.Sound(path + '/sound effects/SE-Typing.ogg')
ghoul01_sound = mixer.Sound(path + '/sound effects/SE-Ghoul01.ogg')
knife_sound = mixer.Sound(path + '/sound effects/SE-Knife.ogg')
enemy_dead = mixer.Sound(path + '/sound effects/SE-EnemyDead.ogg')
fist_sound = mixer.Sound(path + '/sound effects/SE-Fists.ogg')
health_sound = mixer.Sound(path + '/sound effects/SE-Health.ogg')


def background():
    mixer.music.set_volume(0.4)
    mixer.music.load(background_sound)
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


def fists():
    mixer.Sound.play(fist_sound)


def health():
    mixer.Sound.play(health_sound)


def killed_enemy():
    mixer.Sound.play(enemy_dead)

# Credits
# background: https://freesound.org/people/RokZRooM/sounds/344778/
# cold: https://freesound.org/people/Kastenfrosch/sounds/162486/
# supply: https://freesound.org/people/Legato87/sounds/72741/
# typing: https://freesound.org/people/Natty23/sounds/257275/
# ghoul01: https://freesound.org/people/limetoe/sounds/317017/
# knife: https://freesound.org/people/JoelAudio/sounds/77611/
# killed enemy: https://freesound.org/people/limetoe/sounds/249524/
# fists: https://freesound.org/people/josepharaoh99/sounds/361636/
# health: https://freesound.org/people/GameAudio/sounds/220173/
