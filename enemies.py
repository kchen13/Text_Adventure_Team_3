class Enemy:
    def __init__(self, name, hp, damage):
        self.name = name
        self.hp = hp
        self.damage = damage

    def is_alive(self):
        return self.hp > 0


class Ghoul(Enemy):
    def __init__(self):
        super().__init__(name="Ghoul", hp=10, damage=5)
