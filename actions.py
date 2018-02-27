from player import Player


class Action():
    def __init__(self, method, name, hotkey, **kwargs):
        self.method = method
        self.hotkey = hotkey
        self.name = name
        self.kwargs = kwargs

    def __str__(self):
        return "{}: {}".format(self.hotkey, self.name)


class MoveNorth(Action):
    def __init__(self, rm_id):
        super().__init__(method=Player.move_north, name='Move North (' + rm_id + ')', hotkey='n')


class MoveSouth(Action):
    def __init__(self, rm_id):
        super().__init__(method=Player.move_south, name='Move South (' + rm_id + ')', hotkey='s')


class MoveEast(Action):
    def __init__(self, rm_id):
        super().__init__(method=Player.move_east, name='Move East (' + rm_id + ')', hotkey='e')


class MoveWest(Action):
    def __init__(self, rm_id):
        super().__init__(method=Player.move_west, name='Move West (' + rm_id + ')', hotkey='w')


class ViewRoomInventory(Action):
    # Room Inventory
    def __init__(self):
        super().__init__(method=Player.room_inventory, name="Search This Room", hotkey='l')


class ViewInventory(Action):
    # Inventory Menu
    def __init__(self):
        super().__init__(method=Player.print_inventory, name='View Inventory', hotkey='i')


class PlayerStats(Action):
    # Player statistics menu
    def __init__(self):
        super().__init__(method=Player.player_stats, name='Player Statistics', hotkey='p')


class Attack(Action):
    def __init__(self, enemy):
        super().__init__(method=Player.attack, name="Attack", hotkey='a', enemy=enemy)


class Flee(Action):
    def __init__(self, tile):
        super().__init__(method=Player.flee, name="Flee", hotkey='f', tile=tile)
