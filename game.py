import world
from player import Player


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


if __name__ == "__main__":
    # Clears player history visits
    open('history.txt', 'w').close()
    # Starts game
    play()
