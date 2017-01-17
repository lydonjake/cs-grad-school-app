"""Optimizes the schools to which a user should apply."""

import itertools
from operator import itemgetter
from helper import float_in_range, int_in_range

__author__ = "Jacob Lydon"
__copyright__ = "Copyright 2017"
__credits__ = []

__license__ = "GPLv3"
__version__ = "0.1"
__maintainer__ = "Jacob Lydon"
__email__ = "jlydon001@regis.edu"
__status__ = "Development"


def optimize_input(num_schools):
    """Gets user parameters to optimize school choice.

    Chance Threshold - the percent chance of acceptance to at least one
    program.
    Adjusted Chance - allows an adjustment to all computed chances. It is
    recommended to choose a lower chance, such as 0.5 or 0.25.
    Adjusted Chance Threshold - slightly lower than Chance Threshold is
    recommended.

    :param num_schools: Int for the number of schools in consideration.
    :return: Dict with optimization parameters.
    """
    optimize_params = dict()

    optimize_params['Chance Threshold'] = float_in_range("Enter a chance threshold for acceptance to at least one "
                                                         "school (i.e. .99): ", 0, 1)
    optimize_params['Num Apps'] = int_in_range("To how many schools will you be applying? ", 0, num_schools)
    optimize_params['Chance Mod'] = float_in_range("Please review your chances. You can adjust them globally to get an "
                                                   "alternate, more/less\nconservative recommendation. Please enter a "
                                                   "multiplier (i.e. .5 or 1.2):", 0, 10)
    optimize_params['Threshold Mod'] = float_in_range("Enter your adjusted chance threshold (i.e. .99): ", 0, 1)

    return optimize_params


def optimize_print(school_list_calcd):
    """Prints the optimized set of schools in which to apply.

    Example Output:
        The following schools maximize your average school rating given your chance thresholds:

        -------- Top Tier Standalone Chance: 62.0% --------

        University Of Michigan, Ann Arbor (UMich) - Rating: 85.8
            PhD Chance: 62.0%
            Chance (This School or Above): 62.0%
            Chance (This School or Above incl. Backup): 62.0%

        -------- Mid Tier Standalone Chance: 22.99% --------

        Harvard University - Rating: 79.3
            PhD Chance: 22.99%
            MS Chance: 43.41%
            Chance (This School or Above): 70.74%
            Chance (This School or Above incl. Backup): 83.44%

        -------- Bottom Tier Standalone Chance: 83.36% --------

        Duke University - Rating: 65.2
            PhD Chance: 57.61%
            MS Chance: 60.08%
            Chance (This School or Above): 87.6%
            Chance (This School or Above incl. Backup): 97.2%

        University Of Maryland, College Park (UMD) - Rating: 60.2
            PhD Chance: 60.75%
            MS Chance: 1.6%
            Chance (This School or Above): 95.13%
            Chance (This School or Above incl. Backup): 98.92%

        Avg School Rating: 72.62

        Total Chance: 95.13%
        Total Chance incl. Backup = 98.92%

        Conservative Total Chance = 69.73%
        Conservative Total Chance incl. Backup = 97.35%

    :param school_list_calcd: Dict containing optimized set of schools and data.
    :return:
    """

    if school_list_calcd["Best Score"] > 0:
        top_printed = False
        mid_printed = False
        bottom_printed = False

        print("\nThe following schools maximize your average school rating given your chance thresholds: ")

        for item, school in enumerate(school_list_calcd["Best Schools"], start=0):
            if school['Tier'] == "Top" and not top_printed:
                print("\n-------- Top Tier Standalone Chance:",
                      str(round(school_list_calcd["Top Tier Chance"] * 100, 2)) + "%", "--------")
                top_printed = True
            elif school['Tier'] == "Mid" and not mid_printed:
                print("\n-------- Mid Tier Standalone Chance:",
                      str(round(school_list_calcd["Mid Tier Chance"] * 100, 2)) + "%", "--------")
                mid_printed = True
            elif school['Tier'] == "Bottom" and not bottom_printed:
                print("\n-------- Bottom Tier Standalone Chance:",
                      str(round(school_list_calcd["Bottom Tier Chance"] * 100, 2)) + "%", "--------")
                bottom_printed = True

            print("\n" + school['Name'], "- Rating:", round(school['Rank'], 2),
                  "\n    PhD Chance: " + str(round(school['PhD Chance'] * 100, 2))
                  + "%" if school['PhD'] == "Yes" else "",
                  "\n    MS Chance: " + str(round(school['MS Chance'] * 100, 2))
                  + "%" if school['MS'] == "Yes" else "",
                  "\n    Chance (This School or Above):", str(round(school['Cumulative Chance'] * 100, 2)) + "%",
                  "\n    Chance (This School or Above incl. Backup):", str(round(school['Cumulative Chance incl. Backup']
                                                                                 * 100, 2)) + "%")

        print("\nAvg School Rating:", str(round(school_list_calcd['Best Score'], 2)))
        print("\nTotal Chance:", str(round(school_list_calcd['Best Chance'] * 100, 2)) + "%")
        print("Total Chance incl. Backup =", str(round(school_list_calcd['Best Total Chance'] * 100, 2)) + "%")
        print("\nConservative Total Chance =", str(round(school_list_calcd['Mod Best Chance'] * 100, 2)) + "%")
        print("Conservative Total Chance incl. Backup =",
              str(round(school_list_calcd['Mod Best Total Chance'] * 100, 2)) + "%")
    else:
        print("\nNo set of schools satisfied your requirements.")


