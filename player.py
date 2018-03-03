import random
import items
import mod_sound_effects
import world
import mod_input_validation
import time

class Player():
    def __init__(self):
        # Inventory on startup
        self.inventory = [items.Axe(), items.DoctorsCoat(), items.Scalpel()]
        # Health Points
        self.hp = 100
        # Armor Points
        self.armor = self.best_armor()
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
        print('*****    Area Items    *****')
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
            room = world.tile_exists(self.location_x, self.location_y)
            selection = mod_input_validation.item_select('Select item to take (0 to exit):', len(room.room_inventory))
            if selection == 0:
                return
            else:
                # Pick up item from current room
                loot = room.room_inventory[int(selection) - 1]
                print('You picked up a', loot)
                self.inventory.append(loot)
                mod_sound_effects.inventory_pickup()
                # Removes from room inventory
                del room.room_inventory[int(selection) - 1]
        self.room_inventory()

    def inventory_actions(self):
        self.print_inventory()
        # Prints inventory actions and executes them
        print('---------------------------')
        print('Choose an action:')
        print('u: Use item(s)')
        print('d: Drop item(s)')
        print('x: Exit inventory menu')
        # Prompts user and validates input
        user_input = mod_input_validation.inventory_action('Action:')
        # Runs user requested actions
        if user_input == 'u':
            self.use_inventory()
        if user_input == 'd':
            self.drop_inventory()
        if user_input == 'x':
            return

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

    def use_inventory(self):
        # Use item prompts and validation
        self.print_inventory()
        selection = mod_input_validation.item_select('Select item to use (0 to exit):', len(self.inventory))
        use = self.inventory[int(selection) - 1]
        # Returns to menu
        if use == 0:
            return
        # Add health, delete from inventory
        health_list = ['First Aid Kit', 'Bandages']
        if use.name in health_list:
            self.add_health(use.health)
            del self.inventory[int(selection) - 1]
        # Does nothing
        else:
            print("Not usable in this instance.")

    def drop_inventory(self):
        # Drop item prompts and validation
        self.print_inventory()
        selection = mod_input_validation.item_select('Select item to remove (0 to exit):', len(self.inventory))
        # Returns to menu if zero
        if selection == 0:
            return
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

    def add_health(self, hp2add):
        # Adds health not to exceed 100
        self.hp += hp2add
        if self.hp > 100:
            self.hp = 100
        mod_sound_effects.health()
        print('Player Health is now:', self.hp)

    def move(self, dx, dy):
        self.location_x += dx
        self.location_y += dy
        print(world.tile_exists(self.location_x, self.location_y).intro_text(self))

    def move_north(self):
        self.move(dx=0, dy=-1)

    def move_south(self):
        self.move(dx=0, dy=1)

    def move_east(self):
        self.move(dx=1, dy=0)

    def move_west(self):
        self.move(dx=-1, dy=0)

    def attack(self, enemy):
        weapon = self.best_weapon()
        if weapon is None:
            print('For Christ Sakes!', weapon.description)
        print("\nYou use {} against {}!".format(weapon.name, enemy.name))
        enemy.hp -= weapon.damage
        self.hp -= (enemy.damage - self.armor * 0.1)
        weapon.sound_effect()
        time.sleep(1.5)
        print("Your HP: ", self.hp)
        if not enemy.is_alive():

            print("You killed {}!".format(enemy.name))
            mod_sound_effects.killed_enemy()
        else:
            print("{} HP: {}".format(enemy.name, enemy.hp))

    def best_armor(self):
        max_hp = 0
        for i in self.inventory:
            if isinstance(i, items.Armor):
                if i.hp > max_hp:
                    max_hp = i.hp
        return max_hp

    def best_weapon(self):
        weapon = None
        max_dmg = 0
        for i in self.inventory:
            if isinstance(i, items.Weapon):
                if i.damage > max_dmg:
                    max_dmg = i.damage
                    weapon = i
        if weapon is None:
            weapon = items.Fists()
        return weapon

    def do_action(self, action, **kwargs):
        action_method = getattr(self, action.method.__name__)
        if action_method:
            action_method(**kwargs)
