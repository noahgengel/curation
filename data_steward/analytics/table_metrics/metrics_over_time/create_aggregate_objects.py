"""
These series of functions are used in the creation of
AggregateMetric objects. These are similar to the regular
DataQualityMetric objects except they contain additional
information to better convey the scale in terms of the
number of rows available across all of the different
sites.

Please see the AggregateMetric class documentation for
further information.
"""

from unweighted_aggregate_metric_functions import \
    create_unweighted_aggregate_metrics_for_tables, \
    create_unweighted_aggregate_metrics_for_hpos, \
    create_unweighted_aggregate_metric_for_dates

from weighted_aggregate_metric_functions import \
    create_aggregate_metric_for_dates,\
    create_weighted_aggregate_metrics_for_hpos, \
    create_weighted_aggregate_metrics_for_tables

from dictionaries_lists_and_prompts import metrics_to_weight


def create_aggregate_metric_master_function(
        metric_dictionary, hpo_dictionary,
        sheet_output, datetimes, metric_choice):
    """
    Function is used to identify which type of AggregateMetric
    object to make. The type of AggregateMetric object to create
    is contingent upon the user_choice parameter. See the
    aggregate_metric_classes.py documentation on the attributes
    of the objects to be instantiated.

    Parameters
    ---------
    metric_dictionary (dict): has the following structure
        keys: all of the different metric_types possible
        values: all of the HPO objects that
            have that associated metric_type

    hpo_dictionary (dict): has the following structure
        keys: all of the different HPO IDs
        values: all of the associated HPO objects that
            have that associated HPO ID

    sheet_output (string): determines the type of 'output'
        to be generated (e.g. the sheets are HPOs or the
        sheets are tables)

    datetimes (list): list of datetime objects that
        represent the dates of the files that are being
        ingested

    metric_choice (str): the type of analysis that the user
        wishes to perform. used to triage whether the function will
        create a 'weighted' or unweighted' metric

    Returns
    -------
    aggregate_metrics (list): list of metrics objects
        (AggregateMetricForTable or
        AggregateMetricForHPO & AggregateMetricForDate)
        that contain all of the 'aggregate metrics' to be displayed
    """
    if metric_choice in metrics_to_weight:
        aggregate_metrics = create_weighted_aggregate_metrics(
            sheet_output=sheet_output,
            metric_dictionary=metric_dictionary,
            datetimes=datetimes, hpo_dictionary=hpo_dictionary)

    else:
        aggregate_metrics = create_unweighted_aggregate_metrics(
            sheet_output=sheet_output,
            metric_dictionary=metric_dictionary,
            datetimes=datetimes,
            hpo_dictionary=hpo_dictionary)

    for aggregate_metric in aggregate_metrics:
        s = aggregate_metric.return_attributes_str()
        print(s)

        aggregate_metrics = []

    return aggregate_metrics


def create_weighted_aggregate_metrics(
    sheet_output, metric_dictionary, datetimes, hpo_dictionary):
    """
    Function is used to create 'weighted' aggregate metrics that can
    be useful in terms of data =analysis

    Parameters
    ---------
    metric_dictionary (dict): has the following structure
        keys: all of the different metric_types possible
        values: all of the HPO objects that
            have that associated metric_type

    hpo_dictionary (dict): has the following structure
        keys: all of the different HPO IDs
        values: all of the associated HPO objects that
            have that associated HPO ID

    sheet_output (string): determines the type of 'output'
        to be generated (e.g. the sheets are HPOs or the
        sheets are tables)

    datetimes (list): list of datetime objects that
        represent the dates of the files that are being
        ingested

    Returns
    -------
    aggregate_metrics (list): list of metrics objects
        (AggregateMetricForTable or
        AggregateMetricForHPO & AggregateMetricForDate)
        that contain all of the 'aggregate metrics' to be displayed
    """
    if sheet_output == 'table_sheets':
        aggregate_metrics = create_weighted_aggregate_metrics_for_tables(
            metric_dictionary=metric_dictionary,
            datetimes=datetimes)

    elif sheet_output == 'hpo_sheets':
        aggregate_metrics = create_weighted_aggregate_metrics_for_hpos(
            hpo_dictionary=hpo_dictionary,
            datetimes=datetimes,
            metric_dictionary=metric_dictionary)

        agg_met_for_dates = create_aggregate_metric_for_dates(
            aggregate_metrics=aggregate_metrics)

        aggregate_metrics.append(agg_met_for_dates)

    else:
        raise Exception(
            """Bad parameter input for function 
            create_aggregate_master_function. Parameter provided
            was: {param}""".format(param=sheet_output))

    return aggregate_metrics


def create_unweighted_aggregate_metrics(
    sheet_output, metric_dictionary, datetimes, hpo_dictionary):
    """
    Function is used to create 'weighted' aggregate metrics that can
    be useful in terms of data =analysis

    Parameters
    ---------
    metric_dictionary (dict): has the following structure
        keys: all of the different metric_types possible
        values: all of the HPO objects that
            have that associated metric_type

    hpo_dictionary (dict): has the following structure
        keys: all of the different HPO IDs
        values: all of the associated HPO objects that
            have that associated HPO ID

    sheet_output (string): determines the type of 'output'
        to be generated (e.g. the sheets are HPOs or the
        sheets are tables)

    datetimes (list): list of datetime objects that
        represent the dates of the files that are being
        ingested

    Returns
    -------
    aggregate_metrics (list): list of metrics objects
        (AggregateMetricForTable or
        AggregateMetricForHPO & AggregateMetricForDate)
        that contain all of the 'aggregate metrics' to be displayed
    """
    if sheet_output == 'table_sheets':
        aggregate_metrics = create_unweighted_aggregate_metrics_for_tables(
            metric_dictionary=metric_dictionary,
            datetimes=datetimes)

    elif sheet_output == 'hpo_sheets':
        aggregate_metrics = create_unweighted_aggregate_metrics_for_hpos(
            hpo_dictionary=hpo_dictionary,
            datetimes=datetimes, metric_dictionary=metric_dictionary)

        agg_met_for_dates = create_unweighted_aggregate_metric_for_dates(
            aggregate_metrics=aggregate_metrics)

        aggregate_metrics.append(agg_met_for_dates)

    else:
        raise Exception(
            """Bad parameter input for function 
            create_aggregate_master_function. Parameter provided
            was: {param}""".format(param=sheet_output))

    return aggregate_metrics

