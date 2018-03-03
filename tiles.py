import actions
import enemies
import items
import mod_companion
import world
import mod_slow_text
import mod_movement_history
import mod_sound_effects


class MapTile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def intro_text(self, the_player):
        raise NotImplementedError()

    def adjacent_moves(self):
        # Returns available movements
        moves = []
        if world.tile_exists(self.x + 1, self.y):
            # Gets the tile's room_id
            rm_id = world.tile_exists(self.x + 1, self.y).room_id
            # Parameter sent so the room_id can be added to the name of the Action
            moves.append(actions.MoveEast(rm_id))
        if world.tile_exists(self.x - 1, self.y):
            rm_id = world.tile_exists(self.x - 1, self.y).room_id
            moves.append(actions.MoveWest(rm_id))
        if world.tile_exists(self.x, self.y - 1):
            rm_id = world.tile_exists(self.x, self.y - 1).room_id
            moves.append(actions.MoveNorth(rm_id))
        if world.tile_exists(self.x, self.y + 1):
            rm_id = world.tile_exists(self.x, self.y + 1).room_id
            moves.append(actions.MoveSouth(rm_id))
        return moves

    def available_actions(self, the_player):
        # Returns available actions
        moves = self.adjacent_moves()
        moves.insert(0, actions.ViewRoomInventory())
        moves.append(actions.PlayerStats())
        moves.append(actions.ViewInventory())
        if len(the_player.companions) > 0:
            moves.append(actions.ViewCompanions())
        return moves


class EnemyRoom(MapTile):
    def intro_text(self, the_player):
        pass

    def __init__(self, x, y, enemy):
        self.enemy = enemy
        super().__init__(x, y)

    def modify_player(self, the_player):
        the_player.best_armor()
        if self.enemy.is_alive():
            damage = self.enemy.damage - (the_player.armor * 0.1)
            the_player.hp = the_player.hp - (self.enemy.damage - the_player.armor * 0.1)
            mod_slow_text.slow('{} does {} damage.\nYou have {} HP remaining.'.
                               format(self.enemy.name, damage, the_player.hp))

    def available_actions(self, the_player):
        if self.enemy.is_alive():
            moves = [actions.Flee(tile=self), actions.Attack(enemy=self.enemy), actions.PlayerStats(),
                     actions.ViewInventory()]
            return moves
        else:
            return MapTile.available_actions(self, the_player)


class HospitalLobby(MapTile):
    room_id = 'Hospital Lobby'
    room_inventory = []

    def intro_text(self, the_player):
        coordinates = mod_movement_history.get_coordinates(self)
        if mod_movement_history.check_history(coordinates):
            mod_sound_effects.background()
            mod_slow_text.super_slow('\n'
                                     '                ************************************\n'
                                     '                *            Hypothermia           *\n'
                                     '                ************************************\n'
                                     'The year is 1835 and your player is a well respected doctor in Philadelphia.\n'
                                     'One day, the temperature drops dramatically in the hospital and the power\n'
                                     'goes out. You are alone with your latest project. A wide spread disease has\n'
                                     'spread across the city and you are working on your test subject Frank. You\n'
                                     'have replaced many of Frank’s body parts with machinery but without\n'
                                     'electricity, you have to abandon him.\n'
                                     '\nThe dropping temperature is causing you to look for supplies and search for a\n'
                                     'warm safe environment. You leave Frank’s room and have a few options where to\n'
                                     'look for supplies.\nYou stand in the hospital lobby awaiting your fate. \n')
        else:
            print('Doc, what are you smoking? You started here. Get moving!')
        return """"""

    def modify_player(self, player):
        # Room has no action on player
        pass


class MysteriousRoom(MapTile):
    room_id = 'oddly mysterious room is this direction.'
    room_inventory = [items.DoctorsCoat(), items.Knife()]

    def intro_text(self, the_player):
        coordinates = mod_movement_history.get_coordinates(self)
        if mod_movement_history.check_history(coordinates):
            mod_slow_text.slow("There's a cold mist in the air, could be somethings in that cabinet though.\n")
        else:
            print('Not so mysterious anymore.')
        return """"""

    @staticmethod
    def modify_player(player):
        damage = 4 - (player.armor * 0.1)
        player.hp -= damage
        mod_slow_text.slow('Your body temperature is dropping.\nYou lost {} health.\nYour HP is currently: {}\n'
                           .format(damage, player.hp))


