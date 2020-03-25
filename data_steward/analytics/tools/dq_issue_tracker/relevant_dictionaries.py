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

full_names: allows one to use the hpo_id (shorter) name to find
    the longer (more human-readable) name

metric_names: keys for the sheet in the dataframe and values
    for the name of the corresponding attribute for the HPO
    object
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


full_names = {
    "saou_uab_selma": "UAB Selma",
    "saou_uab_hunt": "UAB Huntsville",
    "saou_tul": "Tulane University",
    "pitt_temple": "Temple University",
    "saou_lsu": "Louisiana State University",
    "trans_am_meyers": "Reliant Medical Group (Meyers Primary Care)",
    "trans_am_essentia": "Essentia Health Superior Clinic",
    "saou_ummc": "University of Mississippi",
    "seec_miami": "SouthEast Enrollment Center Miami",
    "seec_morehouse": "SouthEast Enrollment Center Morehouse",
    "seec_emory": "SouthEast Enrollment Center Emory",
    "uamc_banner": "Banner Health",
    "pitt": "University of Pittsburgh",
    "nyc_cu": "Columbia University Medical Center",
    "ipmc_uic": "University of Illinois Chicago",
    "trans_am_spectrum": "Spectrum Health",
    "tach_hfhs": "Henry Ford Health System",
    "nec_bmc": "Boston Medical Center",
    "cpmc_uci": "UC Irvine",
    "nec_phs": "Partners HealthCare",
    "nyc_cornell": "Weill Cornell Medical Center",
    "ipmc_nu": "Northwestern Memorial Hospital",
    "nyc_hh": "Harlem Hospital",
    "ipmc_uchicago": "University of Chicago",
    "aouw_mcri": "Marshfield Clinic",
    "syhc": "San Ysidro Health Center",
    "cpmc_ceders": "Cedars-Sinai",
    "seec_ufl": "University of Florida",
    "saou_uab": "University of Alabama at Birmingham",
    "trans_am_baylor": "Baylor",
    "cpmc_ucsd": "UC San Diego",
    "ecchc": "Eau Claire Cooperative Health Center",
    "chci": "Community Health Center, Inc.",
    "aouw_uwh": "UW Health (University of Wisconsin Madison)",
    "cpmc_usc": "University of Southern California",
    "hrhc": "HRHCare",
    "ipmc_northshore": "NorthShore University Health System",
    "chs": "Cherokee Health Systems",
    "cpmc_ucsf": "UC San Francisco",
    "jhchc": "Jackson-Hinds CHC",
    "aouw_mcw": "Medical College of Wisconsin",
    "cpmc_ucd": "UC Davis",
    "ipmc_rush": "Rush University",
    "va": "United States Department of Veterans Affairs - Boston",
    "saou_umc": "University Medical Center (UA Tuscaloosa)"
}


metrics_names = {
    # field population metrics
    'measurement_units': 'unit_success',
    'drug_routes': 'route_success',

    # integration metrics
    'drug_success': 'drug_integration',
    'sites_measurement': 'measurement_integration',

    # ACHILLES errors
    'end_before_begin': 'end_before_start',
    'data_after_death': 'data_after_death',

    # other metrics
    'concept': 'concept_success',
    'duplicates': 'duplicates'}
