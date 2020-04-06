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
    sheet_output, metric_dictionary, datetimes, hpo_names):
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
    """

    dataframes_dict = create_dataframe_skeletons(
        sheet_output=sheet_output,
        metric_dictionary=metric_dictionary,
        datetimes=datetimes,
        hpo_names=hpo_names)

    print(dataframes_dict)
