"""Queries, calculates, and prints computer science grad school acceptance
chances.

Calculation is based on user-data scraped from grad-cafe.com into MySQL
database.
"""

import random
import scipy.stats as stats
import pymysql
from statistics import stdev

__author__ = "Jacob Lydon"
__copyright__ = "Copyright 2017"
__credits__ = []

__license__ = "GPLv3"
__version__ = "0.1"
__maintainer__ = "Jacob Lydon"
__email__ = "jlydon001@regis.edu"
__status__ = "Development"


def chance_query(db_connection, schools):
    """Queries csdata database for chosen schools.

    Fetches the following data for each school and degree type, where
    at least 1 applicant was accepted or rejected in database:
        - Number of applicants
        - Degree
        - Accepted
        - Rejected
        - GPA (avg. and std. dev.)
        - GRE Quantitative (avg. and std. dev.)
        - GRE Verbal (avg. and std. dev.)
        - GRE Combined (avg. and std. dev.)
        - GRE A/W (avg. and std. dev.)

    :param db_connection: Database connection to csdata.
    :param schools: List of potential schools.
    :return: Cursor for queried data.
    """
    cursor = db_connection.cursor(pymysql.cursors.DictCursor)
    phd_query = ""
    ms_query = ""

    for school in schools:
        if school['PhD'] == 'Yes':
            phd_query += "School LIKE '" + school['Name'] + "' OR "
        if school['MS'] == 'Yes':
            ms_query += "School LIKE '" + school['Name'] + "' OR "

    if phd_query == "":
        phd_query = "School LIKE 'No school was selected' OR "
    if ms_query == "":
        ms_query = "School LIKE 'No school was selected' OR "

    phd_query = phd_query[:-3]
    ms_query = ms_query[:-3]

    select_query = """
        SELECT * FROM (SELECT
            School,
            COUNT(ID) AS Applicants,
            Degree,
            COALESCE(SUM(Status LIKE "Accepted"), 0) AS Accepted,
            COALESCE(SUM(Status LIKE "Rejected"), 0) AS Rejected,
            (AVG(GPA) + 0E0) AS GPA,
            STDDEV_SAMP(GPA) As GPADev,
            (AVG(GREV) + 0E0) AS Verbal,
            STDDEV_SAMP(GREV) AS VerbalDev,
            (AVG(GREQ) + 0E0) AS Quant,
            STDDEV_SAMP(GREQ) AS QuantDev,
            (AVG(GRET) + 0E0) AS Combined,
            STDDEV_SAMP(GRET) CombinedDev,
            (AVG(GREAW) + 0E0) AS AW,
            STDDEV_SAMP(GREAW) AS AWDev
        FROM csdata
        WHERE (Degree = "PhD" AND (""" + phd_query + """)) OR (Degree = "MS" AND (""" + ms_query + """))
        GROUP BY School, Degree) AS Inner_Table
        WHERE (Accepted + Rejected) > 0
        """

    cursor.execute(select_query)
    return cursor


