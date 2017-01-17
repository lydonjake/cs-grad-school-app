"""Drives CS application program modules.

Run this file to estimate the user's chance of acceptance to an optimized
set of computer science graduate school.

Program Structure:
1.  Enter student profile data. Percentile guesstimates are required for
    letters of recommendation, statement of purpose, and research experience.
2.  Enter schools under consideration and program ranking (0-100). The program
    calculates approximate acceptance chances based on grad-cafe.com user data
    and profile data. Program prints associated data for each school along with
    chances.
3.  Enter a chance threshold for acceptance to at least one school
    (i.e. .995), number of applications, and a confidence adjustment for both
    calculated chances and threshold.
4.  Program calculates the optimal set of schools to which the user should
    apply to maximize school rankings while exceeding the chance threshold.
    Acceptance chances are printed overall, cumulatively and in 3 tiers,
    organized by ranking.
"""

from pymysql import connect, Error
from data.test_user_school_data import test_user_data
from chance import chance_calc
from school_data_io import school_data_in
from user_data_io import user_data_in, user_data_print
from optimize import optimize_overall_calc, optimize_print

__author__ = "Jacob Lydon"
__copyright__ = "Copyright 2017"
__credits__ = []

__license__ = "GPLv3"
__version__ = "0.1"
__maintainer__ = "Jacob Lydon"
__email__ = "jlydon001@regis.edu"
__status__ = "Development"

password = input("Please enter the root user MySQL password: ")

while True:
    """ Connect to MySQL database """
    try:
        conn = connect(host='localhost',
                       database='csdata',
                       user='root',
                       password=password)

    except Error as e:
        print(e, "\nNo database connection. Please restart to try again.")

    else:
        print("On your first try, please use our test student profile and schools to get a feel for the program\n"
              "because there is quite a bit of data entry. The test student has a good profile and is considering\n"
              "16 schools. You may also add additional schools to the test school list.\n")

        if input("Type 'test' to use the test profile (or any other key): ").lower() == "test":
            user_data = test_user_data()
        else:
            user_data = user_data_in()

        user_data_print(user_data)

        if input("\nType 'test' to use the test school list (or any other key): ").lower() == "test":
            schools_consider = school_data_in(conn, True)
        else:
            schools_consider = school_data_in(conn, False)

        schools_consider = chance_calc(conn, user_data, schools_consider)

        while True:
            optimize_schools = optimize_overall_calc(schools_consider)

            optimize_print(optimize_schools)

            if input("\nEnter 'Y' to try different chance parameters (or any other key): ").lower() not in ["y"]:
                break

        if input("\nEnter 'Y' to try restart the program (or any other key): ").lower() not in ["y"]:
            break
