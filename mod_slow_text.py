# Author: Kelby Chen
# Purpose: Print text slowly, can be expanded for multiple speeds

import sys
import time

import mod_sound_effects


def slow_text(output):
    """
    Method takes in any string and outputs it slowly on the screen.
    Gives a sense of suspense.
    :param output:
    :return: None
    """
    for letter in output:
        sys.stdout.write(letter)
        sys.stdout.flush()
        time.sleep(0.015)  # Ideal speed 0.015
        mod_sound_effects.typing()


def super_slow(output):
    for letter in output:
        sys.stdout.write(letter)
        sys.stdout.flush()
        time.sleep(0.05)  # Ideal speed 0.015
        mod_sound_effects.typing()
