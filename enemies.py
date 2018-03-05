class Enemy:
    def __init__(self, name, hp, damage):
        self.name = name
        self.hp = hp
        self.damage = damage

    def is_alive(self):
        return self.hp > 0


class Ghoul(Enemy):
    def __init__(self):
        super().__init__(name="Ghoul", hp=50, damage=8)


class GiantGhoul(Enemy):
    def __init__(self):
        super().__init__(name="Giant Ghoul", hp=100, damage=16)


class Zombie(Enemy):
    def __init__(self):
        super().__init__(name="Giant Ghoul", hp=120, damage=23)


class UndeadMob(Enemy):
    def __init__(self):
        super().__init__(name="Undead Mob", hp=500, damage=150)