def chance_calc(db_connection, user_data, schools):
    """Calculates an acceptance chance for each potential school and degree.

    Student profile data and school data are analyzed to produce an estimated
    chance of acceptance.

    Algorithm:
    1.  Calc sample acceptance rate.
    2.  Correct to avoid math errors in the case of 100% acceptance or rejection.
    3.  Calc z-scores for all known user-data.
    4.  Calc 99% confident high and low range for actual acceptance.
    5.  Calc inverse of CDF for high, sample, low accepted numbers.
            - Sets sample acceptance rate z-score.
    6.  Sets the z-score standard deviation. The distribution is modified such
        that the deviation below the acceptance rate z-score is short-tailed
        based on the std. dev. of the step 5 calcs. Above the acceptance rate,
        the distribution is long tailed out to a z-score of 3.
            - The effect is that there is much more certainty of rejection
            below the acceptance rate z-score than acceptance above.
            - Example:
                Carnegie Mellon University (CMU) - PhD
                Sample Acceptance Rate: 28.02% (195 Accepted - 501 Rejected)
                Low Likely Accepted: 168
                High Likely Accepted: 223
                Low z-score: 0.702
                Sample z-score: 0.582
                High z-score: 0.467
                Below Std. Dev.: 0.118
                Above Std. Dev.: 0.806

                To illustrate the effect, students with respective z-scores of
                0.464 and 1.388 are both 1.0 std. dev. from 0.582 (mean z-score).
    7.  Monte Carlo simulation to account for unknowns. 1000 student profile
        instances are given a weighted average z-score, which is compared with
        step 5 and 6 calcs to give an instance chance. Chance is the average
        of the instance chances.

        LOR, SOP, and Research are random variables between their respective
        inputted ranges converted to z-scores. Category weights are random
        variables between the following ranges (qualitatively based mostly on
        quora.com answers):
            - LOR 15 to 30
            - SOP 15 to 30
            - Research 15 to 30
            - GPA 7.5
            - Other GPA 7.5
            - Quant 10 to 15
            - Verbal 1 to 5
            - Combined 1 to 5
            - AW 1 to 5

    :param db_connection: Database connection to csdata.
    :param user_data: Ordered Dictionary containing student profile data.
    :param schools: List of potential schools.
    :return: List of potential schools, with data and calculated chance.
    """
    cursor = chance_query(db_connection, schools)
    item = cursor.fetchone()

    while item is not None:
        school_data = item

        # Algorithm Step 1.
        school_data['Accept Rate'] = float(school_data["Accepted"]) / (float(school_data['Accepted'])
                                                                       + float(school_data["Rejected"]))
        school_data['Applied'] = float(school_data['Accepted'] + school_data['Rejected'])

        # Algorithm Step 2.
        if school_data['Accept Rate'] == 1:
            test_accept_rate = .99
        elif school_data['Accept Rate'] == 0:
            test_accept_rate = 0.01
        else:
            test_accept_rate = school_data['Accept Rate']

        # Algorithm Step 3.
        try:
            z_gpa = (user_data['GPA'] - school_data["GPA"]) / school_data['GPADev']
        except (ValueError, ZeroDivisionError):
            z_gpa = 0.1
        try:
            z_other_gpa = (user_data['Other GPA'] - school_data["GPA"]) / school_data['GPADev']
        except (ValueError, ZeroDivisionError):
            z_other_gpa = 0.1
        try:
            z_verbal = (user_data['Verbal'] - school_data["Verbal"]) / school_data["VerbalDev"]
        except (ValueError, ZeroDivisionError):
            z_verbal = 2.0
        try:
            z_quant = (user_data['Quant'] - school_data["Quant"]) / school_data["QuantDev"] / school_data["QuantDev"]
        except (ValueError, ZeroDivisionError):
            z_quant = 2.0
        try:
            z_combined = ((user_data['Quant'] + user_data['Verbal']) - school_data["Combined"]) \
                         / school_data["CombinedDev"]
        except (ValueError, ZeroDivisionError):
            z_combined = 5.0
        try:
            z_aw = (user_data['AW'] - school_data["AW"]) / school_data["AWDev"] / school_data['AWDev']
        except (ValueError, ZeroDivisionError):
            z_aw = 0.5

        # Algorithm Step 4.
        school_data['Accept High'] = stats.binom.ppf(.99, school_data['Applied'], test_accept_rate)
        school_data['Accept Low'] = stats.binom.isf(.99, school_data['Applied'], test_accept_rate)

        # Algorithm Step 5.
        if school_data['Accept High'] == school_data['Applied']:
            high = stats.norm.ppf(0.001)
        else:
            high = stats.norm.ppf(1 - (school_data['Accept High'] / school_data['Applied']))
        if school_data['Accept Low'] == 0:
            low = stats.norm.ppf(.999)
        else:
            low = stats.norm.ppf(1 - (school_data['Accept Low'] / school_data['Applied']))
        sample = stats.norm.ppf(1 - test_accept_rate)

        # Algorithm Step 6.
        below_avg_stdev = stdev([high, sample, low])
        above_avg_stdev = (3 - sample) / 3

        # Algorithm Step 7.
        instances = 1000
        chance_sum = 0
        for i in range(0, 1000):
            z_lor = stats.norm.ppf((random.randint(user_data["LOR Low"], user_data["LOR High"])) / 100)
            z_sop = stats.norm.ppf((random.randint(user_data["SOP Low"], user_data["SOP High"])) / 100)
            z_research = stats.norm.ppf((random.randint(user_data["Research Low"],
                                                        user_data["Research High"])) / 100)

            weights = {"LOR": random.randint(15, 30),
                       "SOP": random.randint(15, 30),
                       "Research": random.randint(15, 30),
                       "GPA": 7.5,
                       "Quant": random.randint(10, 15),
                       "Verbal": random.randint(1, 5),
                       "Combined": random.randint(1, 5),
                       "AW": random.randint(1, 5)}

            sum_instance = z_lor * weights["LOR"] + z_sop * weights["SOP"] + z_research * weights["Research"] \
                           + z_gpa * weights["GPA"] + z_other_gpa * weights["GPA"] + z_quant * weights["Quant"] \
                           + z_verbal * weights["Verbal"] + z_combined * weights["Combined"] + z_aw * weights["AW"]

            z_score_instance = sum_instance / sum(weights.values())

            if z_score_instance > sample:
                chance_sum += stats.norm.cdf(z_score_instance, sample, above_avg_stdev)
            else:
                chance_sum += stats.norm.cdf(z_score_instance, sample, below_avg_stdev)

            school_data['Chance'] = chance_sum / instances * 100

        for school in schools:
            if school['Name'] == school_data["School"] and school[school_data["Degree"]] == "Yes":
                school[str(school_data["Degree"]) + " Chance"] = school_data['Chance'] / 100

        chance_print(school_data)

        item = cursor.fetchone()

    db_connection.close()

    return schools