def optimize_overall_calc(schools_consider):
    """Calculates the optimal set of schools in which to apply, given student
    school rankings and optimization parameters.

    Algorithm:
    1.  Get all possible school combinations.
    2.  For each combination:
        2a. Calc the chance of being accepted to at least 1 school in combo.
        2b. Calc the average rating of the combo's schools.
        2c. Store the combo with an average rating that exceeds both chance
            thresholds and the previous optimal average rating.

    :param schools_consider: List of potential schools, with data and calculated chance.
    :return: Dict containing optimized set of schools and data.
    """
    params = optimize_input(len(schools_consider))
    school_list_calcd = {"Best Score": 0,
                         "Best Chance": 0,
                         "Best Total Chance": 0,
                         "Mod Best Chance": 0,
                         "Mod Best Total Chance": 0}

    # Algorithm Step 1.
    school_combinations = list(itertools.combinations(iter(schools_consider), params['Num Apps']))

    # Algorithm Step 2.
    for combo in school_combinations:
        running_sum_rank = 0.0
        running_chance = 1.0
        running_mod_chance = 1.0
        running_chance_including_backup = 1.0
        running_mod_chance_including_backup = 1.0

        # Algorithm Step 2a.
        for school in combo:
            running_sum_rank += school['Rank']

            if school['PhD'] == "Yes":
                phd_chance = school['PhD Chance']
            else:
                phd_chance = 0

            if school['MS'] == "Yes":
                ms_chance = school['MS Chance']
            else:
                ms_chance = 0

            if school['PhD'] == "Yes":
                running_chance *= 1 - phd_chance
                running_mod_chance *= 1 - (phd_chance * params['Chance Mod'])
            else:
                running_chance *= 1 - ms_chance
                running_mod_chance *= 1 - (ms_chance * params['Chance Mod'])

            running_chance_including_backup *= 1 - (phd_chance + ((1 - phd_chance) * ms_chance))
            running_mod_chance_including_backup \
                *= 1 - (phd_chance + ((1 - phd_chance) * ms_chance * params['Chance Mod']))

        chance = 1 - running_chance
        mod_chance = 1 - running_mod_chance
        total_chance = 1 - running_chance_including_backup
        mod_total_chance = 1 - running_mod_chance_including_backup

        # Algorithm Step 2b.
        average = running_sum_rank / len(combo)

        # Algorithm Step 2c.
        if chance > params['Chance Threshold'] and average > school_list_calcd['Best Score'] \
                and mod_total_chance > params['Threshold Mod']:
            school_list_calcd['Best Score'] = average
            school_list_calcd['Best Chance'] = chance
            school_list_calcd['Best Total Chance'] = total_chance
            school_list_calcd['Mod Best Chance'] = mod_chance
            school_list_calcd['Mod Best Total Chance'] = mod_total_chance
            school_list_calcd['Best Schools'] = combo

    if school_list_calcd['Best Score'] > 0:
        school_list_calcd['Best Schools'] = sorted(school_list_calcd['Best Schools'],
                                                   key=itemgetter('Rank'), reverse=True)

        school_list_calcd = optimize_tier_calc(school_list_calcd)

    return school_list_calcd


