"""
This file is intended to serve as a 'storing place' for pieces of information
that may change in the future. This also is a great means to sequester pieces
of information that may otherwise 'bog down' the regular code.

Dictionaries
------------
thresholds: thresholds: the point at which a data quality metric (whether too
    high or too low) would be flagged as 'erroneous'. not used in the
    metrics_over_time script yet but has potential future implementations.

choice_dict: correlates the user-specified choice to the corresponding
    page on the analytics report

Prompts
-------
analysis_type_prompt: used to determine what data quality metric the user
    would like to analyze

percentage_dict: correlated a particular analysis choice with whether or
    not it is intended to report out a fixed number (as in the case of
    duplicate records) or a  'percentage' (namely success or failure
    rates)

target_low_dict: indicates whether the metric is intended to be
    minimized (in the case of an 'error') or maximized (in the
    case of a 'success rate')
"""

thresholds = {
    'concept_success_min': 90,
    'duplicates_max': 5,

    'end_before_begin_max': 0,
    'data_after_death_max': 0,

    'drug_ingredient_integration_min': 90,
    'measurement_integration_min': 90,

    'unit_success_min': 85,
    'route_success_min': 85
}


# ----------USED FOR THE STARTUP OF A FILE ---------- #
analysis_type_prompt = \
        "\nWhat kind of analysis over time report would you like " \
        "to generate for each site?\n\n" \
        "A. Duplicates\n" \
        "B. Amount of data following death dates\n" \
        "C. Amount of data with end dates preceding start dates\n" \
        "D. Success rate for concept_id field\n" \
        "E. Population of the 'unit' field in the measurement table (" \
        "only for specified measurements)\n" \
        "F. Population of the 'route' field in the drug exposure table\n" \
        "G. Percentage of expected drug ingredients observed\n" \
        "H. Percentage of expected measurements observed\n" \
        "I. Date consistency across tables \n\n" \
        "Please specify your choice by typing the corresponding letter."

choice_dict = {
    'a': 'duplicates',
    'b': 'data_after_death',
    'c': 'end_before_begin',
    'd': 'concept',
    'e': 'measurement_units',
    'f': 'drug_routes',
    'g': 'drug_success',
    'h': 'sites_measurement',
    'i': 'visit_date_disparity'}

percentage_dict = {
    'duplicates': False,
    'data_after_death': True,
    'end_before_begin': True,
    'concept': True,
    'measurement_units': True,
    'drug_routes': True,
    'drug_success': True,
    'sites_measurement': True,
    'visit_date_disparity': True
}

target_low_dict = {
    'duplicates': True,
    'data_after_death': True,
    'end_before_begin': True,
    'concept': False,
    'measurement_units': False,
    'drug_routes': False,
    'drug_success': False,
    'sites_measurement': False,
    'visit_date_disparity': False
}