def chance_print(school_data):
    """Prints school data and user acceptance chances.

    Example:
        Carnegie Mellon University (CMU) - PhD
        Sample Acceptance Rate: 28.02% (195 Accepted - 501 Rejected)
        Sample GPA: 3.75 (Avg) - 0.25 (Std Dev)
        Sample GRE Quant: 166.4 (Avg) - 3.7 (Std Dev)
        Sample GRE Verbal: 159.2 (Avg) - 7.7 (Std Dev)
        Sample GRE A/W: 4.2 (Avg) - 0.8 (Std Dev)

        Based on the sample data, between 168 - 223 out of 696 applications are likely to be accepted.
        Your chance at Carnegie Mellon University (CMU) - PhD acceptance: 2.0%

    :param school_data: Dict containing school data and calculated chance.
    :return:
    """
    print(school_data["School"], "-", school_data["Degree"])
    print("Sample Acceptance Rate:", str(round(school_data["Accept Rate"] * 100, 2)) + "% (" +
          str(school_data["Accepted"]), "Accepted -", school_data["Rejected"], "Rejected)")
    print("Sample GPA:", str(round(school_data["GPA"], 2)), "(Avg) -",
          str(round(school_data["GPADev"], 2)), "(Std Dev)")
    print("Sample GRE Quant:", round(school_data["Quant"], 1), "(Avg) -",
          round(school_data["QuantDev"], 1), "(Std Dev)")
    print("Sample GRE Verbal:", round(school_data["Verbal"], 1), "(Avg) -",
          round(school_data["VerbalDev"], 1), "(Std Dev)")
    print("Sample GRE A/W:", round(school_data["AW"], 1), "(Avg) -",
          round(school_data["AWDev"], 1), "(Std Dev)")

    print("\nBased on the sample data, between", int(school_data['Accept Low']), "-", int(school_data['Accept High']),
          "out of", int(school_data['Applied']), "applications are likely to be accepted.")

    if school_data['Chance'] < 1:
        print("Your chance at", school_data["School"], "-", school_data["Degree"], "acceptance:",
              str(round(school_data['Chance'], 3)) + "%", "\n")
    else:
        print("Your chance at", school_data["School"], "-", school_data["Degree"], "acceptance:",
              str(int(school_data['Chance'])) + "%", "\n")
