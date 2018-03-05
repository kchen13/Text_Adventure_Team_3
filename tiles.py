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
                "be people there? Smoke, fire, and warmth is a sound decision?\n"
                "You look towards the west the familiar direction of your home. How much has your\n"
                "house been ransacked and scavanged? Is it worth the detour to try and get supplies\n"
                "at your home? Are there memories or belongings you hold dear?\n")
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
    room_id = 'street parallel to the smoke'
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
    room_id = 'street parallel to the smoke'
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
        mod_slow_text.slow('It is frigid out here!\nYou lost {} health.\nYour HP is currently: {}\n'
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


class SnowyPath01(MapTile):
    room_id = 'a cold snowy path.'
    room_inventory = []

    def intro_text(self, the_player):
        coordinates = mod_movement_history.get_coordinates(self)
        mod_sound_effects.wind()
        if mod_movement_history.check_history(coordinates):
            mod_slow_text.super_slow("\nThere might be a way around this way. It starts snowing and the wind picks\n"
                                     "up. The sound of rustling trash in the distance.\n")
        else:
            mod_slow_text.slow("\nStill snowing here, want to build a snowman?\n")
        return """"""

    @staticmethod
    def modify_player(player):
        damage = 15 - (player.armor * 0.1)
        player.hp -= damage
        mod_slow_text.slow('Your body temperature is dropping.\nYou lost {} health.\nYour HP is currently: {}\n'
                           .format(damage, player.hp))


class AbandonedTruck02(EnemyRoom):
    room_id = 'an abondoned truck'
    room_inventory = [items.Bandages(), items.Bandages()]

    def __init__(self, x, y):
        super().__init__(x, y, enemies.Ghoul())

    def intro_text(self, the_player):
        if self.enemy.is_alive():
            mod_slow_text.super_slow("\nThis truck is beat up, hopefully there's something here........\n")
            mod_sound_effects.giant_ghoul()
            mod_slow_text.slow("Crap... A giant ghoul appears from around the side. He sounds like he's pissed."
                               "\nGhoul HP:" + str(self.enemy.hp))
        else:
            mod_slow_text.slow("\nA dead giant ghoul is a good giant ghoul.")
        return """"""


class SmallAlley02(MapTile):
    room_id = 'a small alley way.'
    room_inventory = [items.FirstAid()]

    def intro_text(self, the_player):
        coordinates = mod_movement_history.get_coordinates(self)
        mod_sound_effects.wind()
        if mod_movement_history.check_history(coordinates):
            mod_slow_text.super_slow("\nThere's less light this way, you hear sounds but can't make them out.\n"
                                     "Appears to be clear and you can see the smoke in the sky this way.")
        else:
            mod_slow_text.slow("\nStay in this alley long enough and you'll become a prostitute for ghouls.\n")
        return """"""

    @staticmethod
    def modify_player(player):
        damage = 17 - (player.armor * 0.1)
        player.hp -= damage
        mod_slow_text.slow('Your body temperature is dropping.\nYou lost {} health.\nYour HP is currently: {}\n'
                           .format(damage, player.hp))


class SmallAlley03(EnemyRoom):
    room_id = 'a small alley way.'
    room_inventory = [items.KevlarJacket()]

    def __init__(self, x, y):
        super().__init__(x, y, enemies.Zombie())

    def intro_text(self, the_player):
        if self.enemy.is_alive():
            mod_slow_text.super_slow("\nYou continue on your quest for warmth. The willingness to live is on a tight\n"
                                     "rope. Still snowing, cold, dark but the smoke isn't too far away now.........\n")
            mod_sound_effects.zombie()
            mod_slow_text.slow("What in the hell is that? A ghoul type creature appears but it is not a ghoul.\n")
            mod_sound_effects.zombie()
            mod_slow_text.slow("Seems to not be missing as much skin but it's blueish skin makes it look frozen. All\n"
                               "remnants of blood are frozen and very blackish. The sound is horrendous, he's like a\n"
                               "zombie or something. The frozen walking dead!"
                               "\nZombie HP:" + str(self.enemy.hp))
        else:
            mod_slow_text.slow("\nWhat is already dead can just be more dead. Give yourself a pat on the back.\n")
        return """"""


class SmallAlley04(MapTile):
    room_id = 'a small alley way.'
    room_inventory = []

    def intro_text(self, the_player):
        coordinates = mod_movement_history.get_coordinates(self)
        mod_sound_effects.wind()
        if mod_movement_history.check_history(coordinates):
            mod_slow_text.super_slow("\nLooks like a dead end up ahead. You walk in despair, thinking of a warm hot\n"
                                     "juicy cheese steak. Or a roast beef sandwich and cheese fries. A hot cup of \n"
                                     "chocolate and then you remember to move your lips as they have almost froze\n"
                                     "shut. The smoke isn't far, there's hope.\n")
        else:
            mod_slow_text.slow("\nMmmmm cheese steaaaaaakssss....\n")
        return """"""

    @staticmethod
    def modify_player(player):
        damage = 17 - (player.armor * 0.1)
        player.hp -= damage
        mod_slow_text.slow('Your body temperature is dropping.\nYou lost {} health.\nYour HP is currently: {}\n'
                           .format(damage, player.hp))


class ZombieTruck01(EnemyRoom):
    room_id = 'towards the smoke, also a truck this way.'
    room_inventory = [items.Bandages()]

    def __init__(self, x, y):
        super().__init__(x, y, enemies.Zombie())

    def intro_text(self, the_player):
        if self.enemy.is_alive():
            mod_slow_text.super_slow("\nThis truck reminds me of when.... there's a hidden path behind this truck...\n")
            mod_sound_effects.zombie()
            mod_slow_text.slow("A frozen zombie jumps out, and screams into your face. It's go time!"
                               "\nZombie HP:" + str(self.enemy.hp))
        else:
            mod_slow_text.slow("\nThe dead frozen zombie lays lifeless, they could probably make a TV show.....")
        return """"""


class FactoryPath(MapTile):
    room_id = 'small path'
    room_inventory = []

    def intro_text(self, the_player):
        coordinates = mod_movement_history.get_coordinates(self)
        mod_sound_effects.wind()
        if mod_movement_history.check_history(coordinates):
            mod_slow_text.super_slow("\nAs you walk through the path, there's light at the end. There's the smoke\n"
                                     "but this is not what was expected. It's a factory building on fire. The smoke\n"
                                     "still rages into the sky and the fire is quite visible.\n")
        else:
            mod_slow_text.slow("\nYou wonder how you have survived so long being so stupid. Amazing.\n")
        return """"""

    @staticmethod
    def modify_player(player):
        damage = 17 - (player.armor * 0.1)
        player.hp -= damage
        mod_slow_text.slow('Your body temperature is dropping.\nYou lost {} health.\nYour HP is currently: {}\n'
                           .format(damage, player.hp))


class Factory(MapTile):
    room_id = 'the Factory up in flames'
    room_inventory = []

    def intro_text(self, the_player):
        coordinates = mod_movement_history.get_coordinates(self)
        mod_sound_effects.wind()
        if mod_movement_history.check_history(coordinates):
            mod_slow_text.super_slow("\nAs you walk closer to the fire, the building burns. This is not the timeline\n"
                                     "you have hoped for. At least there is still fire, maybe there's some sort of\n"
                                     "fuel... supplies....")
            mod_sound_effects.zombie()
            mod_slow_text.super_slow("Oh no! You see a bunched up mob of what looks like zombies that...\n")
            mod_sound_effects.ghoul01()
            mod_slow_text.super_slow("Are surrounding the immediate area. They haven't turned around yet, thank the\n"
                                     "heavens. You freeze and try to not make a sound. What will do?\n")
            mod_sound_effects.zombie()
            mod_sound_effects.ghoul01()
            mod_slow_text.super_slow("You look to your left, a street that goes a bit aways. Could be an opportunity\n"
                                     "at a not so gruesome death. To the right, well shit! The right literally\n"
                                     "mirrors the left. The mob of unfriendly have turn around. Decide quick!\n")
        else:
            mod_slow_text.slow("\nBurn baby burn. Mob of undead up ahead.\n")
        return """"""

    @staticmethod
    def modify_player(player):
        damage = 17 - (player.armor * 0.1)
        player.hp -= damage
        mod_slow_text.slow('Your body temperature is dropping.\nYou lost {} health.\nYour HP is currently: {}\n'
                           .format(damage, player.hp))


class FightUndeadMob(EnemyRoom):
    room_id = 'towards the undead mob.'
    room_inventory = []

    def __init__(self, x, y):
        super().__init__(x, y, enemies.UndeadMob())

    def intro_text(self, the_player):
        if self.enemy.is_alive():
            mod_slow_text.super_slow("\nYou charge like a maniac towards the mob.......\n")
            mod_sound_effects.undead_mob()
            mod_slow_text.slow("You immediately regret this decision. The death of an unknown doctor comes to mind.\n"
                               "\nZombie HP:" + str(self.enemy.hp))
        else:
            mod_slow_text.slow("\nNo way you survived this.")
        return """"""


class Victory01(MapTile):
    room_id = 'street right of the factory'

    def intro_text(self, the_player):
        mod_slow_text.super_slow("You are hauling ass, running fast and hard, almost out of breath. You feel like\n"
                                 "the oxygen is going to freeze inside of your lungs. Full on panic as you start to\n"
                                 "stumble. You look back... they're coming!\n")
        mod_sound_effects.undead_mob()
        mod_slow_text.super_slow("Suddenly a pothole cover lifts up, a human's voice!\n"
                                 "\nMan's voice: If you want to live you better come down under here!\n"
                                 "You slide down right into the pot hole. Fall down 10 feet into frozen sewage. It\n"
                                 "freaking stinks down here but you're alive.\n")
        mod_sound_effects.victory()
        mod_slow_text.super_slow("\nMan's voice: Hey man! I'm Joe Oakes. I know you, you're a doctor right? Well this\n"
                                 "is our means of survival for now. We have all entrances to the tunnels down here\n"
                                 "locked. We have a heat source and generators as well towards our base. This\n"
                                 "community is the future, we are rebuilding and will figure a way to live normal.\n"
                                 "\n You made it doc! These are the lower class survivors but hell, you made it!\n"
                                 "Survived monsters of all sorts and avoided dying from the cold.\n")
        return """"""

    @staticmethod
    def modify_player(player):
        player.victory = True


class Victory02(MapTile):
    room_id = 'street right of the factory'

    def intro_text(self, the_player):
        mod_slow_text.super_slow("You are hauling ass, running fast and hard, almost out of breath. You feel like\n"
                                 "the oxygen is going to freeze inside of your lungs. Full on panic as you start to\n"
                                 "stumble. You look back... they're coming!\n")
        mod_sound_effects.undead_mob()
        mod_slow_text.super_slow("Your whole body is tense, ready for a battle to the death.\n"
                                 "\nMan's voice: If you want to live you better come down under here!\n"
                                 "You slide down right into the pot hole. Fall down 10 feet but it's warm and lovely.\n"
                                 "It's absolutely brilliant down here.\n")
        mod_sound_effects.victory()
        mod_slow_text.super_slow("\nMan's voice: Hey man! I'm Thaddeus. I know you, you're a doctor right? Well this\n"
                                 "is our means of survival for now. All the uppper class civilians made it down here a\n"
                                 "while ago. We have all entrances to the tunnels down here locked and protected at\n"
                                 "all times. I used to be a body builder, plenty of us big muscles were hired by the\n"
                                 "rich folks that had a plan. We have plenty of heat sources and generators setup all\n"
                                 "over the place. Besides being underground this is the most safe and best place to\n"
                                 "be. Welcom to our community!\n"
                                 "\n You made it doc! Survived monsters of all sorts and avoided dying from the cold."
                                 "\n Living with the upper class, you're going to fit right in as a doctor and they\n"
                                 "will all need you down here.\n")
        return """"""

    @staticmethod
    def modify_player(player):
        player.victory = True


class HomePath01(MapTile):
    room_id = 'road that connects to your home and the main street.'
    room_inventory = [items.Axe()]

    def intro_text(self, the_player):
        coordinates = mod_movement_history.get_coordinates(self)
        mod_sound_effects.wind()
        if mod_movement_history.check_history(coordinates):
            mod_slow_text.super_slow("\nThe wind is a constant smack to your face. You shiver and brace yourself\n"
                                     "against the cold and unforgiving wind. The memories of your home give you\n"
                                     "inner warmth that gives you hope and strength. There's a burnt up fireman's\n"
                                     "outfit with remains of a skeleton, may be something is in the area.\n")
        else:
            mod_slow_text.slow("\nGet moving or die, a pretty easy question right?\n")
        return """"""

    @staticmethod
    def modify_player(player):
        damage = 8 - (player.armor * 0.1)
        player.hp -= damage
        mod_slow_text.slow('Your body temperature is dropping.\nYou lost {} health.\nYour HP is currently: {}\n'
                           .format(damage, player.hp))


class HomePath02(EnemyRoom):
    room_id = 'road that connects to your home and the main street.'
    room_inventory = [items.KevlarJacket()]

    def __init__(self, x, y):
        super().__init__(x, y, enemies.Zombie())

    def intro_text(self, the_player):
        if self.enemy.is_alive():
            mod_slow_text.super_slow("\nNot much further till your once beautiful home. The hope and belief that\n"
                                     "there is something there that will help you on your quest for survival is\n"
                                     "strong. You've now started walking faster in desperation and excitement.\n")
            mod_sound_effects.zombie()
            mod_slow_text.slow("What in the hell is that? A ghoul type creature appears but it is not a ghoul.\n")
            mod_sound_effects.zombie()
            mod_slow_text.slow("Seems to not be missing as much skin but it's blueish skin makes it look frozen. All\n"
                               "remnants of blood are frozen and very blackish. The sound is horrendous, he's like a\n"
                               "zombie or something. The frozen walking dead!"
                               "\nZombie HP:" + str(self.enemy.hp))
        else:
            mod_slow_text.slow("\nWhat is already dead can just be more dead. Give yourself a pat on the back.\n")
        return """"""


class Driveway(EnemyRoom):
    room_id = 'driveway in front of your house.'
    room_inventory = [items.FirstAid(), items.Bandages()]

    def __init__(self, x, y):
        super().__init__(x, y, enemies.GiantGhoul())

    def intro_text(self, the_player):
        if self.enemy.is_alive():
            mod_slow_text.super_slow("\nThe coast looks clear your house is in shambles. Emotions are strong but\n"
                                     "you try to remain strong and fight back the tears. A burnt up car sits there\n"
                                     "peacefully. Your coming to terms with the situation......\n")
            mod_sound_effects.giant_ghoul()
            mod_slow_text.slow("You freeze in fear. It is absolutely massive! Looks like this kind of ghoul eats\n"
                               "those other ghouls for lunch. Twice the size and twice the ugly!\n"
                               "\nGiant Ghoul HP:" + str(self.enemy.hp))
        else:
            mod_slow_text.slow("\nA dead giant ghoul lays lifeless, it probably trespassed at the wrong house.\n")
        return """"""


class Home(MapTile):
    room_id = 'home sweet home.'
    room_inventory = [items.Colt45()]

    def intro_text(self, the_player):
        coordinates = mod_movement_history.get_coordinates(self)
        mod_sound_effects.wind()
        if mod_movement_history.check_history(coordinates):
            mod_slow_text.super_slow("\nYou enter through you front door. There isn't much here at all, a complete\n"
                                     "mess. The backdoor leads to a road that should be able to take you back in the\n"
                                     "direction of the smoke. People have already taken their turns looting the\n"
                                     "place. Did they find your hidden pistol though?\n")
        else:
            mod_slow_text.slow("\nHome is where the heart is, unless you want a frozen heart you should probably go.\n")
        return """"""

    @staticmethod
    def modify_player(player):
        damage = 5 - (player.armor * 0.1)
        player.hp -= damage
        mod_slow_text.slow('Your body temperature is dropping.\nYou lost {} health.\nYour HP is currently: {}\n'
                           .format(damage, player.hp))


class Backyard(MapTile):
    room_id = 'backyard of your house.'
    room_inventory = []

    def intro_text(self, the_player):
        coordinates = mod_movement_history.get_coordinates(self)
        mod_sound_effects.wind()
        if mod_movement_history.check_history(coordinates):
            mod_slow_text.super_slow("\nYou can see the smoke in the distance, it's off to the north east. Walking\n"
                                     "around aimlessly is also an option, it's really up to you at this point. While"
                                     "pondering your options you hear a familiar sound. What could be out here?\n")
            mod_sound_effects.good_mystery()
            mod_slow_text.super_slow("\nA German Shepard dog comes out from behind a tree. It's slow to engage,\n"
                                     "you're a bit shocked, your body tenses up gripping your {}.\n\n"
                                     .format(the_player.best_weapon().name))
            mod_sound_effects.dog()
            mod_slow_text.super_slow("\nThe dog is a wearing protective vest. Maybe it was a service dog before.\n"
                                     "It's super friendly, looks like you got yourself a new partner.\n")
            the_player.companions.append(mod_companion.Dog())
            the_player.print_companions()
            mod_sound_effects.dog()

        else:
            mod_slow_text.slow("\nIt's a wall of junk, hoarding trash isn't a smart idea right now.\n")
        return """"""

    @staticmethod
    def modify_player(player):
        damage = 15 - (player.armor * 0.1)
        player.hp -= damage
        mod_slow_text.slow('Your body temperature is dropping.\nYou lost {} health.\nYour HP is currently: {}\n'
                           .format(damage, player.hp))

# TODO: make path back to main path towards fire
