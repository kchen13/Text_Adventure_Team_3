import actions
import enemies
import items
import world
import mod_slow_text
import mod_movement_history
import mod_sound_effects


class MapTile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def intro_text(self):
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

    def available_actions(self):
        # Returns available actions
        moves = self.adjacent_moves()
        moves.insert(0, actions.ViewRoomInventory())
        moves.append(actions.PlayerStats())
        moves.append(actions.ViewInventory())
        return moves


class EnemyRoom(MapTile):
    def intro_text(self):
        pass

    def __init__(self, x, y, enemy):
        self.enemy = enemy
        super().__init__(x, y)

    def modify_player(self, the_player):
        the_player.best_armor()
        if self.enemy.is_alive():
            damage = self.enemy.damage - (the_player.armor * 0.1)
            the_player.hp = the_player.hp - (self.enemy.damage - the_player.armor * 0.1)
            print('{} does {} damage.\nYou have {} HP remaining.'.
                  format(self.enemy.name, damage, the_player.hp))

    def available_actions(self):
        if self.enemy.is_alive():
            moves = [actions.Flee(tile=self), actions.Attack(enemy=self.enemy), actions.PlayerStats(),
                     actions.ViewInventory()]
            return moves
        else:
            return MapTile.available_actions(self)


class HospitalLobby(MapTile):
    room_id = 'Hospital Lobby'
    room_inventory = []

    def intro_text(self):
        coordinates = str(self.x) + str(self.y)
        mod_sound_effects.background()
        if mod_movement_history.check_history(coordinates):
            mod_slow_text.slow_text('\n'
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

    def intro_text(self):
        coordinates = str(self.x) + str(self.y)
        if mod_movement_history.check_history(coordinates):
            mod_slow_text.slow_text("There's a mist in the air, could be somethings in that cabinet though.\n")
        else:
            print('Not so mysterious anymore.')
        return """"""

    @staticmethod
    def modify_player(player):
        damage = 4 - (player.armor * 0.1)
        player.hp -= damage
        print('Your body temperature is dropping.\nYou lost {} health.\nYour HP is currently: {}\n'
              .format(damage, player.hp))


class ColdRoom(MapTile):
    room_id = 'seems colder this way.'
    room_inventory = []

    def intro_text(self):
        coordinates = str(self.x) + str(self.y)
        mod_sound_effects.cold()
        if mod_movement_history.check_history(coordinates):
            mod_slow_text.slow_text("\nA cold fierce wind hits your body.\n")
        else:
            mod_slow_text.slow_text("\nA cold fierce wind reminds you that you've been here before.\n")
        return """"""

    @staticmethod
    def modify_player(player):
        damage = 8 - (player.armor * 0.1)
        player.hp -= damage
        print('You lost {} health.\nYour HP is currently: {}\n'.format(damage, player.hp))


class SupplyRoom01(MapTile):
    room_id = 'looks like there could be supplies in this room.'
    room_inventory = [items.FirstAid(), items.Bandages()]

    def intro_text(self):
        coordinates = str(self.x) + str(self.y)
        mod_sound_effects.supply()
        if mod_movement_history.check_history(coordinates):
            mod_slow_text.slow_text("\nIt's some sort of supplies room. Searching may be of your best interest.\n")
        else:
            mod_slow_text.slow_text("\nThis is that supply room you were in earlier.\n")
        return """"""

    @staticmethod
    def modify_player(player):
        damage = 4 - (player.armor * 0.1)
        player.hp -= damage
        print('Your body temperature is dropping.\nYou lost {} health.\nYour HP is currently: {}\n'
              .format(damage, player.hp))


class GhoulRoom01(EnemyRoom):
    room_id = 'is... that a sound???'
    room_inventory = [items.Bandages()]

    def __init__(self, x, y):
        super().__init__(x, y, enemies.Ghoul())

    def intro_text(self):
        if self.enemy.is_alive():
            mod_sound_effects.ghoul01()
            mod_slow_text.slow_text("\nHoly crap, it's a God damn ghoul!"
                                    "\nGhoul HP:" + str(self.enemy.hp))
        else:
            mod_slow_text.slow_text("\nHa! That ghoul looks like Tom Brady after Super Bowl LII.")
        return """"""


class ParkingLot(MapTile):
    room_id = 'Parking Lot of the Hospital'
    room_inventory = [items.FirstAid(), items.Bandages()]

    def intro_text(self):
        coordinates = str(self.x) + str(self.y)
        mod_sound_effects.supply()
        if mod_movement_history.check_history(coordinates):
            mod_slow_text.slow_text("\nThe moment you walk out you realize how quickly the temperature has fallen. In "
                                    "order to survive you're going to need to find warmth and shelter. Better decide "
                                    "quick before you die from the frigid coldness.\n")
        else:
            mod_slow_text.slow_text("\nIt's blistering cold and there's a sign that says No Loitering.")
        return """"""

    @staticmethod
    def modify_player(player):
        damage = 8 - (player.armor * 0.1)
        player.hp -= damage
        print('Your body temperature is dropping.\nYou lost {} health.\nYour HP is currently: {}\n'
              .format(damage, player.hp))


class WinningRoom(MapTile):
    room_id = 'is that warmth?'

    def intro_text(self):
        return """
        You see a bright light in the distance...
        ... it grows as you get closer! It's sunlight!
 
 
        Victory is yours!
        """

    @staticmethod
    def modify_player(player):
        player.victory = True
