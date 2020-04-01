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

from aggregate_metric_classes import AggregateMetricForTable, \
    AggregateMetricForHPO, AggregateMetricForDate

from dictionaries_lists_and_prompts import metrics_to_weight

from auxillary_aggregate_functions import find_relevant_tables, \
    cycle_through_dqms_for_table, cycle_through_dqms_for_hpo, \
    find_unique_dates_and_metrics


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
    else:  # FIXME: integration metrics - should not be weighted
        aggregate_metrics = []

    return aggregate_metrics


def create_weighted_aggregate_metrics_for_tables(
    metric_dictionary, datetimes):
    """
    Function is intended to create 'aggregate' data quality
    metrics that can be applied to a specific data quality metric
    for a particular date (across all HPOs).

    Parameters
    ----------
    metric_dictionary (dict): has the following structure
        keys: all of the different metric_types possible
        values: all of the HPO objects that
            have that associated metric_type

    datetimes (list): list of datetime objects that
        represent the dates of the files that are being
        ingested

    Returns
    -------
    new_aggregate_metrics (list): contains AggregateMetricForTable
        objects that reflect each date, metric, and table combination
    """

    # create a metric type for each
    #    a. metric
    #    b. date
    #    c. table

    new_agg_metrics = []

    # A - really will only go into for applicable metric
    for metric_type, hpo_object_list in metric_dictionary.items():

        tables_for_metric = find_relevant_tables(
            hpo_object_list=hpo_object_list, metric_type=metric_type)
        # now we know the tables and dates for all of the metrics

        # B.
        for date in datetimes:

            # C
            for table in tables_for_metric:
                # to add to the new object's attributes
                total_rows, pertinent_rows = 0, 0

                hpos_counted = []  # need to prevent double-counting

                # now we need to find the relevant DataQualityMetric objects
                for hpo_object in hpo_object_list:

                    if hpo_object.date == date:
                        hpos_counted, total_rows, pertinent_rows = \
                            cycle_through_dqms_for_table(
                                hpo_object=hpo_object,
                                metric_type=metric_type,
                                date=date, table=table,
                                hpos_counted=hpos_counted,
                                total_rows=total_rows,
                                pertinent_rows=pertinent_rows)

                # actually create the metric - culled for all three dimensions

                new_am = AggregateMetricForTable(
                    date=date, table_name=table, metric_type=metric_type,
                    num_total_rows=total_rows, num_pertinent_rows=pertinent_rows)

                new_agg_metrics.append(new_am)

    # finished the loop - now has all the aggregate metrics
    return new_agg_metrics


def create_weighted_aggregate_metrics_for_hpos(
    hpo_dictionary, datetimes, metric_dictionary):
    """
    Function is intended to create 'aggregate' data quality
    metrics that can be applied to a specific data quality metric
    for a particular HPO (across all tables).

    Parameters
    ----------
    hpo_dictionary (dict): has the following structure
        keys: all of the different HPO IDs
        values: all of the associated HPO objects that
            have that associated HPO ID

    datetimes (list): list of datetime objects that
        represent the dates of the files that are being
        ingested

    metric_dictionary (dict): has the following structure
        keys: all of the different metric_types possible
        values: all of the HPO objects that
            have that associated metric_type

    Returns
    -------
    new_aggregate_metrics (list): contains AggregateMetricForHPO
        objects that reflect each date, metric, and HPO combination
        (regardless of table)
    """

    # create a metric type for each
    #    a. HPO
    #    b. date
    #    b. metric

    new_agg_metrics = []

    # A.
    for hpo, hpo_objects in hpo_dictionary.items():

        # B.
        for date in datetimes:

            # C.
            for metric in metric_dictionary:

                total_rows, pertinent_rows = 0, 0

                # need to specify - only check the relevant metric
                if len(hpo_objects) > 0:

                    for hpo_object in hpo_objects:

                        # want to exclude device exposure for now
                        tables_counted = ['Device Exposure']  # need to prevent double-counting

                        if hpo_object.date == date:

                            total_rows, pertinent_rows, tables_counted = \
                                cycle_through_dqms_for_hpo(
                                    hpo_object=hpo_object, metric=metric,
                                    date=date, hpo_name=hpo_object.name,
                                    tables_counted=tables_counted,
                                    total_rows=total_rows,
                                    pertinent_rows=pertinent_rows)

                new_agg_metric = AggregateMetricForHPO(
                    date=date, hpo_name=hpo, metric_type=metric,
                    num_total_rows=total_rows,
                    num_pertinent_rows=pertinent_rows)

                new_agg_metrics.append(new_agg_metric)

    # finished the loop - now has all the aggregate metrics
    return new_agg_metrics


def create_aggregate_metric_for_dates(aggregate_metrics):
    """
    This function is designed to create a special 'total'
    AggregateMetricForDate for a particular metric for each date.

    This is intended to show the relative
    count/success rate/failure rate:
        a. across all tables
        b. across all HPOs
        c. on the same date
        d. on the same metric type

    Parameters
    ----------
    aggregate_metrics (list): contains AggregateMetricForHPO
        objects that reflect each date, metric, and HPO combination
        (regardless of table)

    Return
    ------
    agg_metrics_for_dates (list): contains the
        AggregateMetricForDate objects that we laid out above.
    """
    dates, metrics, agg_metrics_for_dates = \
        find_unique_dates_and_metrics(aggregate_metrics=aggregate_metrics)

    # should ultimately be len(dates) x len(metrics) AMFD objects
    for date in dates:
        for metric in metrics:
            num_pertinent_rows, num_total_rows = 0, 0

            # find the relevant metrics - add if relevant
            for agg_hpo_metric in aggregate_metrics:
                if agg_hpo_metric.date == date \
                        and agg_hpo_metric.metric_type == metric:

                    hpo_total_rows = agg_hpo_metric.num_total_rows
                    hpo_pert_rows = agg_hpo_metric.num_pertinent_rows

                    num_pertinent_rows += hpo_pert_rows
                    num_total_rows += hpo_total_rows

            amfd = AggregateMetricForDate(
                date=date, metric_type=metric,
                num_total_rows=num_total_rows,
                num_pertinent_rows=num_pertinent_rows)

            agg_metrics_for_dates.append(amfd)

    return agg_metrics_for_dates