class ColdRoom(MapTile):
    room_id = 'seems colder this way.'
    room_inventory = []

    def intro_text(self, the_player):
        coordinates = mod_movement_history.get_coordinates(self)
        mod_sound_effects.cold()
        if mod_movement_history.check_history(coordinates):
            mod_slow_text.slow("\nA cold fierce wind hits your body.\n")
        else:
            mod_slow_text.slow("\nA cold fierce wind reminds you that you've been here before.\n")
        return """"""

    @staticmethod
    def modify_player(player):
        damage = 8 - (player.armor * 0.1)
        player.hp -= damage
        mod_slow_text.slow('You lost {} health.\nYour HP is currently: {}\n'.format(damage, player.hp))


class SupplyRoom01(MapTile):
    room_id = 'looks like there could be supplies in this room.'
    room_inventory = [items.FirstAid(), items.Bandages(), items.Scalpel()]

    def intro_text(self, the_player):
        coordinates = mod_movement_history.get_coordinates(self)
        mod_sound_effects.supply()
        if mod_movement_history.check_history(coordinates):
            mod_slow_text.super_slow("\nIt's some sort of supplies room. Searching may be of your best interest.\n")
        else:
            mod_slow_text.slow("\nThis is that supply room you were in earlier.\n")
        return """"""

    @staticmethod
    def modify_player(player):
        damage = 4 - (player.armor * 0.1)
        player.hp -= damage
        mod_slow_text.slow('Your body temperature is dropping.\nYou lost {} health.\nYour HP is currently: {}\n'
                           .format(damage, player.hp))


class GhoulRoom01(EnemyRoom):
    room_id = 'is... that a sound???'
    room_inventory = [items.Bandages()]

    def __init__(self, x, y):
        super().__init__(x, y, enemies.Ghoul())

    def intro_text(self, the_player):
        if self.enemy.is_alive():
            mod_sound_effects.ghoul01()
            mod_slow_text.slow("\nHoly crap, it's a God damn ghoul! Ugly, ferocious looking and missing some skin."
                               "\nGhoul HP:" + str(self.enemy.hp))
        else:
            mod_slow_text.slow("\nHa! That ghoul looks like Tom Brady after Super Bowl LII.")
        return """"""


class ParkingLot01(MapTile):
    room_id = 'Parking Lot of the Hospital'
    room_inventory = []

    def intro_text(self, the_player):
        coordinates = mod_movement_history.get_coordinates(self)
        mod_sound_effects.wind()
        if mod_movement_history.check_history(coordinates):
            mod_slow_text.super_slow(
                "\nThe moment you walk out you realize how quickly the temperature has fallen.\nIn "
                "order to survive you're going to need to find warmth and shelter. Better decide\n"
                "quick before you die from the frigid coldness.\n")
        else:
            mod_slow_text.slow("\nIt's blistering cold and there's a sign that says No Loitering.")
        return """"""

    @staticmethod
    def modify_player(player):
        damage = 8 - (player.armor * 0.1)
        player.hp -= damage
        mod_slow_text.slow('Your body temperature is dropping.\nYou lost {} health.\nYour HP is currently: {}\n'
                           .format(damage, player.hp))


class ParkingLot02(MapTile):
    room_id = 'Parking Lot of the Hospital'
    room_inventory = []

    def intro_text(self, the_player):
        coordinates = mod_movement_history.get_coordinates(self)
        mod_sound_effects.wind()
        if mod_movement_history.check_history(coordinates):
            mod_slow_text.slow("\nYou continue on, out towards the main street and away from the hospital. Will "
                               "you\nmake it to shelter? Making decisions for your survival will be crucial.\n")
        else:
            mod_slow_text.slow("\nIt's blistering cold and there's a sign that says No Loitering.")
        return """"""

    @staticmethod
    def modify_player(player):
        damage = 8 - (player.armor * 0.1)
        player.hp -= damage
        mod_slow_text.slow('Your body temperature is dropping.\nYou lost {} health.\nYour HP is currently: {}\n'
                           .format(damage, player.hp))


