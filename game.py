import mod_slow_text
import mod_sound_effects
import world
from player import Player
import time


def play():
    world.load_tiles()
    player = Player()
    # These lines load the starting room and display the text
    room = world.tile_exists(player.location_x, player.location_y)
    print(room.intro_text(player))
    while player.is_alive() and not player.victory:
        room = world.tile_exists(player.location_x, player.location_y)
        # Check to see if player moved before modding player
        if player.last_position(player.location_x, player.location_y):
            room.modify_player(player)
        if player.is_alive() and not player.victory:
            print("Choose an action:")
            available_actions = room.available_actions(player)
            for action in available_actions:
                print(action)
            action_input = input('Action: ')
            for action in available_actions:
                if action_input == action.hotkey:
                    player.do_action(action, **action.kwargs)
                    break
    if player.victory:
        time.sleep(1)
        mod_slow_text.super_slow('                ************************************\n'
                                 '                *            GAME   OVER           *\n'
                                 '                ************************************\n')
        mod_sound_effects.undead_mob()
        time.sleep(7)
    if not player.victory:
        mod_slow_text.super_slow('The agony of defeat. You have not been able to survive. Your body lays there\n'
                                 'cold and dead forever......\n')
        mod_sound_effects.zombie()
        time.sleep(1)
        mod_slow_text.super_slow('Or maybe not.......\n'
                                 '                ************************************\n'
                                 '                *            GAME   OVER           *\n'
                                 '                ************************************\n')
        mod_sound_effects.undead_mob()
        time.sleep(7)


if __name__ == "__main__":
    # Clears player history visits
    open('history.txt', 'w').close()
    # Starts game
    play()
