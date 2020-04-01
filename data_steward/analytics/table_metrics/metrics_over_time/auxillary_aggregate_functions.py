"""
This file is used to store 'auxillary' functions that are used
to create AggregateMetric objects. These auxillary functions should
be useful in ensuring that the main create_aggregate_objects.py
file remains uncluttered and readable.
"""


def find_relevant_tables(
    hpo_object_list, metric_type):
    """
    This function is used to find the tables that should be
    either triaged into separate AggregateMetric objects
    (as in the case of AggregateMetricForTable) or iterated
    over (as in the case of AggregateMetricForHPO).

    Parameters
    ----------
    hpo_object_list (list): HPO objects that will be iterated
        over. we intend to return the tables that exist across
        all of the DataQualityMetrics for the particular
        metric_type

    metric_type (string): shows the kind of metric that is
        being determined (e.g. duplicate records)

    Return
    ------
    tables_for_metric (list): contains all of the tables
        that exist across all of the HPO objects for
        the specified metric_type
    """

    # need to create tables for each metric - varies by metric
    tables_for_metric = []

    for hpo_object in hpo_object_list:
        relevant_dqms= hpo_object.use_string_to_get_relevant_objects(
            metric=metric_type)

        for dqm in relevant_dqms:
            table = dqm.table

            if table not in tables_for_metric:
                tables_for_metric.append(table)

    return tables_for_metric


def cycle_through_dqms_for_hpo(
    hpo_object, metric, date, hpo_name, tables_counted,
    total_rows, pertinent_rows):
    """
    Function is used once an HPO is found and warrants its own
    AggregateMetricForHPO because it has a unique set of date
    and metric parameters.

    Parameters
    ----------
    hpo_object (HPO): object of class HPO that has all the
        information we want to sort across (and ultimately
        average across all of the applicable tables)

    metric (string): represents the kind of metric that
        is to be investigated (e.g. duplicates)

    date (datetime): the datetime that should be unique
        for the AggregateMetricForHPO to be created.

    hpo_name (string): name of the HPO object

    tables_counted (list): list of tables that should not
        be counted in the 'overall tally'. this is used to
        prevent the same table from being counted more than
        once

    total_rows (float): starts at zero. goal is to add the
        total number of rows that span the
        HPO across all of the tables

    pertinent_rows (float): starts at zero. goal is to add
        the total number of rows that either
        contribute to either the 'success' or failure rate

    Returns
    -------
    total_rows (float): total number of rows that span the
        HPO across all of the tables

    pertinent_rows (float): total number of rows that either
        contribute to either the 'success' or failure rate

    tables_counted (list): list of tables that should not
        be counted in the 'overall tally'. now also contains
        the tables that contributed to the overall tally for
        the particular HPO on the particular date
    """
    relevant_dqms = hpo_object.use_string_to_get_relevant_objects(
                                metric=metric)

    for dqm in relevant_dqms:

        # regardless of dqm.table
        if (dqm.date == date and
            dqm.hpo == hpo_name and
            dqm.metric_type == metric) and \
                (hpo_object.date == date) and \
                dqm.table not in tables_counted:

            table = dqm.table
            metric_type = dqm.metric_type

            hpo_pert_rows, hpo_total_rows = \
                hpo_object.use_table_name_to_find_rows(
                    table=table, metric=metric_type)

            total_rows += float(hpo_total_rows)
            pertinent_rows += float(hpo_pert_rows)

            # prevent double counting
            tables_counted.append(dqm.table)

    return total_rows, pertinent_rows, tables_counted


def cycle_through_dqms_for_table(
    hpo_object, metric_type, date, table, hpos_counted,
    total_rows, pertinent_rows):
    """
    Function is used once an HPO is found and warrants its own
    AggregateMetricForHPO because it has a unique set of date
    and metric parameters.

    Parameters
    ----------
    hpo_object (HPO): object of class HPO that has all the
        information we want to sort across (and ultimately
        average across all of the applicable tables)

    metric (string): represents the kind of metric that
        is to be investigated (e.g. duplicates)

    date (datetime): the datetime that should be unique
        for the AggregateMetricForTable to be created.

    hpo_name (string): name of the HPO object

    hpos_counted (list): list of HPOs that should not
        be counted in the 'overall tally'. this is used to
        prevent the same HPO from being counted more than
        once

    total_rows (float): starts at zero. goal is to add the
        total number of rows that span the
        table across all of the HPOs

    pertinent_rows (float): starts at zero. goal is to add
        the total number of rows that either
        contribute to either the 'success' or failure rate

    Returns
    -------
    total_rows (float): total number of rows that span the
        table across all of the HPOs

    pertinent_rows (float): total number of rows that either
        contribute to either the 'success' or failure rate

    hpos_counted (list): list of HPOs that should not
        be counted in the 'overall tally'. now also contains
        the HPOs that contributed to the overall tally for
        the particular HPO on the particular date
    """

    relevant_dqms = hpo_object.use_string_to_get_relevant_objects(
        metric=metric_type)

    for dqm in relevant_dqms:

        # regardless of dqm.hpo
        # warrants 'counting' towards the metric to create
        if (dqm.metric_type == metric_type and
            dqm.date == date and
            dqm.table == table) and \
                hpo_object.name not in hpos_counted:

            hpo_pert_rows, hpo_total_rows = \
                hpo_object.use_table_name_to_find_rows(
                    table=table, metric=metric_type)

            # float conversion for consistency
            total_rows += float(hpo_total_rows)
            pertinent_rows += float(hpo_pert_rows)

    hpos_counted.append(hpo_object.name)  # prevent from counting again

    return hpos_counted, total_rows, pertinent_rows