class MainStreet(MapTile):
    room_id = 'The main street outside of the Hospital'
    room_inventory = []

    def intro_text(self, the_player):
        coordinates = mod_movement_history.get_coordinates(self)
        mod_sound_effects.wind()
        if mod_movement_history.check_history(coordinates):
            mod_slow_text.super_slow(
                "\nYou're now exiting the parking lot. The cold wind continues to hurt your face.\n"
                "There seems to be hope in heading north, is that a cloud of smoke? Could there\n"
                "be people there? Smoke, fire, warmth, what shall you do?\n")
        else:
            mod_slow_text.slow("\nIf you're not a polar bear you should probably look for warmth.\n")
        return """"""

    @staticmethod
    def modify_player(player):
        damage = 8 - (player.armor * 0.1)
        player.hp -= damage
        mod_slow_text.slow('Your body temperature is dropping.\nYou lost {} health.\nYour HP is currently: {}\n'
                           .format(damage, player.hp))


class AbandonedCar01(MapTile):
    room_id = 'towards an abandoned broken down car'
    room_inventory = [items.FirstAid(), items.Bandages()]

    def intro_text(self, the_player):
        coordinates = mod_movement_history.get_coordinates(self)
        mod_sound_effects.wind()
        if mod_movement_history.check_history(coordinates):
            mod_slow_text.super_slow("\nThe car is broken down, the door seems unlocked. Finders keepers.... right?\n")
        else:
            mod_slow_text.slow("\nSame old car, unfortunately a magical fairy hasn't come and revived it.\n")
        return """"""

    @staticmethod
    def modify_player(player):
        damage = 10 - (player.armor * 0.1)
        player.hp -= damage
        mod_slow_text.slow('Your body temperature is dropping.\nYou lost {} health.\nYour HP is currently: {}\n'
                           .format(damage, player.hp))


class AbandonedTruck01(EnemyRoom):
    room_id = 'towards a truck, could there be supplies there?'
    room_inventory = [items.Bandages()]

    def __init__(self, x, y):
        super().__init__(x, y, enemies.Ghoul())

    def intro_text(self, the_player):
        if self.enemy.is_alive():
            mod_slow_text.super_slow("\nLet's take a look at what's in the truck........\n")
            mod_sound_effects.ghoul01()
            mod_slow_text.slow("Ghoul! This one looks different from the ones in the hospital, uglier and\n"
                               "with less skin. He must be cold too.\n "
                               "\nGhoul HP:" + str(self.enemy.hp))
        else:
            mod_slow_text.slow("\nA dead ghoul is a good ghoul.")
        return """"""


class SmokePath01(MapTile):
    room_id = 'street that leads towards the smoke in the distance.'
    room_inventory = []

    def intro_text(self, the_player):
        coordinates = mod_movement_history.get_coordinates(self)
        mod_sound_effects.wind()
        if mod_movement_history.check_history(coordinates):
            mod_slow_text.super_slow("\nYou see the smoke in the distance, the feeling and hope is enough to keep you\n"
                                     "warm for now. The streets are abandoned, there's trash flying around being \n"
                                     "pushed by the fierce cold winds.\n")
        else:
            mod_slow_text.slow("\nThe wind blowing the trash around is making more progress than you.\n")
        return """"""

    @staticmethod
    def modify_player(player):
        damage = 10 - (player.armor * 0.1)
        player.hp -= damage
        mod_slow_text.slow('Your body temperature is dropping.\nYou lost {} health.\nYour HP is currently: {}\n'
                           .format(damage, player.hp))


class SmokePath02(EnemyRoom):
    room_id = 'street that continues closer to the smoke in the distance.'
    room_inventory = [items.FirstAid(), items.Axe()]

    def __init__(self, x, y):
        super().__init__(x, y, enemies.Ghoul())

    def intro_text(self, the_player):
        if self.enemy.is_alive():
            mod_slow_text.super_slow("\nThe street gets narrower as you walk, looks like a barricade at the next\n"
                                     "block. The city looks like crap. It's pretty quiet, a bit too quiet........\n")
            mod_sound_effects.ghoul01()
            mod_slow_text.slow("Holy crap, it's a God damn ghoul! It has hardly any skin on him, eww!"
                               "\nGhoul HP:" + str(self.enemy.hp))
        else:
            mod_slow_text.slow("\nA defeated ghoul lays here. You're impressed by your previous feat and give\n "
                               "yourself a pat on the back.\n")
        return """"""


