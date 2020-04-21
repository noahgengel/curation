"""
This program generates an e-mail from a properly-formatted Excel
file. The e-mail should contain information regarding data quality
for the various AoU HPO sites.
Assumptions
-----------
1. Excel file in question is also imported into this current directory
2. Script also stored with introduction.txt, great_job.txt, and contact_list.py
Code was developed with respect to PEP8 standards
"""
from startup_functions import startup, \
    convert_file_names_to_datetimes

from create_dqms import create_dqm_list

from functions_to_create_hpo_objects import establish_hpo_objects, \
    add_dqm_to_hpo_objects, add_number_total_rows_for_hpo_and_date, \
    sort_hpos_into_dicts

from create_aggregate_objects import \
    create_aggregate_metric_master_function


report1 = 'april_17_2020.xlsx'

report_names = [report1]

sheet_names = [
    'concept', 'data_after_death', 'date_datetime_disparity',
    'drug_routes', 'drug_success', 'duplicates',
    'end_before_begin', 'measurement_units', 'erroneous_dates',
    'sites_measurement', 'person_id_failure_rate']


def create_hpo_objects(dqm_objects, file_names, datetimes):
    """
    Function is used to create the various 'HPO' objects
    that will be used to eventually populate the sheets.

    Parameter
    ---------
    dqm_objects (list): list of DataQualityMetric objects.
        these will eventually be associated to their respective
        HPO objects.

    file_names (list): list of the strings that indicate
        the names of the files being ingested. these
        in sequential order.

    datetimes (list): list of datetime objects that
        represent the dates of the files that are being
        ingested

    Return
    ------
    hpo_objects (list): contains all of the HPO objects. the
        DataQualityMetric objects will now be associated to
        the HPO objects appropriately.

    NOTE
    ----
    The DQM objects that are being established would only
    have 'metrics' that are associated with the user's choice
    of analytics output.
    """
    blank_hpo_objects = establish_hpo_objects(
        dqm_objects=dqm_objects)

    hpo_objects = add_dqm_to_hpo_objects(
        dqm_objects=dqm_objects, hpo_objects=blank_hpo_objects)

    for date in datetimes:
        hpo_objects = \
            add_number_total_rows_for_hpo_and_date(
                hpos=hpo_objects,
                date_names=file_names,
                date=date)

    return hpo_objects


def main():
    """
    Function that executes the entirety of the program.
    """

    all_objects = []

    for metric_choice in sheet_names:
        dfs, hpo_names, target_low, percent_bool = \
            startup(file_names=report_names,
                    metric_choice=metric_choice)

        file_names, datetimes = convert_file_names_to_datetimes(
            file_names=report_names)

        dqm_list = create_dqm_list(
            dfs=dfs, file_names=file_names, datetimes=datetimes,
            user_choice=metric_choice, percent_bool=percent_bool,
            target_low=target_low, hpo_names=hpo_names)

        hpo_objects = create_hpo_objects(
            dqm_objects=dqm_list, file_names=file_names,
            datetimes=datetimes)

        metric_dictionary, hpo_dictionary = sort_hpos_into_dicts(
            hpo_objects=hpo_objects, hpo_names=hpo_names,
            user_choice=metric_choice)

        # since we are looking to calculate aggregate objects for
        # HPOs - not tables
        sheet_output = 'hpo_sheets'

        # creating the aggregate metrics for the HPO
        aggregate_metrics = create_aggregate_metric_master_function(
            metric_dictionary=metric_dictionary,
            hpo_dictionary=hpo_dictionary,
            sheet_output=sheet_output, datetimes=datetimes,
            metric_choice=metric_choice)

        all_objects.extend(hpo_objects)
        all_objects.extend(aggregate_metrics)

    for hpo_object in all_objects:

        failing_metrics = hpo_object.find_failing_metrics()

        try:
            for metric in failing_metrics:
                metric.print_attributes()
        except TypeError:
            pass  # no failing metrics found


if __name__ == "__main__":
    main()
