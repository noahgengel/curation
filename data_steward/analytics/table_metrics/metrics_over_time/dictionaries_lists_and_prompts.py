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

percentage_dict: correlated a particular analysis choice with whether or
    not it is intended to report out a fixed number (as in the case of
    duplicate records) or a  'percentage' (namely success or failure
    rates)

target_low_dict: indicates whether the metric is intended to be
    minimized (in the case of an 'error') or maximized (in the
    case of a 'success rate')

columns_to_document_for_sheet: indicates which columns contain
    information that should be stored for the particular data
    quality metric that is being analyzed

table_based_on_column_provided: allows us to determine the table that
    should be associated with a particular Data Quality Dimension object
    based upon the column that was used to get the associated 'value'
    float

data_quality_dimension_dict: shows which attribute of Kahn's Data Quality
    framework the particular 'data quality metric' at hand relates to

metric_type_to_english_dict: allows one to translate the 'metric type'
    that is normally associated with a 'DataQualityMetric' object to
    'English'. this is useful for printing the columns on a new
    dashboard

Prompts
-------
analysis_type_prompt: used to determine what data quality metric the user
    would like to analyze
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

columns_to_document_for_sheet = {
    'measurement_units': ['total_unit_success_rate'],

    'sites_measurement': ['Physical_Measurement',
                          'CMP', 'CBCwDiff', 'CBC',
                          'Lipid', 'All_Measurements'],

    'end_before_begin': [
        'visit_occurrence', 'condition_occurrence',
        'drug_exposure', 'device_exposure'],

    'duplicates': ['visit_occurrence', 'condition_occurrence',
                   'drug_exposure', 'measurement',
                   'procedure_occurrence', 'device_exposure',
                   'observation'],

    'drug_routes': ['total_route_success_rate'],

    'drug_success': [
        'ace_inhibitors', 'painnsaids',	'msknsaids',
        'statins', 'antibiotics', 'opioids',
        'oralhypoglycemics', 'vaccine', 'ccb',
        'diuretics', 'all_drugs'],

    'data_after_death': [
        'visit_occurrence', 'condition_occurrence',
        'drug_exposure', 'measurement',
        'procedure_occurrence', 'observation',
        'device_exposure'],

    'diabetes': [
        'diabetics_w_drugs', 'diabetics_w_glucose',
        'diabetics_w_a1c', 'diabetics_w_insulin'
    ],

    'concept': [
        'observation_success_rate', 'drug_success_rate',
        'procedure_success_rate', 'condition_success_rate'
        'measurement_success_rate', 'visit_success_rate']
}


table_based_on_column_provided = {
    'total_unit_success_rate': 'Measurement',
    'total_route_success_rate': 'Drug Exposure',
    'all_drugs': 'Drug Exposure',
    'All_Measurements': 'Measurement',
    'visit_occurrence': 'Visit Occurrence',
    'condition_occurrence': 'Condition Occurrence',
    'drug_exposure': 'Drug Exposure',
    'device_exposure': 'Device Exposure',
    'measurement': 'Measurement',
    'procedure_occurrence': 'Procedure Occurrence',
    'observation': 'Observation',
    'observation_success_rate': 'Observation',
    'drug_success_rate': 'Drug Exposure',
    'procedure_success_rate': 'Procedure',
    'condition_success_rate': 'Condition Occurrence',
    'measurement_success_rate': 'Measurement',
    'visit_success_rate': 'Visit Occurrence'
}

data_quality_dimension_dict = {
    'concept': 'Conformance',
    'duplicates': 'Plausibility',
    'end_before_begin': 'Plausibility',
    'data_after_death': 'Plausibility',
    'sites_measurement': 'Completeness',
    'drug_success': 'Completeness',
    'drug_routes': 'Completeness',
    'measurement_units': 'Completeness'
}

metric_type_to_english_dict = {
    # field population metrics
    'measurement_units': 'Unit Concept ID Success Rate',
    'drug_routes': 'Route Concept ID Success Rate',

    # integration metrics
    'drug_success': 'Drug Ingredient Integration',
    'sites_measurement': 'Measurement Integration',

    # ACHILLES errors
    'end_before_begin': 'End Dates Preceding Start Dates',
    'data_after_death': 'Data After Death',

    # other metrics
    'concept': 'Concept ID Success Rate',
    'duplicates': 'Duplicate Records'
}