class SmokeNarrow01(MapTile):
    room_id = 'street becomes narrow and the barricade is just up ahead'
    room_inventory = []

    def intro_text(self, the_player):
        coordinates = mod_movement_history.get_coordinates(self)
        mod_sound_effects.wind()
        if mod_movement_history.check_history(coordinates):
            mod_slow_text.super_slow("\nThe smoke in the air is getting closer but it looks like you'll need to take\n"
                                     "a detour or go around on the smaller alley streets. A straight shot to fire and\n"
                                     "warmth is just not an option.\n")
        else:
            mod_slow_text.slow("\nCame back again? What are you the Terminator?\n")
        return """"""

    @staticmethod
    def modify_player(player):
        damage = 10 - (player.armor * 0.1)
        player.hp -= damage
        mod_slow_text.slow('Your body temperature is dropping.\nYou lost {} health.\nYour HP is currently: {}\n'
                           .format(damage, player.hp))


class SmallAlley01(MapTile):
    room_id = 'a small alley way.'
    room_inventory = []

    def intro_text(self, the_player):
        coordinates = mod_movement_history.get_coordinates(self)
        mod_sound_effects.wind()
        if mod_movement_history.check_history(coordinates):
            mod_slow_text.super_slow("\nThere's less light this way, you hear sounds but can't make them out.\n"
                                     "Could just be the trash moving around, maybe rats or mice. Can they "
                                     "even.... \n"
                                     "survive these temperatures?\n")
        else:
            mod_slow_text.slow("\nStay in this alley long enough and you'll become a prostitute for ghouls.\n")
        return """"""

    @staticmethod
    def modify_player(player):
        damage = 10 - (player.armor * 0.1)
        player.hp -= damage
        mod_slow_text.slow('Your body temperature is dropping.\nYou lost {} health.\nYour HP is currently: {}\n'
                           .format(damage, player.hp))


class PharmaceuticalStore(EnemyRoom):
    room_id = 'a broken down Pharmaceutical Store.'
    room_inventory = [items.FirstAid(), items.Bandages()]

    def __init__(self, x, y):
        super().__init__(x, y, enemies.GiantGhoul())

    def intro_text(self, the_player):
        if self.enemy.is_alive():
            mod_slow_text.super_slow("\nThe coast looks clear after slowly peeking in. You make your way to the to\n"
                                     "the back counter. Shame it's one to shambles and completely ravaged. Not much\n"
                                     "here at all and it looks like everything has been looted. What a minute.......\n"
                                     "what's this? A bookbag?\n")
            mod_sound_effects.giant_ghoul()
            mod_slow_text.slow("You freeze in fear. It is absolutely massive! Looks like this kind of ghoul eats\n"
                               "those other ghouls for lunch. Twice the size and twice the ugly!\n"
                               "\nGiant Ghoul HP:" + str(self.enemy.hp))
        else:
            mod_slow_text.slow("\nThe uglier they are, the uglier they die. A giant ghoul lays here lifeless.\n")
        return """"""


class Barricade(MapTile):
    room_id = 'barricade, stock pile of crashed cars and trash'
    room_inventory = []

    def intro_text(self, the_player):
        coordinates = mod_movement_history.get_coordinates(self)
        mod_sound_effects.wind()
        if mod_movement_history.check_history(coordinates):
            mod_slow_text.super_slow("\nHeading north directly to the fire at this point is impossible. You'll have\n"
                                     "to go around, only one direction from here and that's east. There's has to be\n"
                                     "a way to circle around. As you look towards the east a figure appears....\n")
            mod_sound_effects.good_mystery()
            mod_slow_text.super_slow("\nThe figure walks out from the shadows. A man's voice says, FREEZE! You're a \n"
                                     "bit shocked, your body tenses up gripping your {}.\n\n"
                                     .format(the_player.best_weapon().name))
            mod_companion.hunter_introduction(the_player)

        else:
            mod_slow_text.slow("\nIt's a wall of junk, hoarding trash isn't a smart idea right now.\n")
        return """"""

    @staticmethod
    def modify_player(player):
        damage = 15 - (player.armor * 0.1)
        player.hp -= damage
        mod_slow_text.slow('Your body temperature is dropping.\nYou lost {} health.\nYour HP is currently: {}\n'
                           .format(damage, player.hp))


class WinningRoom(MapTile):
    room_id = 'is that warmth?'

    def intro_text(self, the_player):
        return """
        You see a bright light in the distance...
        ... it grows as you get closer! It's sunlight!
 
 
        Victory is yours!
        """

    @staticmethod
    def modify_player(player):
        player.victory = True
