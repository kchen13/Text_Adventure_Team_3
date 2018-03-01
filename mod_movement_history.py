# Author: Kelby Chen
# Purpose: Keeps track of where the player has gone.


def check_history(room_entered):
    """
    Returns False if player was in room, else adds room to text file and returns True
    :param room_entered:
    :return:
    """
    if room_entered in open('history.txt').read():
        return False
    else:
        with open("history.txt", "a") as file:
            file.write(room_entered + '\n')
        return True


def get_coordinates(self):
    return str(self.x) + str(self.y)
