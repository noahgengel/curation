"""
File is intended to store a number of functions that are
used to create the HPO objects throughtout the script.
"""

from dictionaries_and_lists import full_names, \
    row_count_col_names
from hpo_class import HPO
from startup_functions import load_files
from functions_to_create_dqm_objects import find_hpo_row, \
    get_info


def establish_hpo_objects(dqm_objects):
    """
    Function is used as a 'launch pad' for all of the other functions
    that create HPO objects based on the various DataQualityMetric
    objects

    Parameters
    ----------
    dqm_objects (list): list of DataQualityMetric objects.
        these will eventually be associated to their respective
        HPO objects.

    Return
    ------
    blank_hpo_objects (list): list of the blank HPO objects. there
        should be a unique (and mostly empty) object for each HPO
        and date (total length should be #HPOs times #dates)
    """
    names_to_establish = []
    dates_to_establish = []
    blank_hpo_objects = []

    for obj in dqm_objects:
        name = obj.name
        date = obj.date

        if name not in names_to_establish:
            names_to_establish.append(name)

        if date not in dates_to_establish:
            dates_to_establish.append(date)

    # create unique object for each HPO and date
    for hpo_name in names_to_establish:
        full_name = full_names[hpo_name]

        for date in dates_to_establish:

            hpo = HPO(
              name=hpo_name, full_name=full_name,
              date=date,

              # all of the metric objects to be left blank
              # for the time being

              concept_success=[], duplicates=[],
              end_before_begin=[], data_after_death=[],
              route_success=[], unit_success=[],
              measurement_integration=[], ingredient_integration=[])

            blank_hpo_objects.append(hpo)

    return blank_hpo_objects


def add_dqm_to_hpo_objects(dqm_objects, hpo_objects):
    """
    This function is designed to leverage the internal
    HPO.add_metric_with_string() function to further
    establish what data quality metrics are associated
    with each of the HPO/date combinations.

    Parameters
    ----------
    dqm_objects (list): list of DataQualityMetric objects.
        these will eventually be associated to their respective
        HPO objects.

    hpo_objects (list): list of the blank HPO objects. there
        should be a unique (and mostly empty) object for each HPO
        and date (total length should be #HPOs times #dates)

    Returns
    -------
    hpo_objects (list): list of the HPO objects originally
        provided to the function. these objects, however,
        now have 'metrtics' provisioned accordingly
    """
    for dqm in dqm_objects:
        hpo_name_for_metric = dqm.hpo
        metric_name = dqm.metric

        for hpo in hpo_objects:
            if hpo.name == hpo_name_for_metric:
                hpo.add_metric_with_string(
                    metric=metric_name,
                    dq_object=dqm)

    return hpo_objects


def add_number_total_rows_for_hpo_and_date(
        hpos, date_names):
    """
    Function is used to add further attributes to the HPO
    objects. These are the attributes pertaining to the number
    of rows in each of the tables. These row counts should be
    stored in the 'concept' sheet.

    Parameters
    ----------
    hpos (list): list of the HPO objects. these should
        already have the name and date established at
        the minimum.

    date_names (list): list of the strings that indicate
        the names of the files being ingested. these
        in sequential order.

    Returns
    -------
    hpos (list): list of the HPO objects. now should have the
        attributes for the number of rows filled in.
    """
    sheet_name = 'concept'

    dfs = load_files(
        user_choice=sheet_name, files_names=date_names)

    for df in dfs:  # each date
        #FIXME: need to assert that the dates coincide

        for hpo in hpos:
            hpo_name = hpo.name
            hpo_row = find_hpo_row(
                sheet=df, hpo=hpo_name)

            num_rows_dictionary = get_info(
                sheet=df, row_num=hpo_row,
                percentage=False, sheet_name=sheet_name,
                columns_to_collect=row_count_col_names,
                target_low=False)

            for table_name, value in num_rows_dictionary.items():
                hpo.add_row_count_with_string(
                    table=table_name, value=value
                )

