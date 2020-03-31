"""
Goals
------
Program should generate a report (Excel file) that shows
how data quality metrics for each HPO site change over time.

Data quality metrics include:
   1. the number of duplicates per table
   2. number of 'start dates' that precede 'end dates'
   3. number of records that are >30 days after a patient's death date
   4. concept table success rates
   5. population of the 'unit' field in the measurement table
   6. population of the 'route' field in the drug exposure table
   7. proportion of expected ingredients observed
   8. proportion of expected measurements observed

Future data quality metrics should also be easily added to this
script.

ASSUMPTIONS
-----------
1. The user has all of the files s/he wants to analyze in the current
directory

2. The user will know to change the 'report' variables to match the
file names of the .xlsx files in the current working directory.

3. All sheets are saved as month_date_year.xlsx
   - month should be fully spelled (august rather than aug)
   - year should be four digits
   - this name is used to determine the date

5. Assumed certain naming conventions in the sheets
   a. consistency in the column names in the 'concept' tab
   b. total/valid rows are logged in the 'concept' tab as
      (first word of the table type)_total_row or
      (first word of the table type)_well_defined_row
      ex: drug_total_row
"""

from startup_functions import \
    startup, convert_file_names_to_datetimes, \
    understand_sheet_output_type

from data_quality_metric_class import DataQualityMetric

from hpo_class import HPO

from functions_to_create_dqm_objects import find_hpo_row, \
    get_info

from dictionaries_lists_and_prompts import \
    metric_type_to_english_dict, data_quality_dimension_dict, \
    columns_to_document_for_sheet, table_based_on_column_provided

from functions_to_create_hpo_objects import establish_hpo_objects, \
    add_dqm_to_hpo_objects, add_number_total_rows_for_hpo_and_date, \
    sort_hpos_into_dicts

from create_aggregate_objects import create_aggregate_dqms


def create_dqm_objects_for_sheet(
        dataframe, hpo_names, user_choice, metric_is_percent,
        target_low, date):
    """
    Function is used to create DataQualityMetric objects for all of
    the pertinent values on the various sheets being loaded.

    Parameters
    ---------
    dataframe (df): contains the information for a particular dimension
        of data quality on a particular date

    hpo_names (list): list of the strings that should go
        into an HPO ID column. for use in generating HPO objects.

    user_choice (string): represents the sheet from the analysis reports
        whose metrics will be compared over time

    metric_is_percent (bool): determines whether the data will be seen
        as 'percentage complete' or individual instances of a
        particular error

    target_low (bool): determines whether the number displayed should
        be considered a desirable or undesirable characteristic

    date (datetime): datetime object that represents the time that the
        data quality metric was documented (corresponding to the
        title of the file from which it was extracted)

    Returns
    -------
    dqm_objects (list): list of DataQualityMetrics objects
        these are objects that all should have the same
        metric_type, data_quality_dimension, and date attributes

    columns (list): the column names that whose data will be extracted.
        these will eventually be converted to either the rows of
        dataframes or the names of the different dataframes to be
        output.
    """
    # to instantiate dqm objects later on
    metric_type = metric_type_to_english_dict[user_choice]
    dqm_type = data_quality_dimension_dict[user_choice]
    columns = columns_to_document_for_sheet[user_choice]

    dqm_objects = []

    # for each HPO (row) in the dataframe
    for name in hpo_names:
        row_number = find_hpo_row(sheet=dataframe, hpo=name)

        data_dict = get_info(
            sheet=dataframe, row_num=row_number,
            percentage=metric_is_percent, sheet_name=user_choice,
            columns_to_collect=columns,
            target_low=target_low)

        # for each table / class (column) in the dataframe
        for table, data in data_dict.items():
            table_name = table_based_on_column_provided[table]

            new_dqm_object = DataQualityMetric(
                hpo=name, table=table_name, metric_type=metric_type,
                value=data, data_quality_dimension=dqm_type,
                date=date)

            dqm_objects.append(new_dqm_object)

    return dqm_objects, columns


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

# UNIONED EHR COMPARISON
report1 = 'may_10_2019.xlsx'
report2 = 'july_15_2019.xlsx'
report3 = 'october_04_2019.xlsx'
report4 = 'march_19_2020.xlsx'

report_names = [report1, report2, report3, report4]


def main():
    """
    Function that executes the entirety of the program.
    """
    user_choice, percent_bool, target_low, dfs, hpo_names = \
        startup(file_names=report_names)

    file_names, datetimes = convert_file_names_to_datetimes(
        file_names=report_names)

    dqm_list = []

    # creating the DQM objects and assigning to HPOs
    for dataframe, file_name, date in zip(dfs, file_names, datetimes):
        dqm_objects, col_names = create_dqm_objects_for_sheet(
            dataframe=dataframe, hpo_names=hpo_names,
            user_choice=user_choice, metric_is_percent=percent_bool,
            target_low=target_low, date=date)

        dqm_list.extend(dqm_objects)

    hpo_objects = create_hpo_objects(
        dqm_objects=dqm_list, file_names=file_names, datetimes=datetimes)

    metric_dictionary, hpo_dictionary = sort_hpos_into_dicts(
        hpo_objects=hpo_objects, hpo_names=hpo_names,
        datetimes=datetimes)

    sheet_output = understand_sheet_output_type(
        hpo_objects=hpo_objects, hpo_names=hpo_names,
        metric_type=user_choice)



if __name__ == "__main__":
    main()
