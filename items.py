﻿# Base class for all items
import mod_sound_effects


class Item():
    # __init__ is the constructor method
    def __init__(self, name, description):
        self.name = name  # attribute of the Item class and any subclasses
        self.description = description  # attribute of the Item class and any subclasses

    # __str__ method is used to print the object
    def __str__(self):
        return '{}: {}\n----------------------\n'.format(self.name, self.description)


# Extend the Items class
class Armor(Item):
    def __init__(self, name, description, hp):
        self.hp = hp
        super().__init__(name, description)

    def __str__(self):
        return '{}: {}\n----------------------\nProtection: {} % less damage taken' \
            .format(self.name, self.description, self.hp)


class Weapon(Item):
    def __init__(self, name, description, damage):
        self.damage = damage
        super().__init__(name, description)

    def __str__(self):
        return '{}: {}\n----------------------\nDamage: {}' \
            .format(self.name, self.description, self.damage)


class Health(Item):
    def __init__(self, name, description, health):
        self.health = health
        super().__init__(name, description)

    def __str__(self):
        return '{}: {}\n----------------------\nHealth Regeneration: {}' \
            .format(self.name, self.description, self.health)


class FirstAid(Health):
    def __init__(self):
        super().__init__(name="First Aid Kit",
                         description="Life saving health boost.",
                         health=30)


class Bandages(Health):
    def __init__(self):
        super().__init__(name="Bandages",
                         description="Great for nicks and scratches.",
                         health=15)


class DoctorsCoat(Armor):
    # __init__ is the constructor method
    def __init__(self):
        super().__init__(name="Doctors Coat",
                         description="Not much linen but a layer is a layer.",
                         hp=15)


class HeavyCoat(Armor):
    # __init__ is the constructor method
    def __init__(self):
        super().__init__(name="Heavy Military Style Coat",
                         description="Great insulation and a hard durable shell.",
                         hp=35)


class KevlarJacket(Armor):
    # __init__ is the constructor method
    def __init__(self):
        super().__init__(name="Heavy Military Kevlar Jacket",
                         description="Great insulation, super tough and almost impenetrable.",
                         hp=45)


class Fists(Weapon):
    def __init__(self):
        super().__init__(name="Bare Knuckles",
                         description="How tough are you?",
                         damage=2)

    @staticmethod
    def sound_effect():
        mod_sound_effects.fists()


class Scalpel(Weapon):
    def __init__(self):
        super().__init__(name="Scalpel",
                         description="Not the biggest threat but sharp and effective.",
                         damage=5)

    @staticmethod
    def sound_effect():
        mod_sound_effects.scalpel()


class Knife(Weapon):
    def __init__(self):
        super().__init__(name="Knife",
                         description="A 4 inch rusted blade.",
                         damage=8)

    @staticmethod
    def sound_effect():
        mod_sound_effects.knife()


class Axe(Weapon):
    def __init__(self):
        super().__init__(name="Fireman's Axe",
                         description="A heavy blade attached to a handle.",
                         damage=12)

    @staticmethod
    def sound_effect():
        mod_sound_effects.axe()


class Colt45(Weapon):
    def __init__(self):
        super().__init__(name="Colt LW Commander 45",
                         description="Single Action Hammer Fired Semi-Auto firing 45 ACP caliber ghoul stoppers.",
                         damage=22)

    @staticmethod
    def sound_effect():
        mod_sound_effects.colt45()
