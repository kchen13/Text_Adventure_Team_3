import random
import items
import world
import mod_input_validation


class Player():
    def __init__(self):
        # Inventory on startup
        self.inventory = [items.Knife()]
        # Health Points
        self.hp = 100
        # Armor Points
        self.armor = 0
        # Start Position
        self.location_x, self.location_y = world.starting_position  # (0, 0)
        # Last Position
        self.last_x = 0
        self.last_y = 0
        # End game victory condition
        self.victory = False  # no victory on start up

    def flee(self, tile):
        """Moves the player randomly to an adjacent tile"""
        available_moves = tile.adjacent_moves()
        r = random.randint(0, len(available_moves) - 1)
        self.do_action(available_moves[r])

    def last_position(self, x, y):
        if self.last_x != x or self.last_y != y:
            self.last_x = x
            self.last_y = y
            return True
        else:
            return False

    def is_alive(self):
        # Checks if still alive
        return self.hp > 0  # Greater than zero value then you are still alive

    def room_inventory(self):
        # Prints room inventory
        item_number = 1
        room = world.tile_exists(self.location_x, self.location_y)
        print('*****    Room Items    *****')
        if len(room.room_inventory) == 0:
            # Returns if no items
            print("There's nothing here. Cold and empty like this world.\n")
            return
        for item in room.room_inventory:
            print('(', item_number, ')', item, '\n')
            item_number += 1
        # Loot item prompts and validations
        user_input = mod_input_validation.yes_or_no('Would you like to take any items?(y/n)')
        if user_input == 'n':
            return
        if user_input == 'y':
            selection = mod_input_validation.item_select('Select item to take:', len(self.inventory))
            # Pick up item from current room
            room = world.tile_exists(self.location_x, self.location_y)
            loot = room.room_inventory[int(selection) - 1]
            self.inventory.append(loot)
            # Removes from room inventory
            del room.room_inventory[int(selection) - 1]
        self.room_inventory()

    def print_inventory(self):
        # Prints inventory menu
        item_number = 1
        print('*****    Inventory    *****')
        if len(self.inventory) == 0:
            # Returns if no items
            print('You have no items.\n')
            return
        for item in self.inventory:
            print('(', item_number, ')', item, '\n')
            item_number += 1
        # Drop item prompts and validations
        user_input = mod_input_validation.yes_or_no('Would you like to drop any items?(y/n)')
        if user_input == 'n':
            return
        if user_input == 'y':
            selection = mod_input_validation.item_select('Select item to remove:', len(self.inventory))
            # Drops item into current room
            room = world.tile_exists(self.location_x, self.location_y)
            drop = self.inventory[int(selection) - 1]
            room.room_inventory.append(drop)
            # Removes from player inventory
            del self.inventory[int(selection) - 1]

    def player_stats(self):
        # Prints health and armor
        print('*****    Player Statistics    *****')
        print('Health: ', self.hp)
        print('Armor: ', self.armor, '\n')

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
