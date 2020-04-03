"""
File is used to store the functions that are used to create
unweighted aggregate metrics. These are metrics that do
NOT weight the sites' contributions to the overall metric
based on row count.

These functions are called in
the create_aggregate_objects file and harness many of the
functions in the auxillary_aggregate_functions file.
"""

from aggregate_metric_classes import AggregateMetricForTable, \
    AggregateMetricForHPO, AggregateMetricForDate


from auxillary_aggregate_functions import find_relevant_tables, \
    cycle_through_dqms_for_table, cycle_through_dqms_for_hpo, \
    find_unique_dates_and_metrics, \
    get_stats_for_unweighted_table_aggregate_metric


def create_unweighted_aggregate_metrics_for_tables(
    metric_dictionary, datetimes):
    """
    Function is intended to create 'aggregate' data quality
    metrics that can be applied to a specific data quality metric
    for a particular date (across all HPOs).

    This metric is NOT weighted. This means that all of the HPOs
    should ultimately contribute equally to the ending metric.

    Parameters
    ----------
    metric_dictionary (dict): has the following structure
        keys: all of the different metric_types possible
        values: all of the HPO objects that
            have that associated metric_type

    datetimes (list): list of datetime objects that
        represent the dates of the files that are being
        ingested
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

                hpos_counted = []  # to avoid repeats
                unweighted_metrics_for_hpos = []

                for hpo_object in hpo_object_list:

                    unweighted_metrics_for_hpos, hpos_counted = \
                        get_stats_for_unweighted_table_aggregate_metric(
                            hpo_object=hpo_object,
                            metric_type=metric_type, date=date,
                            table=table, hpos_counted=hpos_counted,
                            unweighted_metrics_for_hpos=unweighted_metrics_for_hpos)

                # setting these equal to 0 to differentiate these as a metric
                total_rows = 0
                pertinent_rows = 0

                # here's where the 'unweighted' aspect comes in - simple mean
                overall_rate = sum(unweighted_metrics_for_hpos) / len(unweighted_metrics_for_hpos)

                new_uw_agg_metric = AggregateMetricForTable(
                    date=date, table_name=table, metric_type=metric_type,
                    num_total_rows=total_rows, num_pertinent_rows=pertinent_rows)

                new_uw_agg_metric.manually_set_overall_rate(rate=overall_rate)

                new_agg_metrics.append(new_uw_agg_metric)

    return new_agg_metrics


def create_unweighted_aggregate_metrics_for_hpos(
    hpo_dictionary, datetimes, metric_dictionary):
    """
    Function is intended to create 'aggregate' data quality
    metrics that can be applied to a specific data quality metric
    for a particular HPO (across all tables).

    These metrics, however, should NOT be weighted. Each HPO
    should contribute equally regardless of the number of
    rows.

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
        (regardless of table). Again, this is unweighted.
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

                            pass  # FIXME

                # setting these equal to 0 to differentiate these as a metric
                total_rows = 0
                pertinent_rows = 0

                new_agg_metric = AggregateMetricForHPO(
                    date=date, hpo_name=hpo, metric_type=metric,
                    num_total_rows=total_rows,
                    num_pertinent_rows=pertinent_rows)

                new_agg_metrics.append(new_agg_metric)

    # finished the loop - now has all the aggregate metrics
    return new_agg_metrics

