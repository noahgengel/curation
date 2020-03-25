"""
File is meant to contain dictionaries that can be used for the
primary file and/or the HPO class functions.

The dictionaries are as follows:
--------------------------------
relevant_links: the relevant links for the output file
that is established in create_dq_issue_site_dfs.py. This will
help maintain the overall readability of the aforementioned
script

thresholds: the point at which a data quality metric (whether too
high or too low) would be flagged as 'erroneous'
"""

relevant_links = {
    "concept_success":
    "https://sites.google.com/view/ehrupload/data-quality-metrics/concept-success-rate?authuser=0",

    "duplicates":
    "https://sites.google.com/view/ehrupload/data-quality-metrics/duplicates?authuser=0",

    "end_before_start":
    "https://sites.google.com/view/ehrupload/data-quality-metrics/end-dates-preceding-start-dates?authuser=0",

    "data_after_death":
    "https://sites.google.com/view/ehrupload/data-quality-metrics/data-after-death?authuser=0",

    "unit_success":
    "https://sites.google.com/view/ehrupload/data-quality-metrics/unit-concept-success-rate?authuser=0",

    "route_success":
    "https://sites.google.com/view/ehrupload/data-quality-metrics/route-concept-success-rate?authuser=0",

    "measurement_integration":
    "https://sites.google.com/view/ehrupload/data-quality-metrics/measurement-integration-rate?authuser=0",

    "drug_integration":
    "https://sites.google.com/view/ehrupload/data-quality-metrics/drug-ingredient-integration-rate?authuser=0"
}


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
