# Author: Kelby Chen
# Purpose: Call methods that pertain to companion interactions and companion bonuses
import items
import mod_slow_text
import mod_input_validation
import mod_sound_effects


def hunter_introduction(player):
    # Hunter into
    mod_slow_text.super_slow("The man walks out and he's bundled up well, he's pointing two pistols at you but he\n"
                             "slowly lowers them. He seems to have scavanged quite well out here in the mean streets \n"
                             "of Philadelphia.\n\n"
                             "Figures Voice: The names Hunter. I used to be an outlaw before the madness, cold and\n"
                             "crazy ass monsters started to take out the weak and idiotic. You look cold, where you \n"
                             "headed towards?\n")

    # User choice
    mod_slow_text.slow("(1): Hey Hunter, yea man it's freezing out here. I'm headed towards the smoke, hoping for\n"
                       "     people, warmth and shelter.\n"
                       "(2): You scared the shit out of me, what's your problem? I'm headed towards the smoke, you\n"
                       "in or your not, don't waste my time asshole.\n"
                       "(3): I like your guns and jacket, how bout you hand them over and there won't be a problem?\n")

    selection = mod_input_validation.speak_select('Select a response:', 2)
    if selection == 1:
        mod_slow_text.super_slow("I saw the smoke as well, I'm thinking of going that direction. Hell I'll join ya,\n"
                                 "you look like you could use some company. I got this extra coat in my bag. It'll \n"
                                 "protect better and give you some warmth. Much better than a doctors coat.\n")
        player.inventory.append(items.HeavyCoat())
        mod_sound_effects.inventory_pickup()
        mod_slow_text.slow('You received a Heavy Military Style Coat from Hunter. Hunter will now join you!\n')

    if selection == 2:
        pass

    return
