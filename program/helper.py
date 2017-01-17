"""Validates int and float types and specified ranges"""

__author__ = "Jacob Lydon"
__copyright__ = "Copyright 2017"
__credits__ = []

__license__ = "GPLv3"
__version__ = "0.1"
__maintainer__ = "Jacob Lydon"
__email__ = "jlydon001@regis.edu"
__status__ = "Development"


def float_in_range(value, low, high):
    """Checks if user input is number and within desired range.

    :param value: Float input to check.
    :param low: Float low range.
    :param high: Float high range.
    :return: Float validated input.
    """
    while True:
        try:
            user_input = float(input(value))

        except ValueError:
            print("Range is", low, "to", high)

        else:
            if low <= user_input <= high:
                return user_input
            else:
                print("Range is", low, "to", high)


def int_in_range(value, low, high):
    """Checks if user input is int and within desired range.

    :param value: Int input to check.
    :param low: Int low range.
    :param high: Int high range.
    :return: Int validated input.
    """
    while True:
        try:
            user_input = int(input(value))

        except ValueError:
            print("Range is", low, "to", high)

        else:
            if low <= user_input <= high:
                return user_input
            else:
                print("Range is", low, "to", high)
