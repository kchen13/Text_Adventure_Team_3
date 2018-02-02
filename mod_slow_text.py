# Author: Kelby Chen

import sys
import time


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
        time.sleep(0.03)

