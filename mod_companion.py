# Author: Kelby Chen
# Purpose: Call methods that pertain to companion interactions and companion bonuses
import items
import mod_slow_text
import mod_input_validation
import mod_sound_effects


class Companion:
    def __init__(self, name, hp, damage):
        self.name = name
        self.hp = hp
        self.damage = damage

    def is_alive(self):
        return self.hp > 0


class Hunter(Companion):
    def __init__(self):
        super().__init__(name="Hunter", hp=100, damage=22)

    def __str__(self):
        return 'Companion: {}\n' \
               '      HP: {}\n' \
               '      Damage: {}\n'.format(self.name, self.hp, self.damage)


def hunter_introduction(player):
    # Hunter into
    mod_slow_text.super_slow("The man walks out and he's bundled up well, he's pointing two pistols at you but he\n"
                             "slowly lowers them. He seems to have scavanged quite well out here in the mean streets \n"
                             "of Philadelphia.\n\n"
                             "Figure's Voice: The names Hunter. I used to be an outlaw before the madness, cold and\n"
                             "crazy ass monsters started to take out the weak and idiotic. You look cold, where you \n"
                             "headed towards?\n")

    # User choice
    mod_slow_text.slow("\n(1): Hey Hunter, yea man it's freezing out here. I'm headed towards the smoke, hoping for\n"
                       "     people, warmth and shelter.\n"
                       "(2): You scared the shit out of me, what's your problem? I'm headed towards the smoke, you\n"
                       "are either in or your not, don't waste my time asshole.\n"
                       "(3): I like your guns and jacket, how bout you hand them over and there won't be a problem?\n")

    selection = mod_input_validation.speak_select('Select a response:', 3)
    if selection == 1:
        mod_slow_text.super_slow("Hunter: I saw the smoke as well, I'm thinking of going that direction. Hell I'll\n"
                                 "join ya, you look like you could use some company. I got this extra coat in my bag.\n"
                                 "It'll protect you better and give you some warmth.\n")
        # Add heavy coat
        player.inventory.append(items.HeavyCoat())
        # Add Hunter
        player.companions.append(Hunter())
        mod_sound_effects.inventory_pickup()
        mod_slow_text.slow('You received a Heavy Military Style Coat from Hunter. Hunter will now join you!\n')
        player.print_companions()

    if selection == 2:
        mod_slow_text.super_slow("Hunter: Well finally I meet a tough summabitch. Literally everyone I've met just\n"
                                 "runs off like I'm boogey man or something. I like it, I like your plan too.\n"
                                 "Here's a jacket to help you out. Unfortunately I only have 3 hands and a third\n"
                                 "pistol, here you guy. Lets role!")
        # Add heavy coat, colt45
        player.inventory.append(items.HeavyCoat())
        player.inventory.append(items.Colt45())
        # Add Hunter
        player.companions.append(Hunter())
        mod_sound_effects.inventory_pickup()
        mod_slow_text.slow('You received a Heavy Military Style Coat and a Colt 45 from Hunter. This must be best\n'
                           'possible decision you have made. Hunter will also now join you!\n')
        player.print_companions()

    if selection == 3:
        mod_slow_text.super_slow("Hunter: What in the world? What's up your ass man. I was gonna help you out.\n"
                                 "\nHe raises his gun at you and fires.\n")
        mod_sound_effects.colt45()
        mod_slow_text.super_slow("You quickly try to take cover as he is still firing shots, you're hit. This is\n"
                                 "the absolutely worst decision you've ever made. You're now safe behind a wall.\n")
        mod_sound_effects.colt45()
        mod_slow_text.super_slow("The firing stops. Thank god! You take a peak and he's ran off. Either he didn't\n"
                                 "want to waste his bullets or he has mercy. You took some damage though.\n")
        player.hp -= 40
        mod_slow_text.super_slow("Your HP: " + str(player.hp))

    return
