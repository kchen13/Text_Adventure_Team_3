# Author: Kelby Chen
# Purpose: Check user input for error handling


def yes_or_no(prompt):
    '''
    Tests for yes and no inputs
    :param prompt: Question to be asked
    :return: y or n
    '''
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


def item_drop(prompt, max_item):
    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print('You have to enter a number from 1 to ', max_item)
            continue
        if not 1 <= value <= max_item:
            print('Incorrect input, please try again.')
            continue
        else:
            break
    return value
