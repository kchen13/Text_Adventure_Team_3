class Enemy:
    def __init__(self, name, hp, damage):
        self.name = name
        self.hp = hp
        self.damage = damage

    def is_alive(self):
        return self.hp > 0


class Ghoul(Enemy):
    def __init__(self):
        super().__init__(name="Ghoul", hp=20, damage=5)


class GiantGhoul(Enemy):
    def __init__(self):
        super().__init__(name="Giant Ghoul", hp=40, damage=10)
