"""School data input and output functions."""

import warnings
import pymysql
from data.test_user_school_data import test_school_data
from helper import float_in_range
from pymysql import Error

__author__ = "Jacob Lydon"
__copyright__ = "Copyright 2017"
__credits__ = []

__license__ = "GPLv3"
__version__ = "0.1"
__maintainer__ = "Jacob Lydon"
__email__ = "jlydon001@regis.edu"
__status__ = "Development"


def school_data_in(db_connection, test_schools):
    """Populates a list of schools the user is considering, with user rankings.

    Checks the database for matching string fragments to user input.
        - Example: Enter "Stan" for Stanford and the program searches the
        database for *Stan* (not case sensitive) and fetches all matches.
    Confirms choice by iterating fetched schools in order of data prevalence.
        - More popular schools require fewer letters.
        - Use well-known abbreviations when possible (i.e. UCLA or MIT)
    Inputs user school ranking (0-100).
        - Example: MIT - 99, Harvard - 90, Princeton -89, UCSD - 88, etc.
    Inputs desired degrees.
        - If PhD is desired, user can choose to consider a MS as well.

    :param db_connection: Database connection to csdata.
    :param test_schools: List of test school data.
    :return: List of potential schools.
    """
    cursor = db_connection.cursor(pymysql.cursors.DictCursor)

    warnings.filterwarnings("ignore", category=pymysql.Warning)

    if test_schools:
        schools = test_school_data()
    else:
        schools = []

    while True:
        school_query = input("\nPlease enter a school (i.e Stanford University, Berkeley, or USC) or 'done': ")

        if school_query.lower() == "done":
            if len(schools) > 0:
                break
            else:
                print("At least one school is required.")

        school_match = False
        school = dict()

        try:
            cursor.execute("""
            SELECT School,
                COUNT(ID)AS Total,
                COUNT(case when Degree = "PhD" then Degree end) AS PhD ,
                COUNT(case when Degree = "MS" then Degree end) AS MS ,
                COUNT(case when Degree = "PhD" then GREQ end) AS QuantPhD,
                COUNT(case when Degree = "PhD" then GPA end) AS GPAPhD,
                COUNT(case when Degree = "MS" then GREQ end) AS QuantMS,
                COUNT(case when Degree = "MS" then GPA end) AS GPAMS
            FROM csdata
            WHERE School LIKE '%""" + school_query + """%'
            GROUP BY School
            ORDER BY Total desc
            """)
        except Error as e:
            print(e, "\n")
        else:
            item = cursor.fetchone()

            while item is not None:
                school_data = item

                if input("Did you mean " + school_data['School'] + " ('Y' or any other key): ").lower() in ['y', 'yes']:
                    school['Name'] = school_data['School']
                    school_match = True
                    break
                else:
                    item = cursor.fetchone()

        if school_match and ((school_data['PhD'] > 1 and school_data['QuantPhD'] > 1 and school_data['GPAPhD'] > 1)
                             or (school_data['MS'] > 1 and school_data['QuantMS'] > 1 and school_data['GPAMS'] > 1)):
            school['Rank'] = float_in_range("Rate this school from 0-100 (higher is better): ", 0, 100)

            while True:
                degree_choice = input("Which degree are you applying for (Phd or MS): ")

                if degree_choice.lower() in ['phd', 'ph.d.', 'p', 'ph']:
                    if school_data['PhD'] > 1 and school_data['QuantPhD'] > 1 and school_data['GPAPhD'] > 1:
                        school['PhD'] = "Yes"
                        backup = input("Would you consider a backup MS from " + school['Name']
                                       + " ('Y' or any other key): ")

                        if backup.lower() in ['y', 'yes']:
                            if school_data['MS'] > 1 and school_data['QuantMS'] > 1 and school_data['GPAMS'] > 1:
                                school['Backup'] = 'MS'
                                school['MS'] = 'Yes'
                            else:
                                print("Not enough data to add a backup MS from", school_data['School'])
                                school['Backup'] = 'PhD'
                                school['MS'] = 'No'
                        else:
                            school['Backup'] = 'PhD'
                            school['MS'] = 'No'

                        schools.append(school)
                        break
                    else:
                        print("Not enough data to add a PhD from", school_data['School'])
                elif degree_choice.lower() in ['m', 'ms', 'm.s.', 'masters', "master's"]:
                    if school_data['MS'] > 1 and school_data['QuantMS'] > 1 and school_data['GPAMS'] > 1:
                        school['Backup'] = 'MS'
                        school['MS'] = 'Yes'
                        school['PhD'] = 'No'
                        schools.append(school)
                        break
                    else:
                        print("Not enough data to add an MS from", school_data['School'])
                else:
                    print("Please choose either PhD or MS.")
        elif school_match:
            print("Not enough data to add an MS or a PhD from", school_data['School'])
        else:
            print("No match was found in the database.")
    return schools
