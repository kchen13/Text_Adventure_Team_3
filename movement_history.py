# Author: Kelby Chen


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
