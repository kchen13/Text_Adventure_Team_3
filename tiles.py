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
            moves.append(actions.MoveEast())
        if world.tile_exists(self.x - 1, self.y):
            moves.append(actions.MoveWest())
        if world.tile_exists(self.x, self.y - 1):
            moves.append(actions.MoveNorth())
        if world.tile_exists(self.x, self.y + 1):
            moves.append(actions.MoveSouth())
        return moves

    def available_actions(self):
        # Returns available actions
        moves = self.adjacent_moves()
        moves.insert(0, actions.ViewRoomInventory())
        moves.append(actions.PlayerStats())
        moves.append(actions.ViewInventory())
        return moves


class StartingRoom(MapTile):
    room_inventory = []

    def intro_text(self):
        mod_sound_effects.background()
        if mod_movement_history.check_history('StartingRoom'):
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
                                    'look for supplies.\n')
        else:
            print('Doc, what are you smoking? You started here. Get moving!')
        return """"""

    def modify_player(self, player):
        # Room has no action on player
        pass


class ColdRoom(MapTile):
    room_inventory = []

    def intro_text(self):
        mod_sound_effects.cold()
        if mod_movement_history.check_history('ColdRoom'):
            mod_slow_text.slow_text("\nA cold fierce wind hits your body.")
        else:
            mod_slow_text.slow_text("\nA cold fierce wind reminds you that you've been here before.")
        return """"""

    def modify_player(self, player):
        # Armor HP percentage subtracted from damage taken
        player.hp -= 5 - (player.armor * 0.1)
        print('You lost 5 health. Your HP is currently:', player.hp, '\n')


class SupplyRoom01(MapTile):
    room_inventory = [items.DoctorsCoat()]

    def intro_text(self):
        mod_sound_effects.supply()
        if mod_movement_history.check_history('SupplyRoom1'):
            mod_slow_text.slow_text("\nIt's some sort of supplies room. Searching may be of your best interest.")
        else:
            mod_slow_text.slow_text("\nThis is that supply room you were in earlier.")
        return """"""

    def modify_player(self, player):
        player.hp -= 2 - (player.armor * 0.1)
        print('Your body temperature is dropping. You lost 2 health. Your HP is currently:', player.hp, '\n')


class EnemyRoom(MapTile):
    def __init__(self, x, y, enemy):
        self.enemy = enemy
        super().__init__(x, y)

    def modify_player(self, the_player):
        if self.enemy.is_alive():
            the_player.hp = the_player.hp - self.enemy.damage
            print("Enemy does {} damage. You have {} HP remaining.".format(self.enemy.damage, the_player.hp))

    def available_actions(self):
        if self.enemy.is_alive():
            return [actions.Flee(tile=self), actions.Attack(enemy=self.enemy)]
        else:
            return self.adjacent_moves()


class GiantSpiderRoom(EnemyRoom):
    def __init__(self, x, y):
        super().__init__(x, y, enemies.GiantSpider())

    def intro_text(self):
        if self.enemy.is_alive():
            return """
            A giant spider jumps down from its web in front of you!
            """
        else:
            return """
            The corpse of a dead spider rots on the ground.
            """


class LeaveCaveRoom(MapTile):
    def intro_text(self):
        return """
        You see a bright light in the distance...
        ... it grows as you get closer! It's sunlight!
 
 
        Victory is yours!
        """

    def modify_player(self, player):
        player.victory = True
