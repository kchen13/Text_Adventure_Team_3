import random
import items
import world
import mod_input_validation


class Player():
    def __init__(self):
        self.inventory = [items.Gold(15), items.Pillow(), items.Rock()]  # Inventory on startup
        self.hp = 100  # Health Points
        self.location_x, self.location_y = world.starting_position  # (0, 0)
        self.victory = False  # no victory on start up

    def flee(self, tile):
        """Moves the player randomly to an adjacent tile"""
        available_moves = tile.adjacent_moves()
        r = random.randint(0, len(available_moves) - 1)
        self.do_action(available_moves[r])

    # is_alive method
    def is_alive(self):
        return self.hp > 0  # Greater than zero value then you are still alive

    def print_inventory(self):
        item_number = 1
        print('*****Inventory*****\n')
        for item in self.inventory:
            print('(', item_number, ')', item, '\n')
            item_number += 1
        if len(self.inventory) == 0:
            print('You have no items.')
            return
        user_input = mod_input_validation.yes_or_no('Would you like to drop any items?(y/n)')
        if user_input == 'n':
            return
        if user_input == 'y':
            selection = mod_input_validation.item_drop('What item would you like to remove?', len(self.inventory))
            del self.inventory[int(selection) - 1]
            self.print_inventory()

    def move(self, dx, dy):
        self.location_x += dx
        self.location_y += dy
        print(world.tile_exists(self.location_x, self.location_y).intro_text())

    def move_north(self):
        self.move(dx=0, dy=-1)

    def move_south(self):
        self.move(dx=0, dy=1)

    def move_east(self):
        self.move(dx=1, dy=0)

    def move_west(self):
        self.move(dx=-1, dy=0)

    def attack(self, enemy):
        best_weapon = None
        max_dmg = 0
        for i in self.inventory:
            if isinstance(i, items.Weapon):
                if i.damage > max_dmg:
                    max_dmg = i.damage
                    best_weapon = i

        print("You use {} against {}!".format(best_weapon.name, enemy.name))
        enemy.hp -= best_weapon.damage
        if not enemy.is_alive():
            print("You killed {}!".format(enemy.name))
        else:
            print("{} HP is {}.".format(enemy.name, enemy.hp))

    def do_action(self, action, **kwargs):
        action_method = getattr(self, action.method.__name__)
        if action_method:
            action_method(**kwargs)
