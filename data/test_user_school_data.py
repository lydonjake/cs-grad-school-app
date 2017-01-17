"""Test data for debugging. Can also be used to store and reuse user data."""

from collections import OrderedDict

__author__ = "Jacob Lydon"
__copyright__ = "Copyright 2017"
__credits__ = []

__license__ = "GPLv3"
__version__ = "0.1"
__maintainer__ = "Jacob Lydon"
__email__ = "jlydon001@regis.edu"
__status__ = "Development"


def test_user_data():
    """Test user data for debugging. Also can be used to save user data.

    :return: Ordered Dictionary containing student profile data.
    """

    data = OrderedDict()

    data['GPA'] = 3.6
    data['Other GPA'] = 3.9
    data['Quant'] = 167
    data['Verbal'] = 162
    data['AW'] = 4.0
    data['LOR High'] = 65
    data['LOR Low'] = 45
    data['Research High'] = 90
    data['Research Low'] = 60
    data['SOP High'] = 70
    data['SOP Low'] = 50

    return data


def test_school_data():
    """Test school data for debugging. Also can be used to save school data.

    :return: List of test school data.
    """

    school_0 = {'Name': 'Massachusetts Institute Of Technology (MIT)',
                'Rank': 96.7,
                'PhD': "Yes",
                'MS': "Yes",
                'Backup': 'MS'}

    school_1 = {'Name': 'Princeton University',
                'Rank': 95,
                'PhD': "Yes",
                'MS': "Yes",
                'Backup': 'MS'}

    school_2= {'Name': 'University Of Michigan, Ann Arbor (UMich)',
                'Rank': 85.8,
                'PhD': "Yes",
                'MS': "No",
                'Backup': 'PhD'}

    school_3 = {'Name': 'Harvard University',
                'Rank': 79.3,
                'PhD': "Yes",
                'MS': "Yes",
                'Backup': 'MS'}

    school_4 = {'Name': 'Carnegie Mellon University (CMU)',
                'Rank': 76.8,
                'PhD': "Yes",
                'MS': "No",
                'Backup': 'PhD'}

    school_5 = {'Name': 'Cornell University',
                'Rank': 72.1,
                'PhD': "Yes",
                'MS': "No",
                'Backup': 'PhD'}

    school_6 = {'Name': 'Duke University',
                'Rank': 65.2,
                'PhD': "Yes",
                'MS': "Yes",
                'Backup': 'MS'}

    school_7 = {'Name': 'Michigan State University (MSU)',
                 'Rank': 56.7,
                 'PhD': "No",
                 'MS': "Yes",
                 'Backup': 'MS'}

    school_8 = {'Name': 'University Of California, San Diego (UC San Diego-UCSD)',
                 'Rank': 64.1,
                 'PhD': "Yes",
                 'MS': "Yes",
                 'Backup': 'MS'}

    school_9 = {'Name': 'University Of Maryland, College Park (UMD)',
                 'Rank': 60.2,
                 'PhD': "Yes",
                 'MS': "Yes",
                 'Backup': 'MS'}

    school_10 = {'Name': 'University Of California, Riverside (UC Riverside-UCR)',
                 'Rank': 56.6,
                 'PhD': "Yes",
                 'MS': "Yes",
                 'Backup': 'MS'}

    school_11 = {'Name': 'Oregon State University (ORST)',
                 'Rank': 61.6,
                 'PhD': "No",
                 'MS': "Yes",
                 'Backup': 'MS'}

    school_12 = {'Name': 'University Of British Columbia (UBC)',
                 'Rank': 47.9,
                 'PhD': "No",
                 'MS': "Yes",
                 'Backup': 'MS'}

    school_13 = {'Name': 'Rutgers University',
                 'Rank': 57.8,
                 'PhD': "Yes",
                 'MS': "Yes",
                 'Backup': 'MS'}

    school_14 = {'Name': 'Simon Fraser University (SFU)',
                 'Rank': 48.3,
                 'PhD': "No",
                 'MS': "Yes",
                 'Backup': 'MS'}

    school_15 = {'Name': 'McGill University',
                 'Rank': 44.7,
                 'PhD': "No",
                 'MS': "Yes",
                 'Backup': 'MS'}

    return [school_0, school_1, school_2, school_3, school_4, school_5, school_6, school_7, school_8,
            school_9, school_10, school_11, school_12, school_13, school_14, school_15]
