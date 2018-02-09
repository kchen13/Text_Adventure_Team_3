import actions
import enemies
import items
import world
import mod_slow_text
import vlc
import time

class MapTile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def intro_text(self):
        raise NotImplementedError()

    def modify_player(self, player):
        raise NotImplementedError()

    def adjacent_moves(self):
        """Returns all move actions for adjacent tiles."""
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
        """Returns all of the available actions in this room."""
        moves = self.adjacent_moves()
        moves.append(actions.ViewInventory())

        return moves


class StartingRoom(MapTile):
    sound_file = vlc.MediaPlayer("C:\Users\billy\Desktop\Mysterious-synth-pad-104-bpm.mp3")
    sound_file.play()
    time.sleep(10)
    #sound_file.stop()
    # override the intro_text method in the superclass
    def intro_text(self):
        return mod_slow_text.slow_text('The year is 1835 and your player is a well respected doctor in Philadelphia.\n'
                                       'One day, the temperature drops dramatically in the hospital and the power\n'
                                       'goes out. You are alone with your latest project. A wide spread disease has\n'
                                       'spread across the city and you are working on your test subject Frank. You\n'
                                       'have replaced many of Frank’s body parts with machinery but without\n'
                                       'electricity, you have to abandon him. The dropping temperature is causing you\n'
                                       'to look for supplies and search for a warm safe environment. You leave\n'
                                       'Frank’s room and have a few options where to look for supplies.\n')

    def modify_player(self, player):
        # Room has no action on player
        pass


class LootRoom(MapTile):
    def __init__(self, x, y, item):
        self.item = item
        super().__init__(x, y)

    def add_loot(self, player):
        player.inventory.append(self.item)

    def modify_player(self, player):
        self.add_loot(player)


class EnemyRoom(MapTile):
    def __init__(self, x, y, enemy):
        self.enemy = enemy
        super().__init__(x, y)

    def modify_player(self, the_player):
        if self.enemy.is_alive():
            the_player.hp = the_player.hp - self.enemy.damage
            sound_file = vlc.MediaPlayer("C:\Users\billy\Desktop\Arrow.mp3")
            sound_file.play()
            time.sleep(10)
            # sound_file.stop()
            print("Enemy does {} damage. You have {} HP remaining.".format(self.enemy.damage, the_player.hp))

    def available_actions(self):
        if self.enemy.is_alive():
            return [actions.Flee(tile=self), actions.Attack(enemy=self.enemy)]
        else:
            return self.adjacent_moves()


class EmptyCavePath(MapTile):
    sound_file = vlc.MediaPlayer("C:\Users\billy\Desktop\Mysterious-synth-pad-104-bpm.mp3")
    sound_file.play()
    time.sleep(10)

    # sound_file.stop()
    def intro_text(self):
        return """
        Another unremarkable part of the cave. You must forge onwards.
        """

    def modify_player(self, player):
        # Room has no action on player
        pass


class GiantSpiderRoom(EnemyRoom):
    def __init__(self, x, y):
        super().__init__(x, y, enemies.GiantSpider())

    def intro_text(self):
        sound_file = vlc.MediaPlayer("C:\Users\billy\Desktop\creepy-background-daniel_simon (1).mp3")
        sound_file.play()
        time.sleep(10)
        # sound_file.stop()
        if self.enemy.is_alive():
            return """
            A giant spider jumps down from its web in front of you!
            """
        else:
            return """
            The corpse of a dead spider rots on the ground.
            """


class FindDaggerRoom(LootRoom):
    def __init__(self, x, y):
        super().__init__(x, y, items.Dagger())

    sound_file = vlc.MediaPlayer("C:\Users\billy\Desktop\412249_SOUNDDOGS__kn.mp3")
    sound_file.play()
    time.sleep(10)

    # sound_file.stop()
    def intro_text(self):
        return """
        Your notice something shiny in the corner.
        It's a dagger! You pick it up.
        """


class LeaveCaveRoom(MapTile):
    def intro_text(self):
        sound_file = vlc.MediaPlayer("C:\Users\billy\Desktop\Heavenly Choir Sound Effect.mp3")
        sound_file.play()
        time.sleep(10)

        # sound_file.stop()
        return """
        You see a bright light in the distance...
        ... it grows as you get closer! It's sunlight!
 
 
        Victory is yours!
        """

    def modify_player(self, player):
        player.victory = True


class DecreaseHealth(MapTile):
    def intro_text(self):
        return mod_slow_text.slow_text("This is a test room for decreasing player health")

    def modify_player(self, player):
        player.hp -= 5
        print('This room is very cold, you lost 5 health. Your HP is currently:', player.hp)
