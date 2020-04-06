"""
File is used to organize the information stored in:
    - HPO objects
    - DataQualityMetric objects
    - AggregateMetric objects

into pandas dataframes. These dataframes are intended
to display the information for HPOs on the different
data quality metrics based on the input from the
user.
"""

from setup_dataframes import create_dataframe_skeletons


def organize_dataframes_master_function(
    sheet_output, metric_dictionary, datetimes, hpo_names,
    metric_choice, hpo_dictionary):
    """
    Function is used to carry out the act of creating the
    dataframes with the data quality metrics that were
    associated with the different HPO objects.

    Parameters
    ----------
    sheet_output (string): determines the type of 'output'
        to be generated (e.g. the sheets are HPOs or the
        sheets are tables)

    metric_dictionary (dict): has the following structure
        keys: all of the different metric_types possible
        values: all of the HPO objects that
            have that associated metric_type

    datetimes (list): list of datetime objects that
        represent the dates of the files that are being
        ingested

    hpo_names (list): list of the HPO names that are to be
        put into dataframes (either as the titles of the
        dataframe or the rows of a dataframe)

    metric_choice (str): the type of analysis that the user
        wishes to perform. used to triage whether the function will
        create a 'weighted' or unweighted' metric

    hpo_dictionary (dict): has the following structure
        keys: all of the different HPO IDs
        values: all of the associated HPO objects that
            have that associated HPO ID
    """

    dataframes_dict, tables_or_classes_for_metric = \
    create_dataframe_skeletons(
        sheet_output=sheet_output,
        metric_dictionary=metric_dictionary,
        datetimes=datetimes,
        hpo_names=hpo_names)

    print(dataframes_dict)


def populate_table_df_rows(
    metric_dictionary, datetimes,
    hpo_names, dataframes_dict,
    metric_choice, hpo_dictionary,
    tables_or_classes_for_metric):
    """
    Function is used to populate each 'table/class'
    dataframe row-by row. Each row of this dataframe
    is a different HPO. Each column of this dataframe
    is a date.

    Parameters
    ----------
    sheet_output (string): determines the type of 'output'
        to be generated (e.g. the sheets are HPOs or the
        sheets are tables)

    metric_dictionary (dict): has the following structure
        keys: all of the different metric_types possible
        values: all of the HPO objects that
            have that associated metric_type

    datetimes (list): list of datetime objects that
        represent the dates of the files that are being
        ingested

    dataframes_dict (dict): has the following structure
        key: the 'name' of the dataframe; the name of
            the table/class

        value: the 'skeleton' of the dataframe to be
            created

    metric_choice (str): the type of analysis that the user
        wishes to perform. used to triage whether the function will
        create a 'weighted' or unweighted' metric

    hpo_dictionary (dict): has the following structure
        keys: all of the different HPO IDs
        values: all of the associated HPO objects that
            have that associated HPO ID

    tables_or_classes_for_metric (list): list of the
        tables or classes that apply to this particular
        metric

    Returns
    -------
    """

    # for each dataframe
    for table_class_name, df in dataframes_dict.items():

        # find the metric selected by the user
        for metric_title, hpos in metric_dictionary:
            if len(hpos) > 0:  # the selected metric

                pass

