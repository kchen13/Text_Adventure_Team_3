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
wind_sound = mixer.Sound(path + '/sound effects/SE-Wind.ogg')
axe_sound = mixer.Sound(path + '/sound effects/SE-Axe.ogg')
scalpel_sound = mixer.Sound(path + '/sound effects/SE-Scalpel.ogg')
giant_ghoul_sound = mixer.Sound(path + '/sound effects/SE-GiantGhoul.ogg')
good_mystery_sound = mixer.Sound(path + '/sound effects/SE-GoodMystery.ogg')
inventory_sound = mixer.Sound(path + '/sound effects/SE-InventoryPickup.ogg')
companion_death_sound = mixer.Sound(path + '/sound effects/SE-CompanionDeath.ogg')
colt45_sound = mixer.Sound(path + '/sound effects/SE-Colt45.ogg')
zombie_sound = mixer.Sound(path + '/sound effects/SE-Zombie.ogg')
undead_mob_sound = mixer.Sound(path + '/sound effects/SE-UndeadMob.ogg')
victory_sound = mixer.Sound(path + '/sound effects/SE-Victory.ogg')
dog_sound = mixer.Sound(path + '/sound effects/SE-DogBark.ogg')


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


def wind():
    mixer.Sound.play(wind_sound)


def axe():
    mixer.Sound.play(axe_sound)


def scalpel():
    mixer.Sound.play(scalpel_sound)


def giant_ghoul():
    mixer.Sound.play(giant_ghoul_sound)


def good_mystery():
    mixer.Sound.play(good_mystery_sound)


def inventory_pickup():
    mixer.Sound.play(inventory_sound)


def companion_death():
    mixer.Sound.play(companion_death_sound)


def colt45():
    mixer.Sound.play(colt45_sound)


def zombie():
    mixer.Sound.play(zombie_sound)


def undead_mob():
    mixer.Sound.play(undead_mob_sound)


def victory():
    mixer.Sound.play(victory_sound)


def dog():
    mixer.Sound.play(dog_sound)

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
# wind: https://freesound.org/people/helhel/sounds/346237/
# axe: https://freesound.org/people/dslrguide/sounds/321480/
# scalpel: https://freesound.org/people/BristolStories/sounds/51702/
# giant_ghoul: https://freesound.org/people/debsound/sounds/250148/
# good_surprise_sound: https://freesound.org/people/qubodup/sounds/169727/
# inventory_pickup: https://freesound.org/people/Wagna/sounds/325805/
# companion_death: https://freesound.org/people/FunWithSound/sounds/394900/
# colt45: https://freesound.org/people/EFlexTheSoundDesigner/sounds/378204/
# zombie: https://freesound.org/people/LittleRobotSoundFactory/sounds/316192/
# undead_mob: https://freesound.org/people/thegreatperson/sounds/210826/
# victory: https://freesound.org/people/FunWithSound/sounds/369252/
# dog: https://freesound.org/people/olliauska/sounds/418105/
