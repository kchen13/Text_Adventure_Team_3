# Base class for all items
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
        return '{}: {}\n----------------------\nProtection: {}' \
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
                         health=20)


class Bandages(Health):
    def __init__(self):
        super().__init__(name="Bandages",
                         description="Great for nicks and scratches.",
                         health=10)


class DoctorsCoat(Armor):
    # __init__ is the constructor method
    def __init__(self):
        super().__init__(name="Doctors Coat",
                         description="Not much linen but a layer is a layer.",
                         hp=20)


class Knife(Weapon):
    def __init__(self):
        super().__init__(name="Knife",
                         description="A 3 inch rusted blade",
                         damage=5)

    @staticmethod
    def sound_effect():
        mod_sound_effects.knife()
