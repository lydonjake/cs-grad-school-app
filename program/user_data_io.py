"""User data input and output functions."""

from collections import OrderedDict
from helper import float_in_range

__author__ = "Jacob Lydon"
__copyright__ = "Copyright 2017"
__credits__ = []

__license__ = "GPLv3"
__version__ = "0.1"
__maintainer__ = "Jacob Lydon"
__email__ = "jlydon001@regis.edu"
__status__ = "Development"


def user_data_in():
    """Inputs and stores student profile data.

    :return: Ordered Dictionary containing student profile data.
    """

    user_data = OrderedDict()

    user_data['GPA'] = ["Cumulative GPA (Convert to US-style 4.0 scale)", 0.0, 4.0]
    user_data['Other GPA'] = ["Other GPA (last 60 credits, major, etc.)", 0.0, 4.0]
    user_data['Quant'] = ["GRE Quantitative", 130, 170]
    user_data['Verbal'] = ["GRE Verbal", 130, 170]
    user_data['AW'] = ["GRE A/W", 0.0, 6.0]
    user_data['LOR High'] = ["Letters of Recommendation Percentile (Highest Guesstimate i.e. 90)", 0, 100]
    user_data['LOR Low'] = ["Letters of Recommendation Percentile (Lowest Guesstimate i.e. 10)", 0, 100]
    user_data['Research High'] = ["Research Experience Percentile (Highest Guesstimate i.e. 90)", 0, 100]
    user_data['Research Low'] = ["Research Experience Percentile (Lowest Guesstimate i.e. 10)", 0, 100]
    user_data['SOP High'] = ["Statement of Purpose Percentile (Highest Guesstimate i.e. 90)", 0, 100]
    user_data['SOP Low'] = ["Statement of Purpose Percentile (Lowest Guesstimate i.e. 10)", 0, 100]

    for key in user_data.keys():
        while True:
            user_input = float_in_range(user_data[key][0] + ": ", user_data[key][1], user_data[key][2])
            if key == 'LOR Low' and user_input >= user_data['LOR High']:
                print(key, "must be lower than", user_data['LOR High'])
            elif key == 'Research Low' and user_input >= user_data['Research High']:
                print(key, "must be lower than", user_data['Research High'])
            elif key == 'SOP Low' and user_input >= user_data['SOP High']:
                print(key, "must be lower than", user_data['SOP High'])
            else:
                user_data[key] = user_input
                break

    return user_data


def user_data_print(user_data):
    """Prints user data.

    :param user_data: Ordered Dictionary containing student profile data.
    :return:
    """
    print("\nYour student profile.")

    for key in user_data.keys():
        print(key + " -", user_data[key])
