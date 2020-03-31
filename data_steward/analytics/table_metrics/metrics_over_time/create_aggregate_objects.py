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

from aggregate_metric_class import AggregateMetricForTable, \
    AggregateMetricForHPO, AggregateMetricForDate


def create_aggregate_metric_master_function(
        metric_dictionary, hpo_dictionary, user_choice,
        sheet_output, datetimes):
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

    user_choice (string): represents the sheet from the
        analysis reports whose metrics will be compared
        over time

    sheet_output (string): determines the type of 'output'
        to be generated (e.g. the sheets are HPOs or the
        sheets are tables)

    datetimes (list): list of datetime objects that
        represent the dates of the files that are being
        ingested

    Returns
    -------
    # FIXME:
    """
    if sheet_output == 'table_sheets':
        aggregate_metrics = create_aggregate_metrics_for_table(
            metric_dictionary=metric_dictionar,
            datetimes=datetimes)
    elif sheet_output == 'hpo_sheets':
        pass
    else:  # should not be allowed
        raise Exception(
            "Bad parameter input for function \
            create_aggregate_master_function - sheet_output \
            parameter")

    return aggregate_metrics


def create_aggregate_metrics_for_table(
        metric_dictionary, datetimes):
    """
    Function is intended to create 'aggregate' data quality
    metrics that can be applied to a specific data quality metric
    for a particular date (across all HPOs). This
    AggregateMetricForTable object will contain information across
    all of the different sites.

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

    # A
    for metric_type, hpo_object_list in metric_dictionary.items():

        # need to create tables for each metric - varies by metric
        tables_for_metric = []

        for hpo_object in hpo_object_list:
            relevant_metrics = hpo_object.use_string_to_get_relevant_objects(
                metric=metric_type)
            for metric in relevant_metrics:
                table = metric.table
                tables_for_metric.append(table)

        # now we know the tables and dates for all of the metrics

        # B.
        for date in datetimes:

            #C
            for table in tables_for_metric:
                # to add to the new object's attributes
                total_rows, pertinent_rows = 0, 0

                # now we need to find the relevant DataQualityMetric objects
                for hpo_object in hpo_object_list:
                    relevant_dqms = hpo_object.use_string_to_get_relevant_objects(
                        metric=metric_type)

                    for dqm in relevant_dqms:

                        # warrants 'counting' towards the metric to create
                        if (dqm.metric_type == metric_type and
                            dqm.date == date and
                                dqm.table == table):

                            hpo_succ_rate, hpo_total_rows = \
                                hpo_object.use_table_name_to_find_rows(
                                    table=table, metric=metric_type)

                            hpo_pert_rows = hpo_succ_rate * hpo_total_rows / 100

                            total_rows += hpo_total_rows
                            pertinent_rows += hpo_pert_rows

                # actually create the metric
                new_am = AggregateMetricForTable(
                    date=date, table_name=table, metric_type=metric_type,
                    num_total_rows=total_rows, num_pertinent_rows=pertinent_rows)

                new_agg_metrics.append(new_am)

    return new_agg_metrics

