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
    # FIXME: need to change the 'aggregate metrics' for integration metrics
    #  they should NOT be weighted by site/table row count

    if metric_choice in metrics_to_weight:
        if sheet_output == 'table_sheets':
            aggregate_metrics = create_aggregate_metrics_for_tables(
                metric_dictionary=metric_dictionary,
                datetimes=datetimes)

        elif sheet_output == 'hpo_sheets':
            aggregate_metrics = create_aggregate_metrics_for_hpos(
                hpo_dictionary=hpo_dictionary,
                datetimes=datetimes,
                metric_dictionary=metric_dictionary)
        else:
            raise Exception(
                """Bad parameter input for function 
                create_aggregate_master_function. Parameter provided
                was: {param}""".format(param=sheet_output))
    else:  # integration metrics
        pass

    return aggregate_metrics


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


def create_aggregate_metrics_for_tables(
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


def create_aggregate_metrics_for_hpos(
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


