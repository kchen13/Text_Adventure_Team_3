# Author: Kelby Chen
# Purpose: Check user input for error handling


def yes_or_no(prompt):
    """
    Tests for yes and no inputs
    :param prompt: user input
    :return: y or n
    """
    while True:
        try:
            value = input(prompt)
        except ValueError:
            print('You have to enter "y" or "n", please try again.')
            continue
        if value.lower() not in ('y', 'n'):
            print('Incorrect input, please try again.')
            continue
        else:
            break
    return value.lower()


def item_select(prompt, max_item):
    """
    Tests for integer and range for item selection
    :param prompt: user input
    :param max_item: list length
    :return: index of item + 1
    """
    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print('You have to enter a number from 1 to ', max_item, '(0 to exit)')
            continue
        if not 0 <= value <= max_item:
            print('Incorrect input, please try again.')
            continue
        else:
            break
    return value


def inventory_action(prompt):
    while True:
        try:
            value = input(prompt)
        except ValueError:
            print('You have to enter "u", "d" or "x", please try again.')
            continue
        if value.lower() not in ('u', 'd', 'x'):
            print('Incorrect input, please try again.')
            continue
        else:
            break
    return value.lower()


def speak_select(prompt, max):
    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print('You have to enter a number from 1 to ', max)
            continue
        if not 1 <= value <= max:
            print('Incorrect input, please try again.')
            continue
        else:
            break
    return value


def companion_action(prompt):
    while True:
        try:
            value = input(prompt)
        except ValueError:
            print('You have to enter "h" or "x", please try again.')
            continue
        if value.lower() not in ('h', 'x'):
            print('Incorrect input, please try again.')
            continue
        else:
            break
    return value.lower()