def optimize_tier_calc(school_list_calcd):
    """Breaks optimized school list into 3 tiers.

    Calculates cumulative chances and chances per tier. Included to approx.
    the "Reach, Target, Backup" paradigm often used by students to sort possible
    applications. Tiers are organized via rank, so its possible to have a higher
    Tier 1 chance than Tier 2, for instance.

    :param school_list_calcd: Dict containing optimized set of schools and data.
    :return: Dict containing optimized set of schools and data in 3 tiers.
    """
    running_top_tier_chance = 1.0
    running_mid_tier_chance = 1.0
    running_bottom_tier_chance = 1.0
    cumulative_chance = 1.0
    cumulative_chance_including_backup = 1.0

    divider = int(len(school_list_calcd['Best Schools']) / 3)
    for item, school in enumerate(school_list_calcd['Best Schools'], start=0):
        if item < divider:
            if school['PhD'] == "Yes":
                phd_chance = school['PhD Chance']
            else:
                phd_chance = 0

            if school['MS'] == "Yes":
                ms_chance = school['MS Chance']
            else:
                ms_chance = 0

            if school['PhD'] == "Yes":
                running_top_tier_chance *= 1 - phd_chance
                cumulative_chance *= 1 - phd_chance
            else:
                running_top_tier_chance *= 1 - ms_chance
                cumulative_chance *= 1 - ms_chance

            school['Tier'] = "Top"

        elif (item < divider * 2 and len(school_list_calcd['Best Schools']) % 3 != 2) \
                or (item <= divider * 2 and len(school_list_calcd['Best Schools']) % 3 == 2):
            if school['PhD'] == "Yes":
                phd_chance = school['PhD Chance']
            else:
                phd_chance = 0

            if school['MS'] == "Yes":
                ms_chance = school['MS Chance']
            else:
                ms_chance = 0

            if school['PhD'] == "Yes":
                running_mid_tier_chance *= 1 - phd_chance
                cumulative_chance *= 1 - phd_chance
            else:
                running_mid_tier_chance *= 1 - ms_chance
                cumulative_chance *= 1 - ms_chance

            school['Tier'] = "Mid"

        else:
            if school['PhD'] == "Yes":
                phd_chance = school['PhD Chance']
            else:
                phd_chance = 0

            if school['MS'] == "Yes":
                ms_chance = school['MS Chance']
            else:
                ms_chance = 0

            if school['PhD'] == "Yes":
                running_bottom_tier_chance *= 1 - phd_chance
                cumulative_chance *= 1 - phd_chance
            else:
                running_bottom_tier_chance *= 1 - ms_chance
                cumulative_chance *= 1 - ms_chance

            school['Tier'] = "Bottom"

        cumulative_chance_including_backup *= 1 - (phd_chance + ((1 - phd_chance) * ms_chance))

        school['Cumulative Chance'] = 1 - cumulative_chance
        school['Cumulative Chance incl. Backup'] = 1 - cumulative_chance_including_backup

    school_list_calcd["Top Tier Chance"] = 1 - running_top_tier_chance
    school_list_calcd["Mid Tier Chance"] = 1 - running_mid_tier_chance
    school_list_calcd["Bottom Tier Chance"] = 1 - running_bottom_tier_chance

    return school_list_calcd
